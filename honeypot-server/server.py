# Python Imports
from BaseHTTPServer import HTTPServer, BaseHTTPRequestHandler
from SocketServer import ThreadingMixIn
from urlparse import parse_qs
import threading
import os.path

# Some constants
EXIT_CODE_BAD_CONFIG_FILE = 1
EXIT_CODE_KEYBOARD_INTERRUPT = 0

# Some global definitions
env_var = {}

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

# Web Request Handler
class Handler(BaseHTTPRequestHandler):
	def do_GET(self):
		# Serve the page accordingly
		if self.path == "/":
			self.send_response(200)
			self.send_header("Content-Type", "text/html")
			self.end_headers()
			# Generate the output bogy
			response_body = "<h3>Which number is betwen eight and ten?</h3>\n"
			response_body += "<form action='check_solution.html'>\n"
			response_body += "  <input type='text' name='solution' />\n"
			response_body += "  <br />\n"
			response_body += "  <input type='submit' value='Submit' />\n"
			response_body += "</form>"
			# Send the response body
			self.wfile.write(response_body)
		elif self.path.startswith("/check_solution.html"):
			self.send_response(200)
			self.send_header("Content-Type", "text/html")
			self.end_headers()
			# Parse the query parameters 
			query_params = parse_qs(self.path[len("/check_solution.html") + 1:])
			if "solution" not in query_params or query_params["solution"][0] != "nine":
				# Form the response leading them back to the home page
				response_body = "<h3>Wrong answer! Try again.</h3>"
				response_body += "Click <a href='/'>here</a> to try again"
				# Send the response back
				self.wfile.write(response_body)
			else:
				# Now, process the user doing well on the Captcha phase
				self.wfile.write("<h4>You passed!</h4>")

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
