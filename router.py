from content import FileServe
from settings import config

class HTTPRouter:

	def __init__(self):
		print(config)

		FileServe()