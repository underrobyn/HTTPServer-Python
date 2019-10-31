import os
from settings import config

class FileServe:

	def __init__(self, http_docs = 'www/'):
		self.http_docs = http_docs
		print(__file__)
		print(config)