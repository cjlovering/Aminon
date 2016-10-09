import time
import os
import sys
import subprocess


def do_query(fi):
    cmd='sh scanner_query.sh asset.com'
    pr = subprocess.Popen([cmd], stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    out, err = pr.communicate()
    vals = out.splitlines()
    diff=float(vals[-1])-float(vals[-2])
    print diff
    fi.write(str(diff)+'\n')

def main(fi):
    for a in range(0,3):
        for x in range(0,100):
            do_query(fi)
    fi.close()


if __name__=="__main__":

    fi=open("times.txt", "a")
    main(fi)
