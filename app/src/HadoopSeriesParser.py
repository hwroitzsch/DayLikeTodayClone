import re
from datetime import datetime

class HadoopSeriesParser:
	def __init__(self):
		self.attribute_count = 8
		self.foundation_date_regex = r'^([^\t]*\t){1}"\d{4}"\^\^<http://www.w3.org/2001/XMLSchema#date>.*$'

	def parse(self, result_data):
		lines_attributes = []

		### Structure
		# <http://dbpedia.org/resource/Axel!>
		# "2002-09-21"^^<http://www.w3.org/2001/XMLSchema#date>
		# "Axel!"@de
		# "35"^^<http://www.w3.org/2001/XMLSchema#nonNegativeInteger>
		# (Produzent) BSP: <http://dbpedia.org/resource/Tina_Fey>
		# (Bild) BSP: <http://commons.wikimedia.org/wiki/Special:FilePath/Ty_Pennington.jpg>
		# (???)
		# "Axel! ist eine deutsche Comedy-Serie mit Axel Stein in der Titelrolle, in der witzige Episoden aus dem Leben der Figur Axel und seiner Freunde gezeigt werden. Die Serie wurde auf Sat.1 ausgestrahlt. Als Fortsetzung entstand eine weitere Serie mit dem Namen Axel! will\u2019s wissen."@de


		for line in result_data:
			if re.match(self.foundation_date_regex, line):
				line_parts = line.split('\t', -1)
				if len(line_parts) == self.attribute_count:

					url = line_parts[0].strip('<>')

					foundation_date = line_parts[1].split('"', -1)
					foundation_date_parts = foundation_date.split('-', -1)
					foundation_date_year = foundation_date_parts[0]
					foundation_date_month = foundation_date_parts[1]
					foundation_date_day = foundation_date_parts[2]

					name = line_parts[2].split('"', -1)[1]

					episode_count = line_parts[3].split('"', -1)[1]

					producer_url = line_parts[4].split('<>', -1)[1]

					image_url = line_parts[5].split('<>', -1)[1]

					summary = line_parts[7].split('"', -1)[1]

					lines_attributes.append({
						'url': url,
						'foundation_date': foundation_date,
						'foundation_date_year': foundation_date_year,
						'foundation_date_month': foundation_date_month,
						'foundation_date_day': foundation_date_day,
						'name': name,
						'episode_count': episode_count,
						'producer_url': producer_url,
						'image_url': image_url,
						'summary': summary
					})
				else:
					pass  # ignore the incomplete lines

		return line_attributes
