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

		self.route = HTTPRouter(self)

		# Form a response and send it
		self.http_respond()

	def decode_request(self, headers):
		header_list = headers.split("\r\n")
		protocol = ""
		header_dict = {}

		for i in header_list:
			if ":" in i:
				header_pair = i.split(": ")
				header_dict[header_pair[0]] = header_pair[1]
			else:
				protocol = i

		print(protocol)
		print(header_dict)

	def content_length(self):
		self.headers["Content-Length"] = len(self.body)

	def http_status(self):
		# Protocol being used
		status = "HTTP/1.1 "

		if self.status == 200:
			status = status + "200 OK"
		elif self.status == 204:
			status = status + "204 No Content"
		elif self.status == 400:
			status = status + "400 Bad Request"
		elif self.status == 401:
			status = status + "401 Unauthorized"
		elif self.status == 403:
			status = status + "403 Forbidden"
		elif self.status == 404:
			status = status + "404 Not Found"
		elif self.status == 405:
			status = status + "405 Method Not Allowed"
		elif self.status == 408:
			status = status + "408 Request Timeout"
		elif self.status == 410:
			status = status + "410 Gone"
		elif self.status == 414:
			status = status + "414 URI Too Long"
		elif self.status == 418:
			status = status + "418 I'm a teapot"
		elif self.status == 429:
			status = status + "429 Too Many Requests"
		elif self.status == 431:
			status = status + "431 Request Header Fields Too Large"
		else:
			status = status + "500 Internal Server Error"

		return status

	# Generate HTTP headers
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