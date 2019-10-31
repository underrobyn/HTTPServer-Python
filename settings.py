import json

config = {}

if __name__ != "__main__":
    try:
        with open("_config.json","r") as setting_file:
            print("Config file read from file.")
            config = json.loads(setting_file.read())
    except FileNotFoundError as e:
        print("Could not find _config.json\nPlease create one.")
        exit(0)