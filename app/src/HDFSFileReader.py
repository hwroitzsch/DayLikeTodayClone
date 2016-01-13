__author__ = 'Hans-Werner Roitzsch'

from hdfs import Config

class HDFSFileReader:
	"""This class represents a reader for accessing files in a HDFS."""

	def __init__(self):
		pass

	@classmethod
	def read(cls, file_path):
		lines = []

		try:
			client = Config().get_client('dev')

			with client.read(file_path, encoding='utf-8', delimiter='\n') as reader:
				for line in reader:
					lines.append(line)  # eventuell unnoetig, kann man auch reader zurueckgeben?
		except:
			print("ERROR: Could not read from HDFS.")
			raise

		return lines
