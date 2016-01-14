__author__ = 'Hans-Werner Roitzsch'

import re
from datetime import datetime

class HadoopPersonsParser:
	def __init__(self):
		#<http://dbpedia.org/resource/Alan_Turing>
		self.url_regex = re.compile(r'^<((http|https|ftp)://)?(www\.)?.*\.([a-zA-Z]{2,3})(:|/|[\w#-])*>$')

		#"1912-06-23"^^<http://www.w3.org/2001/XMLSchema#date>
		self.date_regex = re.compile(r'^"\d{4}-\d{2}-\d{2}"\^\^(<http://www\.w3\.org/2001/XMLSchema\#d.*)$')  # somehow > instead of .* at the end doesn't match
		self.date_year_regex = re.compile(r'^"\d{4}"\^\^(<http://www\.w3\.org/2001/XMLSchema\#gYear.*)$')  # somehow > instead of .* at the end doesn't match

		#"Alan"@de
		self.name_regex = re.compile(r'^"(([A-Z\\\\u0-9][a-z\\\\0-9]*)[- ]{0,1})+"@(de|en)$')

		#<http://dbpedia.org/resource/London>
		self.birth_place_regex = re.compile(r'^<((http|https|ftp)://)?(www\.)?.*\.([a-zA-Z]{2,3})(/|[\w#-])*>$')

		#"britischer Logiker, Mathematiker und Kryptoanalytiker"@de
		self.description_regex = re.compile(r'^".*"@(de|en)$')

		#<http://commons.wikimedia.org/wiki/Special:FilePath/Alan_Turing_cropped.jpg>
		self.image_url_regex = re.compile(r'^<((http|https|ftp)://)?(www\.)?(\w*|\.|\-)*([a-zA-Z]{2,3})(/|:|[\w#-])*\.(png|jpg|jpeg|svg|gif|gifv|bmp)>$')

		self.regex_list = [
			self.url_regex,
			self.date_regex,
			self.date_year_regex,
			self.name_regex,
			self.birth_place_regex,
			self.description_regex,
			self.image_url_regex
		]

	def parse(self, result_data):
		list_of_line_attributes = []
		line_attributes = self.get_initial_line_attributes()  # at first we assume no attributes are present

		for index,line in enumerate(result_data):
			line = line.strip('\n')
			
			# skipp empty lines and comments
			if line.startswith('#'):
				continue
			if line == '':
				continue

			values = line.split('\t')

			for value_index, value in enumerate(values):
				for regex_index, compiled_regex in enumerate(self.regex_list):

					# try to match the regexes
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
							print('SETTING BIRTH DATE FOR PERSON IN LINE', index)
							date = value.split('"')[1]
							line_attributes['birth_date'] = date
							line_attributes['birth_date_year'] = date.split('-')[0]
							line_attributes['birth_date_month'] = date.split('-')[1]
							line_attributes['birth_date_day'] = date.split('-')[2]
							break

						elif compiled_regex == self.date_year_regex and not line_attributes['birth_date']:
							print('SETTING BIRTH DATE ONLY YEAR FOR PERSON IN LINE', index)
							date = value.split('"')[1]
							line_attributes['birth_date'] = date
							line_attributes['birth_date_year'] = date.split('-')[0]
							line_attributes['birth_date_month'] = ''
							line_attributes['birth_date_day'] = ''
							break

						elif compiled_regex == self.date_regex:  # we are checking for the date regex
							date = value.split('"')[1]
							line_attributes['death_date'] = date
							line_attributes['death_date_year'] = date.split('-')[0]
							line_attributes['death_date_month'] = date.split('-')[1]
							line_attributes['death_date_day'] = date.split('-')[2]
							break

						### URL ###
						elif compiled_regex == self.url_regex:
							if not line_attributes['url']:
								line_attributes['url'] = value.strip('<>')
								break

						### FIRST NAME & LAST NAME
						elif compiled_regex == self.name_regex:
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
						elif compiled_regex == self.description_regex:
							if not line_attributes['description']:
								line_attributes['description'] = value.split('"')[1]
								break

						### IMAGE URL ###
						elif compiled_regex == self.image_url_regex:
							if not line_attributes['image_url']:
								line_attributes['image_url'] = value.strip('<>\n')
								break

						else:
							break

			list_of_line_attributes.append(line_attributes)

			line_attributes = self.get_initial_line_attributes()

		return list_of_line_attributes


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

	def build_json(self, list_of_line_attributes):
		json_data = {}

		json_data['events'] = []

		for index, line_attributes in enumerate(list_of_line_attributes):
			one_event = {}

			one_event['media'] = {}

			### URL ###
			one_event['media']['url'] = str(line_attributes['image_url'])
			one_event['media']['caption'] = str(line_attributes['first_name']) + ' ' + str(line_attributes['last_name'])
			one_event['media']['credit'] = 'Wikipedia/<a href=\'' + str(line_attributes['image_url']) + '\'>image_' + str(index) + '</a>'

			### START DATE ###
			one_event['start_date'] = {}
			if line_attributes['birth_date'] and line_attributes['birth_date_year'] and line_attributes['birth_date_month'] and line_attributes['birth_date_day']:
				one_event['start_date']['year'] = line_attributes['birth_date_year']
				one_event['start_date']['month'] = line_attributes['birth_date_month']
				one_event['start_date']['day'] = line_attributes['birth_date_year']
			elif line_attributes['birth_date'] and line_attributes['birth_date_year']:
				one_event['start_date']['year'] = line_attributes['birth_date_year']
			else:
				one_event['start_date']['year'] = '0000'

			### TEXT ###
			one_event['text'] = {}

			text_headline = ''
			if line_attributes['first_name']: text_headline += line_attributes['first_name'] + ' '
			if line_attributes['last_name']: text_headline += line_attributes['last_name'] + '<br>'
			if line_attributes['birth_date_year']: text_headline += line_attributes['birth_date_year'] + ' - '
			if line_attributes['death_date_year']: text_headline += line_attributes['death_date_year']
			one_event['text']['headline'] = text_headline

			one_event['text']['text'] = ''
			if line_attributes['description']: one_event['text']['text'] = line_attributes['description']

			json_data['events'].append(one_event)

		# meta data block
		json_data['title'] = {}
		json_data['title']['media'] = {}
		json_data['title']['media']['url'] = '//de.wikipedia.org/static/images/project-logos/dewiki.png'
		json_data['title']['media']['caption'] = 'people born the same day'
		json_data['title']['media']['credit'] = 'wikipedia/<a href=\'http://www.de.wikipedia.org\'>link_wiki</a>'
		json_data['title']['text'] = {}

		json_data['title']['text']['headline'] = 'People<br/> born in ' + line_attributes['birth_date_year']
		json_data['title']['text']['text'] = '<p>These are people born the same day.</p>'

		return json_data
