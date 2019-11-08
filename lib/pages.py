from lib.utils import *
from re import match

class ServerPages:

	def __init__(self, server_docs = "docs"):
		self.server_docs = get_full_dir_link(server_docs)

		self.dir_list_file = "dir.html"


	def get_rel_link(self, file):
		return self.server_docs + file

	def get_file_content(self, rel_file):
		if not check_can_read(rel_file): return "FileReadDenied::" + rel_file

		with open(rel_file, "r") as data_file:
			return data_file.read()


	def var_rule_time(self, content):
		# print(content)
		pass

	def parse_vars(self, content):
		rules = match(r"{{[a-z]+::[a-z_|]+\}\}", content)
		self.var_rule_time(content)


	def directory_list(self, directory):
		rel_file = self.get_rel_link(self.dir_list_file)
		dir_list_html = self.get_file_content(rel_file)

		self.parse_vars(dir_list_html)
		list_dir_contents(directory)

		return dir_list_html


	def error_page(self, status):
		rel_file = self.get_rel_link("%s.html" % status)

		if not check_file_exists(rel_file):
			return "FileNotExist::" + rel_file

		error_page_html = self.get_file_content(rel_file)

		self.parse_vars(error_page_html)

		return error_page_html