from threading import *
from connection import HTTPClient
import socket

class ServerSock(Thread):

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

		# Run the server
		self.listen()

	def set_settings(self, settings):
		# Load settings
		self.host = None if "host" not in settings else settings["host"]
		self.port = 8080 if "port" not in settings else settings["port"]
		self.timeout = 30 if "timeout" not in settings else settings["timeout"]

	def listen(self):
		print("Socket server running on %s:%s" % (self.host, self.port))

		while True:
			conn, address = self.sock.accept()

			c = HTTPClient(conn, address, self.client_count)
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