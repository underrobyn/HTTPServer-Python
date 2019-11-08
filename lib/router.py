from lib.settings import (http_files, server_docs, log, config)
from lib.utils import *

class HTTPRouter:

	def __init__(self, responder):
		self.responder = responder

		if self.responder.request_protocol != "HTTP/1.1":
			print("Invalid HTTP protocol requested.")
			self.responder.status = 400
			return

		request_handlers = {
			"GET":self.handle_get_request,
			"HEAD":self.handle_head_request,
			"POST":self.handle_post_request
		}
		if self.responder.request_method in request_handlers:
			request_handlers[self.responder.request_method]()
		else:
			self.invalid_request_method()

	def get_index_file(self, dir):
		rel_dir = http_files.get_rel_link(dir)
		valid_indexes = config["router"]["index_file"]
		index_file = ""

		if not check_dir_exists(rel_dir):
			return ""

		print(dir)
		print(list_dir_contents(rel_dir))

		for i in list_dir_contents(rel_dir):
			print(i)
			if i in valid_indexes:
				index_file = i
				break

		return index_file

	def get_request_file(self, file):
		if file[-1] == "/" or len(file[1:]) == 0:
			return self.get_index_file(file)
		else:
			return file

	def set_response(self, status, body):
		self.responder.status = status
		self.responder.body = body
		self.responder.content_length()

	def handle_get_request(self):
		rel_link = http_files.get_rel_link(self.responder.request_uri)
		request_file = self.get_request_file(self.responder.request_uri)

		if request_file == "" and check_dir_exists(rel_link):
			self.responder.body = server_docs.directory_list(rel_link)
			return

		file_status = http_files.load_file_status(request_file)

		print("Attempting: status[%s] for GET %s" % (file_status, request_file))

		if file_status != 200:
			self.responder.status = file_status
			self.responder.body = server_docs.error_page(file_status)
			return

		file_cont = http_files.load_file_content(request_file)

		self.set_response(file_status, file_cont)

	def handle_post_request(self):
		self.responder.status = 501
		log(3,"Not Implemented: %s" % self.responder.request_protocol)

	def handle_head_request(self):
		# Run request as GET
		self.handle_get_request()

		# Remove response body
		# Don't use self.set_response as it will reset Content-Length header
		self.responder.body = ""

	def invalid_request_method(self):
		self.responder.status = 400
		log(3,"Invalid request method: %s" % self.responder.request_protocol)