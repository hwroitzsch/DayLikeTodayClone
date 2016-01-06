__author__ = 'Hans-Werner Roitzsch'


import re


class HadoopResultParser:
	def __init__(self):
		#<http://dbpedia.org/resource/Alan_Turing>
		self.url_regex = re.compile(r'^<((http|https|ftp)://)?(www\.)?.*\.([a-zA-Z]{2,3})(:|/|[\w#-])*>$')

		#"1912-06-23"^^<http://www.w3.org/2001/XMLSchema#date>
		self.date_regex = re.compile(r'^"\d{4}-\d{2}-\d{2}"\^\^(<http://www\.w3\.org/2001/XMLSchema\#d.*)$')  # somehow > instead of .* at the end doesn't match

		#"Alan"@de
		self.name_regex = re.compile(r'^"([a-zA-Z]*)"@(de|en)$')

		#<http://dbpedia.org/resource/London>
		self.birth_place_regex = re.compile(r'^<((http|https|ftp)://)?(www\.)?.*\.([a-zA-Z]{2,3})(/|[\w#-])*>$')

		#"britischer Logiker, Mathematiker und Kryptoanalytiker"@de
		self.description_regex = re.compile(r'"(\w*| |,|\.|;|:|\-)*"@(de|en)')

		#<http://commons.wikimedia.org/wiki/Special:FilePath/Alan_Turing_cropped.jpg>
		self.image_url_regex = re.compile(r'^<((http|https|ftp)://)?(www\.)?(\w*|\.|\-)*([a-zA-Z]{2,3})(/|:|[\w#-])*\.(png|jpg|jpeg|svg|gif|gifv|bmp)>$')

		self.regex_list = [
			self.url_regex,
			self.date_regex,
			self.name_regex,
			self.birth_place_regex,
			self.description_regex,
			self.image_url_regex
		]

	def parse(self, result_data):
		line_attributes = self.get_initial_line_attributes()  # at first we assume no attributes are present

		for index,line in enumerate(result_data):
			line = line.strip('\n')
			# skipp empty lines and comments
			print('===LINE:', index+1, '===', line)
			if line.startswith('#'):
				print('SKIPPING (comment line)')
				continue
			if line == '':
				print('SKIPPING (line empty)')
				continue

			values = line.split('\t')


			for value_index, value in enumerate(values):
				for regex_index, compiled_regex in enumerate(self.regex_list):
					# try to match the regex
					regex_match = compiled_regex.match(value)


					if regex_match:
						### BIRTH DATE & DEATH DATE ###
						# the following if statement checks which date we got, birth date or death date
						if (
							not line_attributes['birth_date'] and  # we have not found a birth date yet
							not line_attributes['first_name'] and  # we have not found a first name, which would separate birth date and death date
							not line_attributes['last_name'] and  # we have not found a last name, which would separate birth date and death date
							compiled_regex == self.date_regex  # we are checking for the date regex
						):
							date = value.split('"')[1]
							line_attributes['birth_date'] = date
							line_attributes['birth_date_year'] = date.split('-')[0]
							line_attributes['birth_date_month'] = date.split('-')[1]
							line_attributes['birth_date_day'] = date.split('-')[2]
							break

						elif compiled_regex == self.date_regex:  # we are checking for the date regex
							date = value.split('"')[1]
							line_attributes['death_date'] = date
							line_attributes['death_date_year'] = date.split('-')[0]
							line_attributes['death_date_month'] = date.split('-')[1]
							line_attributes['death_date_day'] = date.split('-')[2]
							break

						### URL ###
						if compiled_regex == self.url_regex:
							if not line_attributes['url']:
								line_attributes['url'] = value.strip('<>')
								break

						### FIRST NAME & LAST NAME
						if compiled_regex == self.name_regex:
							if not line_attributes['last_name']:
								# if there is only one match, we assume it to be the last name
								line_attributes['last_name'] = value.split('"')[1]
								break
							else:
								line_attributes['first_name'] = value.split('"')[1]
								break

						### BIRTH PLACE ###
						# the regexes for url and birthplace are equal, but we assume, that there will always be a URL
						if compiled_regex == self.birth_place_regex:
							if not line_attributes['birth_place']:
								birth_place_parts = value.strip('<>').split('/')
								birth_place = birth_place_parts[-1]
								line_attributes['birth_place'] = birth_place
								break

						### DESCRIPTION ###
						if compiled_regex == self.description_regex:
							if not line_attributes['description']:
								line_attributes['description'] = value.split('"')[1]
								break

						### IMAGE URL ###
						if compiled_regex == self.image_url_regex:
							print('===IMAGE URL FOUND===')
							if not line_attributes['image_url']:
								line_attributes['image_url'] = value.strip('<>\n')
								break

			#<http://dbpedia.org/resource/Alan_Turing>	"1912-06-23"^^<http://www.w3.org/2001/XMLSchema#date>	"Turing"@de	"Alan"@de	<http://dbpedia.org/resource/London>	"1954-06-07"^^<http://www.w3.org/2001/XMLSchema#date>	"britischer Logiker, Mathematiker und Kryptoanalytiker"@de	<http://commons.wikimedia.org/wiki/Special:FilePath/Alan_Turing_cropped.jpg>

			print('====================\nATTRIBUTES OF LINE:')
			print('url:', line_attributes['url'])
			print('birth_date:', line_attributes['birth_date'])
			print('birth_date_year:', line_attributes['birth_date_year'])
			print('birth_date_month:', line_attributes['birth_date_month'])
			print('birth_date_day:', line_attributes['birth_date_day'])
			print('last_name:', line_attributes['last_name'])
			print('first_name:', line_attributes['first_name'])
			print('birth_place:', line_attributes['birth_place'])
			print('death_date:', line_attributes['death_date'])
			print('death_date_year:', line_attributes['death_date_year'])
			print('death_date_month:', line_attributes['death_date_month'])
			print('death_date_day:', line_attributes['death_date_day'])
			print('description:', line_attributes['description'])
			print('image_url:', line_attributes['image_url'])

			line_attributes = self.get_initial_line_attributes()


	def get_initial_line_attributes(self):
		return {
			'url': False,

			'birth_date': False,
			'birth_date_year': False,
			'birth_date_month': False,
			'birth_date_day': False,

			'last_name': False,

			'first_name': False,

			'birth_place': False,

			'death_date': False,
			'death_date_year': False,
			'death_date_month': False,
			'death_date_day': False,

			'description': False,

			'image_url': False
		}

	def determin_line_type(self, line):
		pass
