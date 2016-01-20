import unittest
from flask import json
from pospax import app

class BaseTest(unittest.TestCase):

	def setUp(self):
		print 'test started'
		self.client = app.test_client()

	def tearDown(self):
		print 'test finished'

	def dumps(self, data):
		return json.dumps(data)

	def loads(self, data):
		return json.loads(data)
