from threading import *
from time import time
from response import HTTPResponder
from settings import (config, log)
import select

class HTTPClient(Thread):

	def __init__(self, client_socket, client_addr, client_number, client_logger):
		super(HTTPClient, self).__init__()

		self.conn = client_socket
		self.addr = client_addr
		self.id = client_number
		self.logger = client_logger

		self.data = ""
		self.created = time()

	def run(self):
		log(1,"HTTPClient created at %s" % self.created)
		self.logger.log("HTTPClient created at %s" % self.created)

		closed = False
		while not closed:
			if not self.conn:
				log(2, "Socket connected to %s is no longer active" % (self.addr,))
				self.logger.log("Socket connected to %s is no longer active" % (self.addr,))
				break

			if self.conn._closed:
				log(2, "Socket connected to %s has been closed" % (self.addr,))
				self.logger.log("Socket connected to %s has been closed" % (self.addr,))
				break

			try:
				sock_read, sock_write, sock_err = select.select([self.conn], [], [])
			except select.error:
				log(3, "Select failed on socket connected to %s" % (self.addr,))
				self.logger.log("Select failed on socket connected to %s" % (self.addr,))
				return
			except OSError as e:
				log(3, str(e))
				return

			if len(sock_read) > 0:
				received = self.conn.recv(config["socket"]["recv_size"])

				if len(received) == 0:
					log(2, "Socket connected to %s has been closed" % (self.addr,))
					closed = True
				else:
					self.data = self.data + received.decode('utf-8')
					if self.data.endswith(u"\r\n"):
						HTTPResponder(self, self.data)

		self.active_time()

	def active_time(self):
		active_for = time() - self.created

		log(1, "HTTPClient object [#%s] is now dead after being active for %s" % (self.id, active_for))
		self.logger.log("HTTPClient object [#%s] is now dead after being active for %s" % (self.id, active_for))

	def send_response(self, data):
		self.conn.send(data.encode('utf-8'))

	def close(self):
		self.conn.close()