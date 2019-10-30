from time import time
from os.path import isfile

class HTTPLog:

	def __init__(self, log_level, log_dir, log_name):
		self.log_level = log_level
		self.log_dir = log_dir
		self.log_name = log_name
		self.log_time = int(time())

		# Make sure log dir has a trailing slash
		if self.log_dir[-1] != "/":
			self.log_dir = self.log_dir + "/"

		# Check if the file already exists
		self.log_file = self.get_file()

		if isfile(self.log_file):
			print("File %s already exists!", self.log_file)

	def get_file(self):
		link = "%s%s_%s.log" % (self.log_dir, self.log_time, self.log_name)
		return link

	def log_file(self):
		# Open log file
		self.handle = open(self.get_file())

	def log_request(self, data, format):
		if format == "csv":
			return