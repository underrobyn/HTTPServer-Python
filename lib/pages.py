from lib.utils import *

class ServerPages:

	def __init__(self, server_docs = "docs"):
		self.server_docs = get_full_dir_link(server_docs)

	# TODO: Handle directory listing as well as 4xx/5xx errors
	def directory_list(self, directory):
		pass

	def error_page(self, status):
		pass