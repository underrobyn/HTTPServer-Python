import os
from utils import *
from settings import config

class FileServe:

	def __init__(self, http_docs = 'www'):
		self.http_docs = http_docs


	def load_file_content(self, file):
		with open(file, "r") as data_file:
			print(data_file.read())