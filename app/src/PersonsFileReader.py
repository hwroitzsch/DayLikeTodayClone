__author__ = 'Hans-Werner Roitzsch'


class PersonsFileReader:
	def __init__(self):
		self.attribute_count = 8

	def read(self, file_path):
		lines = []
		lines_attributes = []

		with open(file_path) as opened_file:
			lines = []
			for line in opened_file:
				lines.append(line)
		return lines
