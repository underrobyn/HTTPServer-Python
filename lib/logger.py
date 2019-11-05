from time import time
from lib.utils import *
from lib.settings import config

class HTTPLog:

	def __init__(self, log_level, log_name, log_format):
		if not config["logs"]["enabled"]:
			print("[*]-> Logs are disabled in _config.json")
			return

		self.log_level = log_level
		self.log_name = log_name
		self.log_format = log_format

		self.log_time = int(time())

		self.log_dir = get_full_dir_link(config["logs"]["log_dir"])
		self.log_file = self.get_file()

		self.create_output()

	def get_extension(self):
		formats = {
			"text":"log",
			"csv":"csv",
			"tsv":"tsv"
		}
		return formats[self.log_format]

	def get_file(self):
		return "%s%s_%s.%s" % (self.log_dir, self.log_time, self.log_name, self.get_extension())

	def create_output(self):
		if check_file_exists(self.log_file):
			print("File %s already exists! It will be appended to." % self.log_file)

		if not create_dir_if_not_exists(self.log_dir):
			print("Failed to create logs directory: %s" % self.log_dir)

		if not create_file_if_not_exists(self.log_file):
			print("Failed to create log file: %s" % self.log_file)
		else:
			print("Log file: %s" % self.log_file)

		if not check_can_write(self.log_file):
			print("Failed to gain write permission for log file: %s" % self.log_file)

	def get_time_string(self):
		return "[" + str(time()) + "]: "

	def log(self, data):
		if not config["logs"]["enabled"]: return

		line = ""

		# TODO: Have logs conform to "Common Log Format"
		if self.log_format == "csv":
			return
		elif self.log_format == "common":
			return 
		elif self.log_format == "text":
			if config["logs"]["timestamp"]:
				line = line + self.get_time_string()
			line = line + data + "\n"

		with open(self.log_file, "a") as output_file:
			output_file.write(line)