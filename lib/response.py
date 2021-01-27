from lib.router import HTTPRouter

http_status_codes = {
	200:"OK",
	201:"Created",
	202:"Accepted",
	204:"No Content",
	206:"Partial Content",

	400:"Bad Request",
	401:"Unauthorized",
	403:"Forbidden",
	404:"Not Found",
	405:"Method Not Allowed",
	408:"Request Timeout",
	410:"Gone",
	414:"URI Too Long",
	418:"I'm a teapot",
	429:"Too Many Requests",
	431:"Request Header Fields Too Large",

	500:"Internal Server Error",
	501:"Not Implemented"
}

class HTTPResponder:

	def __init__(self, socket, http_data):
		# Request variables
		self.request_method = "GET"
		self.request_uri = "/"
		self.query_string = ""
		self.query_string_dict = {}
		self.request_protocol = "/"
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
			if len(i) == 0: continue

			if ":" in i:
				header_pair = i.split(": ")
				header_dict[header_pair[0]] = header_pair[1]
			else:
				protocol = i.split(" ")

		self.request_headers = header_dict

		self.request_method = protocol[0]
		self.request_uri = protocol[1]
		self.request_protocol = protocol[2]
		
		if '?' in self.request_uri:
			qss = self.request_uri.split("?")
			self.request_uri = qss[0]
			self.query_string = qss[1]
		
		if len(self.query_string) > 0:
			kv_pairs = self.query_string.split("&")
			
			for kvpair in kv_pairs:
				value = '1'
				key = kvpair
				
				if '=' in kvpair:
					kvdata = kvpair.split("=")
					key = kvdata[0]
					value = kvdata[1]
				
				self.query_string_dict[key] = value
			

	def content_length(self):
		self.headers["Content-Length"] = len(self.body)

	def http_status(self):
		if self.status not in http_status_codes:
			self.status = 500

		return "HTTP/1.1 %s %s" % (self.status, http_status_codes[self.status])

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

		# Add protocol and status
		response = response + self.http_status()

		# Add HTTP Headers
		response = response + self.http_headers()

		# Add HTTP Body
		response = response + self.http_body()

		# Send response and close the connection
		self.socket.send_response(response)
		self.socket.close()