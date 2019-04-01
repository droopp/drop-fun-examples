#
# xml maker
# $1 number of dublicate
#


import sys
import time

# API


def read():
    msg = sys.stdin.readline()
    return msg.strip()


def log(m):
    sys.stderr.write("{}: {}\n".format(time.time(), m))
    sys.stderr.flush()


def send(m):
    sys.stdout.write("{}\n".format(m))
    sys.stdout.flush()


# Process - actor
#  read - recieve message from world
#  send - send message to world
#  log  -  logging anything


def main(num):
    while 1:

        msg = read()
        if not msg:
            break

        log("get message: " + msg)

        try:

            msg0 = msg.split(",")

            xml = """<root><date>{}</date><data>{}</data></root>""".format(msg0[1], msg0[2])

            send(xml)

        except Exception as e:
            log(e)
            send(msg)


if __name__ == "__main__":
    main(int(sys.argv[1]))
