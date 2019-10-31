from sock import HTTPSock
from settings import config

def main():
    server = HTTPSock()
    server.set_settings(config)
    server.start()

if __name__ == '__main__':
    main()