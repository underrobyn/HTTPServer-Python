from lib.sock import HTTPSock
from lib.settings import config

def main():
    server = HTTPSock()
    server.set_settings(config)
    server.start()

if __name__ == '__main__':
    main()