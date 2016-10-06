import argparse
import subprocess
import time
import sys

def restart_scan():
    start_scan()

def try_ip(a, b, c, d):
    ip = "%d.%d.%d.%d" % (a, b, c, d)
    cmd = "sh scanner_query.sh %s" % ip
    p = subprocess.call([cmd], shell=True)

def start_scan(run_time):
    for a in range(1, 191):
        if a == 10 or a == 191:
            pass
        else:
            for b in range(1,255):
                for c in range(1,255):
                    for d in range (1,255):
                        try_ip(a, b, c, d)
                        if (time.time()-start_time) >= run_time:
                            sys.exit()
    restart_scan()


def __name__=="__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument('-t',
                        '--time',
                        help='Length of time to run scan attack in seconds, default 60')
    args = parser.parse_args()

    if args.time:
        run_time = args.time
    else
        run_time = 60

    global start_time
    start_time=time.time()

    start_scan(run_time)
