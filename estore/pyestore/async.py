#
# Async func
#

import sys
import time

import threading
import Queue
import json

import handler

from cassandra.cluster import Cluster
from cassandra.policies import DCAwareRoundRobinPolicy
# from cassandra.policies import RoundRobinPolicy

from cassandra.auth import PlainTextAuthProvider
# from cassandra import ConsistencyLevel
# from cassandra.query import BatchStatement
# from cassandra.query import SimpleStatement
# from cassandra import ReadTimeout

from gevent import monkey
from gevent.pool import Pool

monkey.patch_all(thread=True,  sys=True)


# CASS_URL = ['cassandra-1.staging.vc.restr.im',
#             'cassandra-2.staging.vc.restr.im',
#             'cassandra-3.staging.vc.restr.im']


# API

def read():
    line = sys.stdin.readline()
    return line.replace("\tncm\t", "\n").strip()


def log(m):
    sys.stderr.write("{}: {}\n".format(time.time(), m))
    sys.stderr.flush()


def send(m):
    sys.stdout.write("{}\n".format(m.replace("\tncm\t", "\n")))
    sys.stdout.flush()


#  read - recieve message from world
#  send - send message to world
#  log  -  logging anything


def get_session(hosts, k, l, p):

    while True:

        try:

            auth_provider = PlainTextAuthProvider(username=l, password=p)

            cluster = Cluster(hosts,
                              auth_provider=auth_provider,
                              load_balancing_policy=DCAwareRoundRobinPolicy(local_dc='dc1')
                              )

            session = cluster.connect(k)

            return session

        except Exception as e:
            log("Error during connection to cluster: {}".format(e))
            time.sleep(2)
            exit(1)


def add_input(input_queue):

    while True:
        msg = read()

        if msg == "stop_async_worker":
            send(msg)
        else:
            input_queue.put_nowait(msg)


def process(args):

    session, msg = args

    log("get message: " + msg)

    _b = time.time()

    params = msg.split("::")

    try:

        # <0.652.0>:a77ca57c-0105-4366-897b-ea326f8d5545@192.168.50.6:<0.486.0>:1573:429363:10167::{"res_code":201}

        msg = json.loads(params[1])

        _uri = msg.get("uri")
        _headers = msg.get("headers")
        _method = msg.get("method")
        _args = msg.get("args")
        _data = msg.get("data")

        resp = ""
        if _method == 'get':
            resp = handler.get(session, _uri, _headers, _args, _data)
        elif _method == 'post':
            resp = handler.post(session, _uri, _headers, _args, _data)
        elif _method == 'put':
            resp = handler.put(_uri, _headers, _args, _data)
        elif _method == 'patch':
            resp = handler.patch(_uri, _headers, _args, _data)
        elif _method == 'delete':
            resp = handler.delete(_uri, _headers, _args, _data)

        send("{}::{}".format(params[0], resp))

        log("message send: {} ".format(time.time() - _b))

    except Exception as e:
        send("{}::{}".format(params[0], json.dumps({"x_res_code": 500,
                                                    "x_res_body": str(e)})))


def main(num, hosts, klp):

    cass_urls = hosts.split(",")
    _klp = klp.split(",")

    session = get_session(cass_urls, _klp[0], _klp[1], _klp[2])

    pool = Pool(int(num))

    input_queue = Queue.Queue()

    input_thread = threading.Thread(target=add_input, args=(input_queue,))
    input_thread.daemon = True
    input_thread.start()

    while 1:

        msg = input_queue.get()

        if not msg:
            time.sleep(1)
            break

        g = pool.spawn(process, (session, msg))
        g.link_exception(exception_callback)


def exception_callback(g):
    """Process gevent exception"""
    try:
        g.get()
    except Exception as exc:
        log("error : {} ".format(exc))
        send(exc)

if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2], sys.argv[3])
