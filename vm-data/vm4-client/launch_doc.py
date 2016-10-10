import argparse
import subprocess
import time
import sys

def try_ip():
    cmd='sh doc_query.sh'
    subprocess.call([cmd], shell=True)

def start_scan():
    for a in range(0, 128):
            try_ip()


if __name__=="__main__":
    start_scan()
