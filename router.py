from settings import (config, http_files)

class HTTPRouter:

	def __init__(self, responder):
		self.responder = responder

		if responder.request_protocol != "HTTP/1.1":
			print("Invalid HTTP protocol requested.")
			self.responder.status = 400
			return

		request_handlers = {
			"GET":self.handle_get_request,
			"POST":self.handle_post_request
		}
		if self.responder.request_method in request_handlers:
			request_handlers[self.responder.request_method]()
		else:
			self.invalid_request_method()

	def get_request_file(self, file):
		request_file = file[1:]

		if len(request_file) == 0:
			return "index.html"
		else:
			return request_file

	def handle_get_request(self):
		request_file = self.get_request_file(self.responder.request_uri)
		file_status = http_files.load_file_status(request_file)

		print("Attempting: status[%s] for GET %s" % (file_status, request_file))

		if file_status != 200:
			self.responder.status = file_status
			return

		self.responder.body = http_files.load_file_content(request_file)

	def handle_post_request(self):
		self.responder.status = 501
		print("Not Implemented: %s" % self.responder.request_protocol)

	def invalid_request_method(self):
		self.responder.status = 400
		print("Invalid request method: %s" % self.responder.request_protocol)