# Python Imports
from BaseHTTPServer import HTTPServer, BaseHTTPRequestHandler
from SocketServer import ThreadingMixIn
import threading, os.path, string, random, thread, time

# Some constants
EXIT_CODE_BAD_CONFIG_FILE = 1
EXIT_CODE_KEYBOARD_INTERRUPT = 0

# Cat Image Paths
CAT_IMAGES = ["cute-cat-1.png", "cute-cat-2.png", "cute-cat-3.png"]

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

def log_in_config(txt):
	if "LOG_OUTPUT" not in env_var: return
	# Else, open the file and write
	try:
		with open(env_var["LOG_OUTPUT"], "a") as file:
			file.write(txt + "\n")
	except:
		print "Failed to write to log: ", txt
		return

# Web Request Handler
class Handler(BaseHTTPRequestHandler):
	def do_GET(self):
		# Serve the page accordingly
		if self.path == "/":
			self.send_response(200)
			self.send_header("Content-Type", "text/html")
			self.end_headers()
			# Generate the response body
			response_body  = "<center>\n"
			response_body += "  <img src='"
			response_body += CAT_IMAGES[random.randint(0, len(CAT_IMAGES) - 1)]
			response_body += "' />\n"
			response_body += "  <br /><br />"
			response_body += "  <h3>This is the super-protected asset server!</h3>"
			response_body += "</center>\n"
			# Send the response body
			self.wfile.write(response_body)
			# Log this event
			log_in_config("Thread with ID " + str(thread.get_ident()) + " was spawned to serve / to user at " + self.client_address[0] + ".")
		elif self.path.endswith(".png"):
			# Sanitize the path by removing the initial forward-slash (/)
			self.path = self.path[1:]
			# Check if the file exists
			if not os.path.isfile(self.path):
				self.send_response(404)
				self.send_header("Content-Type", "type/html")
				self.end_headers()
				self.wfile.write("<h4>404 - File Not Found</h4>")
				# Log this event
				log_in_config("Thread with ID " + str(thread.get_ident()) + " was spawned to serve /" + self.path + " to user at " + self.client_address[0] + " but the file was not found.")
				# Now, return
				return
			# Else, we have the file, read and dump it to the web stream
			self.send_response(200)
			self.send_header("Content-Type", "image/png")
			self.end_headers()
			with open(self.path, "rb") as file:
				self.wfile.write(file.read())
			# Log this event
			log_in_config("Thread with ID " + str(thread.get_ident()) + " was spawned to serve /" + self.path + " to user at " + self.client_address[0] + ".")

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
