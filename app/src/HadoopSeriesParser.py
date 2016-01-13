import re
from datetime import datetime

class HadoopSeriesParser:
	def __init__(self):
		self.attribute_count = 5

	def parse(self, result_data):
		lines_attributes = []

		for line in result_data:
			line_parts = line.split('\t', -1)
			if len(line_parts) == self.attribute_count:
				lines_attributes.append({
					'name': line_parts[0],
					'episode_count': line_parts[1],
					'producer': line_parts[2],
					'summary': line_parts[3],
					'image_url': line_parts[4],
				})
			else:
				pass  # ignore the incomplete lines

		return build_json(lines_attributes)

	def build_json(self, result):
		for line_attributes in lines_attributes:
			pass  # TODO!!!
