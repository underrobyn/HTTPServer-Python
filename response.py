from router import HTTPRouter
from settings import config

class HTTPResponder:

	def __init__(self, socket, http_data):
		# Request variables
		self.method = "GET"
		self.request_uri = "/"
		self.request_headers = {}

		# Response variables
		self.status = 200
		self.headers = {
			"Server": "HTTPServer"
		}
		self.body = ""

		# Data passed to class
		self.socket = socket
		self.http_data = http_data

		# Create a response based on request data
		self.decode_request(http_data)

		HTTPRouter()

		# Form a response and send it
		self.http_respond()

	def decode_request(self, headers):
		print(headers)

	def content_length(self):
		self.headers["Content-Length"] = len(self.body)

	def http_status(self):
		# Protocol being used
		status = "HTTP/1.1 "

		if self.status == 200:
			status = status + "204 No Content"
		elif self.status == 404:
			status = status + "404 Not Found"
		else:
			status = status + "500 Internal Server Error"

		return status

	# Generate HTTP headers incl. status code
	def http_headers(self):
		# Create break between protocol and headers
		headers = "\r\n"

		# Loop over headers in dictionary
		for header in self.headers:
			header_text = "%s: %s\r\n" % (header, self.headers[header])
			headers = headers + header_text

		return headers

	def http_body(self):
		# Break between headers and body
		return "\r\n\n" + self.body

	# Send a full HTTP response
	def http_respond(self):
		# Now we can formulate a valid HTTP response
		response = ""

		# Generate content-length header
		self.content_length()

		# Add protocol and status
		response = response + self.http_status()

		# Add HTTP Headers
		response = response + self.http_headers()

		# Add HTTP Body
		response = response + self.http_body()

		# Send response and close the connection
		self.socket.send_response(response)
		self.socket.close()