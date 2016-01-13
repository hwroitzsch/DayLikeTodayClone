__author__ = 'Hans-Werner Roitzsch'


class SeriesFileReader:
	def __init__(self):
		self.attribute_count = 8

	def read(self, file_path):
		lines = []
		lines_attributes = []

		with open(file_path) as opened_file:
			for index, line in enumerate(opened_file):
				if True:
					line_parts = line.split('\t', -1)
					line_parts = [elem.strip('\n') for elem in line_parts]
					# print(line_parts)
					if len(line_parts) == self.attribute_count:
						line_attributes = {}

						line_attributes['url'] = ''
						line_attributes['start_date'] = ''
						line_attributes['start_date_year'] = ''
						line_attributes['start_date_month'] = ''
						line_attributes['start_date_day'] = ''
						line_attributes['name'] = ''
						line_attributes['episode_count'] = ''
						line_attributes['producer_url'] = ''
						line_attributes['image_url'] = ''
						line_attributes['summary'] = ''
						
						if line_parts[0] != '':
							line_attributes['url'] = line_parts[0].strip('<>')
						if line_parts[1] != '':
							line_attributes['start_date'] = line_parts[1].split('"', -1)[1]
							start_date_parts = line_attributes['start_date'].split('-', -1)
							line_attributes['start_date_year'] = start_date_parts[0]
							line_attributes['start_date_month'] = start_date_parts[1]
							line_attributes['start_date_day'] = start_date_parts[2]
						if line_parts[2] != '':
							line_attributes['name'] = line_parts[2].split('"', -1)[1]
						if line_parts[3] != '':
							line_attributes['episode_count'] = line_parts[3].split('"', -1)[1]
						if line_parts[4] != '':
							line_attributes['producer_url'] = line_parts[4].strip('<>')
						if line_parts[6] != '':
							line_attributes['image_url'] = line_parts[6].strip('<>')
						if line_parts[7] != '':
							# print('PART #', index, ': ',  line_parts[7], sep='')
							line_attributes['summary'] = line_parts[7].split('"', -1)[1]
						lines_attributes.append(line_attributes)
					else:
						pass  # ignore the incomplete lines
		return lines_attributes
