##
# Estore func
#

import sys
import time

import threading
import Queue
import json

from gevent import monkey
from gevent.pool import Pool
import gevent

monkey.patch_all(thread=True,  sys=True)


# API

def read():
    line = sys.stdin.readline()
    return line.strip()


def log(m):
    sys.stderr.write("{}: {}\n".format(time.time(), m))
    sys.stderr.flush()


def send(m):
    sys.stdout.write("{}\n".format(m))
    sys.stdout.flush()


#  read - recieve message from world
#  send - send message to world
#  log  -  logging anything

def add_input(input_queue):

    while True:
        msg = read()

        if msg == "stop_async_worker":
            send(msg)
        else:
            input_queue.put(msg)


def process(args):

    msg, stime = args

    log("start working..")
    log("get message: " + msg)

    _b = time.time()

    # <0.652.0>:a77ca57c-0105-4366-897b-ea326f8d5545@192.168.50.6:<0.486.0>:1573:429363:10167::{"res_code":201}

    params = msg.split("::")

    msg = json.loads(params[1])

    # _uri = msg.get("uri")
    # _headers = msg.get("headers")
    # _method = msg.get("method")
    # _args = msg.get("args")

    _data = msg.get("data")

    gevent.sleep(int(stime))

    if _data.get("xcode") is not None:
        resp = {"x_res_code": _data.get("xcode"), "x_res_body": _data}

    else:
        resp = _data

    send("{}::{}".format(params[0], json.dumps(resp)))

    log("message send: {} ".format(time.time() - _b))


def main(num, stime):

    pool = Pool(int(num))

    input_queue = Queue.Queue()

    input_thread = threading.Thread(target=add_input, args=(input_queue,))
    input_thread.daemon = True
    input_thread.start()

    while 1:

        msg = input_queue.get()

        if not msg:
            break

        g = pool.spawn(process, (msg, stime))
        g.link_exception(exception_callback)


def exception_callback(g):
    """Process gevent exception"""
    try:
        g.get()
    except Exception as exc:
        log("error : {} ".format(exc))
        send(exc)

if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
