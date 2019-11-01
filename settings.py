from json import loads
from utils import *
from content import FileServe

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

# Configure some classes
http_files = FileServe(config["router"]["http_docs"], config["router"]["config_file"])