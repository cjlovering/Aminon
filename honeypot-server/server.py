# Python Imports
from BaseHTTPServer import HTTPServer, BaseHTTPRequestHandler
from SocketServer import ThreadingMixIn
from urlparse import parse_qs
import threading, os.path, string, random, thread, time

# Some constants
EXIT_CODE_BAD_CONFIG_FILE = 1
EXIT_CODE_KEYBOARD_INTERRUPT = 0

# Some CAPTCHA Questions
CAPTCHA_QA = [
		("What has spots, lives on a farm, and likes to mo0o0oooOO from dawn till dusk?", "cow"),
		("What number does the string n!yn resemble? Write the word for the number.", "nine")
	     ]

# Some global definitions
env_var = {}
session_store = {}

# Basic Helper Functions
def read_from_config(file_name="config"):
	if not os.path.isfile(file_name):
		# Path doesn't exist
		exit(EXIT_CODE_BAD_CONFIG_FILE)
	# Else, process the file and store the environment variables
	try:
		with open(file_name, "r") as file:
			for line in file:
				# Going over each line in the file
				splitted = line.strip().split("=")
				key, value = splitted[0].strip(), "=".join(splitted[1:])
				# Add it to the environment variables map
				env_var[key] = value
	except IOError as exception:
		exit(EXIT_CODE_BAD_CONFIG_FILE)
	# Return true to indicate success
	return True

def getSessionID():
	return "".join(random.SystemRandom().choice(string.ascii_lowercase + string.ascii_uppercase + string.digits) for _ in range(20)) + "_" + str(int(time.time()))

def log_in_config(txt):
	if "LOG_OUTPUT" not in env_var: return
	# Else, open the file and write
	try:
		with open(env_var["LOG_OUTPUT"], "a") as file:
			file.write(str(int(time.time())) + ": " + txt + "\n")
	except:
		print "Failed to write to log: ", txt
		return

# Web Request Handler
class Handler(BaseHTTPRequestHandler):
	def do_GET(self):
		# Serve the page accordingly
		if self.path == "/":
			# Grab the User-Agent from headers
			useragent_header = ""
			if "User-Agent" in self.headers:
				useragent_header = ". User came in with User-Agent: " + self.headers["User-Agent"]
			# Send the response back
			self.send_response(200)
			self.send_header("Content-Type", "text/html")
			self.end_headers()
			# Generate a session ID
			session_id = getSessionID()
			# Generate a random question number
			question_num = random.randint(0, len(CAPTCHA_QA) - 1)
			question = CAPTCHA_QA[question_num][0]
			# Add it to the session store/map
			session_store[session_id] = (question_num, self.client_address[0])
			# Generate the output body
			response_body  = "<h3>" + question  + "</h3>\n"
			response_body += "<form action='check_solution.html'>\n"
			response_body += "  <input type='text' name='solution' />\n"
			response_body += "  <input type='hidden' name='secret' value='"
			response_body += session_id
			response_body += "' />\n"
			response_body += "  <br />\n"
			response_body += "  <input type='submit' value='Submit' />\n"
			response_body += "</form>"
			# Send the response body
			self.wfile.write(response_body)
			# Log this event
			log_in_config("Thread with ID " + str(thread.get_ident()) + " was spawned to serve / to user at " + self.client_address[0]  + " with a fresh session ID: " + session_id + useragent_header)
		elif self.path.startswith("/check_solution.html"):
			# Grab the User-Agent from headers
			useragent_header = ""
			if "User-Agent" in self.headers:
				useragent_header = " User can in with User-Agent: " + self.headers["User-Agent"]
			# Send the response back
			self.send_response(200)
			self.send_header("Content-Type", "text/html")
			self.end_headers()
			# Parse the query parameters 
			query_params = parse_qs(self.path[len("/check_solution.html") + 1:])
			if "secret" not in query_params or query_params["secret"][0] not in session_store or \
			   "solution" not in query_params or query_params["solution"][0] != CAPTCHA_QA[session_store[query_params["secret"][0]][0]][1] or \
			   session_store[query_params["secret"][0]][1] != self.client_address[0]:
				# Form the response leading them back to the home page
				response_body = "<h3>Wrong answer! Try again.</h3>"
				response_body += "Click <a href='/'>here</a> to try again"
				# Send the response back
				self.wfile.write(response_body)
				# Log this event
				session_id = "an invalid session ID"
				if "secret" in query_params and query_params["secret"][0] in session_store:
					session_id = "existing session ID " + query_params["secret"][0]
				log_in_config("Thread with ID " + str(thread.get_ident()) + " was spawned to serve /check_solution.html to user at " + self.client_address[0] + " with " + session_id + ". The user didn't pass the CAPTCHA challenge." + useragent_header)
			else:
				# Now, process the user doing well on the Captcha phase
				self.wfile.write("<h4>You passed!</h4>")
				# Log this event
				log_in_config("Thread with ID " + str(thread.get_ident()) + " was spawned to serve /check_solution.html to user " + self.client_address[0] + " with existing session ID " + query_params["secret"][0]  + ". The user passed the CAPTCHA challenge." + useragent_header)
			# Nonetheless, invalide the session to prevent response brute-forcing
			if "secret" in query_params and query_params["secret"][0] in session_store:
				session_store.pop(query_params["secret"][0])

# Threaded Server
class ThreadedHTTPServer(ThreadingMixIn, HTTPServer):
	"""Handles requests in a separate thread."""

# Main
def main():
	# Read from the config file
	read_from_config()
	# Configure the server
	host = "0.0.0.0"
	port = int(env_var["PORT"])
	# Now fire up the server
	try:
		ThreadedHTTPServer((host, port), Handler).serve_forever()
	except KeyboardInterrupt:
		exit(EXIT_CODE_KEYBOARD_INTERRUPT)

if __name__ == "__main__":
	main()
