from content import FileServe
from settings import config

class HTTPRouter:

	def __init__(self, responder):
		self.responder = responder

		FileServe()