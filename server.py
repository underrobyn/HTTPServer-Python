from sock import ServerSock

settings = {
    "host":"0.0.0.0",
    "port":3698,
    "timeout":30
}

def main():
    server = ServerSock()
    server.set_settings(settings)
    server.start()

if __name__ == '__main__':
    main()