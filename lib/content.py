from lib.utils import *

class FileServe:

	def __init__(self, http_docs = 'www', http_config = '.httpconf'):
		self.http_docs = get_full_dir_link(http_docs)
		self.http_conf = http_config

		if not check_dir_exists(self.http_docs):
			print("%s does not exist. It will be created." % self.http_docs)
			create_dir_if_not_exists(self.http_docs)

	def get_rel_link(self, file):
		return self.http_docs + file

	def load_file_status(self, file):
		rel_file = self.get_rel_link(file)

		if not check_file_exists(rel_file):
			return 404

		if not check_can_read(rel_file):
			return 403

		return 200

	def load_file_content(self, file):
		rel_file = self.get_rel_link(file)

		self.load_file_conf(rel_file)

		with open(rel_file, "r") as data_file:
			return data_file.read()

	def load_file_conf(self, file):
		return self.load_dir_conf(get_dir_for_file(file))

	def load_dir_conf(self, dir):
		conf_dir = dir + os.path.sep
		conf_file = conf_dir + self.http_conf

		if not check_file_exists(conf_file):
			print("%s does not have a config file." % conf_dir)

		if check_can_read(conf_file):
			print("%s cannot be read" % conf_file)