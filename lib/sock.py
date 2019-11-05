from threading import *
from lib.connection import HTTPClient
from lib.logger import HTTPLog
import socket

class HTTPSock(Thread):

	def run(self):
		# Create server socket
		self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

		# Update timeout settings
		if socket.getdefaulttimeout() != self.timeout:
			socket.setdefaulttimeout(self.timeout)
			print("Updated socket timeout, new value: %s" % self.timeout)

		# Make server listen for connections
		self.sock.bind((self.host, self.port))
		self.sock.listen(5)

		# Create socket specific attributes
		self.clients = []
		self.client_count = 0
		self.client_logger = HTTPLog(1, "httpclient", "text")

		# Run the server
		self.listen()

	# Load settings
	def set_settings(self, settings):
		self.host = None if "host" not in settings["socket"] else settings["socket"]["host"]
		self.port = 8080 if "port" not in settings["socket"] else settings["socket"]["port"]
		self.timeout = 30 if "timeout" not in settings["socket"] else settings["socket"]["timeout"]

	def listen(self):
		print("Socket server running on %s:%s" % (self.host, self.port))

		while True:
			conn, address = self.sock.accept()

			c = HTTPClient(conn, address, self.client_count, self.client_logger)
			c.start()

			self.clients.append(c)
			self.client_count = self.client_count + 1

			print("Socket connected: %s" % address[0])

	def close(self):
		print("Closing server socket %s:%s" % (self.host, self.port))

		# If the socket still exists, close it
		if self.sock:
			self.sock.close()
			self.sock = None
			print("Socket closed.")