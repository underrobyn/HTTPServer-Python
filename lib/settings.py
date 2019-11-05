from json import loads
from sys import argv
from lib.utils import *
from lib.content import FileServe
from lib.pages import ServerPages


arguments = {}
config = {}
config_file = "_config.json"


# Get command line arguments from sys.argv
def parse_cli_args():
	global arguments

	if len(argv) < 2: return

	for i in argv:
		if "=" not in i: continue

		tokenised = i.split("=")
		if tokenised[0] == "" or tokenised[1] == "": continue

		arguments[tokenised[0]] = tokenised[1]

	apply_cli_args()


# Loop through parsed arguments in the form key=value to see if we are changing anything
def apply_cli_args():
	global arguments, config_file

	if "config" in arguments:
		config_file = arguments["config"]


def load_config():
	global config, config_file

	if not check_file_exists(config_file):
		print("Could not find %s" % config_file)
		exit(99)

	if not check_can_read(config_file):
		print("Unable to read %s" % config_file)
		exit(99)

	with open(config_file, "r") as setting_file:
		print("Config file read from file.")
		config = loads(setting_file.read())


parse_cli_args()
load_config()


# Console logging
def log(level, message):
	if level >= config["console"]["log_level"]:
		print(message)


# Configure some classes
http_files = FileServe(config["router"]["http_docs"], config["router"]["config_file"])
server_docs = ServerPages(config["router"]["server_docs"])