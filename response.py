class HTTPResponder:

	def __init__(self, socket, http_data):
		self.status = 200
		self.headers = {
			"Server": "HTTPServer"
		}
		self.body = http_data

		self.socket = socket
		self.http_data = http_data

		self.decode_headers(http_data)
		self.http_respond()

	def decode_headers(self, headers):
		pass
		print(headers)

	def content_length(self):
		self.headers["Content-Length"] = len(self.body)

	# Generate HTTP headers incl. status code
	def http_headers(self):
		# Protocol being used
		headers = "HTTP/1.1 "

		# TODO: Implement function to handle this.
		if self.status == 200:
			headers = headers + "200 OK"
		elif self.status == 404:
			headers = headers + "404 Not Found"
		else:
			headers = headers + "500 Internal Server Error"

		# Create break between protocol and headers
		headers = headers + "\r\n"

		# Loop over headers in dictionary
		for header in self.headers:
			header_text = "%s: %s\r\n" % (header, self.headers[header])
			headers = headers + header_text

		return headers

	def http_body(self):
		return self.body

	# Send a full HTTP response
	def http_respond(self):
		response = ""

		# Generate content-length header
		self.content_length()

		# Add HTTP Headers
		response = response + self.http_headers()

		# Break between headers and body
		response = response + "\r\n\n"

		# Add HTTP Body
		response = response + self.http_body()

		# Send response and close the connection
		self.socket.send_response(response)
		self.socket.close()