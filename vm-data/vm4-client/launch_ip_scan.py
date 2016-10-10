import argparse
import subprocess
import time
import sys

def try_ip(d):
    ip = "10.4.6.%d" % d
    cmd = "sh scanner_query.sh %s" % ip
    p = subprocess.call([cmd], shell=True)

def start_scan(loops):
    for a in range(0, loops):
        for d in range (128,255):
            try_ip(d)


if __name__=="__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument('-q',
                        '--queries',
                        help=', default 2')
    args = parser.parse_args()

    if args.queries:
        loops = args.queries
    else:
        loops = 2

    start_scan(int(loops))
