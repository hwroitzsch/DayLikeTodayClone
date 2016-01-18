import re
from datetime import datetime

class HadoopPersonsParser:
	def __init__(self):
		self.attribute_count = 8

	def parse(self, result_data):
		lines_attributes = []

		for line in result_data:
			line_parts = line.split('\t', -1)
			if len(line_parts) == self.attribute_count:
				line_attributes = {}
				if line_parts[0]:
					line_attributes['url'] = line_parts[0].strip('<>')
				if line_parts[1]:
					line_attributes['persons_date'] = line_parts[1].split('"', -1)[1]
					persons_date_parts = line_attributes['persons_date'].split('-', -1)
					line_attributes['birth_date_year'] = persons_date_parts[0]
					line_attributes['birth_date_month'] = ""
					line_attributes['birth_date_day'] = ""
					if len(persons_date_parts)==3:
						line_attributes['birth_date_month'] = persons_date_parts[1]
						line_attributes['birth_date_day'] = persons_date_parts[2]
				if line_parts[2]:
					line_attributes['surname'] = line_parts[2].split('"', -1)[1]
				if line_parts[3]:
					line_attributes['name'] = line_parts[3].split('"', -1)[1]
				if line_parts[4]:
					line_attributes['birthplace'] = line_parts[4].split('/', -1)[4]
				if line_parts[5]:
					line_attributes['deathdate'] = line_parts[5].split('"', -1)[1]
				if line_parts[6]:
					line_attributes['description'] = line_parts[6].split('"', -1)[1]
				if line_parts[7]:
					line_attributes['image_url'] = line_parts[7].strip('<>')
				
				lines_attributes.append(line_attributes)
			else:
				pass  # ignore the incomplete lines
		return lines_attributes
