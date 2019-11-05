from json import loads
from lib.utils import *
from lib.content import FileServe

config = {}
file = "_config.json"

if not check_file_exists(file):
	print("Could not find _config.json")
	exit(99)

if not check_can_read(file):
	print("Unable to read _config.json")
	exit(99)

with open(file,"r") as setting_file:
	print("Config file read from file.")
	config = loads(setting_file.read())

# Console logging

def log(level, message):
	if level >= config["console"]["log_level"]:
			print(message)


# Configure some classes
http_files = FileServe(config["router"]["http_docs"], config["router"]["config_file"])