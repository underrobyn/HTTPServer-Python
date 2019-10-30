class HTTPResponder:

	def __init__(self, socket, http_data):
		response = "HTTP/1.1 200 OK\r\n\n\n"

		response = response + http_data

		self.decode_headers(http_data)

		socket.send_response(response)
		socket.close()

	def decode_headers(self, headers):
		pass
		print(headers)