__author__ = 'Hans-Werner Roitzsch'


class HadoopResultParser:
	def __init__(self):
		pass

	def parse(self, result_data):
		for index,line in enumerate(result_data):
			print('Result#', index, ':\n', line, '\n\n', sep='')
			values = line.split('\t')

			url = values[0].strip('<>')

			birth_date = values[1].split('"')[1]
			birth_date_year = birth_date.split('-')[0]
			birth_date_month = birth_date.split('-')[1]
			birth_date_day = birth_date.split('-')[2]

			last_name = values[2].split('"')[1]

			first_name = values[3].split('"')[1]

			birth_place_parts = values[4].strip('<>').split('/')
			birth_place = birth_place_parts[-1]

			death_date = values[5].split('"')[1]
			death_date_year = death_date.split('-')[0]
			death_date_month = death_date.split('-')[1]
			death_date_day = death_date.split('-')[2]

			description = values[6].split('"')[1]

			image_url = values[7].strip('<>\n')

			print('url:', url)
			print('birth_date:', birth_date)
			print('birth_date_year:', birth_date_year)
			print('birth_date_month:', birth_date_month)
			print('birth_date_day:', birth_date_day)
			print('last_name:', last_name)
			print('first_name:', first_name)
			print('birth_place:', birth_place)
			print('death_date:', death_date)
			print('death_date_year:', death_date_year)
			print('death_date_month:', death_date_month)
			print('death_date_day:', death_date_day)
			print('description:', description)
			print('image_url:', image_url)


			#<http://dbpedia.org/resource/Alan_Turing>	"1912-06-23"^^<http://www.w3.org/2001/XMLSchema#date>	"Turing"@de	"Alan"@de	<http://dbpedia.org/resource/London>	"1954-06-07"^^<http://www.w3.org/2001/XMLSchema#date>	"britischer Logiker, Mathematiker und Kryptoanalytiker"@de	<http://commons.wikimedia.org/wiki/Special:FilePath/Alan_Turing_cropped.jpg>

	def determin_line_type(self, line):
		pass
