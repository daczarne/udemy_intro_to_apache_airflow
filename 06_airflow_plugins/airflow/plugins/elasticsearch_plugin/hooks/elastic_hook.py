from airflow.hooks.base import BaseHook
from elasticsearch import Elasticsearch

class ElasticHook(BaseHook):

	#* Initialize the hook
	def __init__(self, conn_id = 'elasticsearch_default', *args, **kwargs):
		super().__init__(*args, **kwargs)
		conn = self.get_connection(conn_id)
		
		conn_config = {}
		hosts = []

		if conn.host:
			hosts = conn.host.split(',')
		if conn.port:
			conn_config['port'] = int(conn.port)
		if conn.login:
			conn_config['http_auth'] = (conn.login, conn.password)

		self.es = Elasticsearch(hosts, **conn_config)
		self.index = conn.schema

	#* Get information about the Elasticsearch instance
	def info(self):
		return self.es.info()

	#* Define the index
	def set_index(self, index):
		self.index = index

	#* Add document to the index
	def add_doc(self, index, doc_type, doc):
		self.set_index(index)
		res = self.es.index(index = index, doc_type = doc_type, body = doc)
		return res
