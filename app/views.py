"""This file contains route definitions and handles requests for these routes."""
import json
from flask import render_template, request, jsonify
from . import app
from time import sleep

from .src.HadoopPersonsParser import HadoopPersonsParser
from .src.HadoopFoundationsParser import HadoopFoundationsParser
from .src.HadoopSeriesParser import HadoopSeriesParser
from .src.HDFSFileReader import HDFSFileReader
from .src.SeriesFileReader import SeriesFileReader
from .src.FoundationsFileReader import FoundationsFileReader

__author__ = "Hans-Werner Roitzsch"

DAYS = [x+1 for x in range(31)]
MONTHS = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
LANGUAGES = ['English', 'German']
TITLE = 'Hadoop!!!'
AUTHORS = [
	'Hans-Werner Roitzsch',
	'Christian Günther',
	'Christopher Rohrlack',
	'Jonny Leuschner',
	'Johannes Reger'
]
CATEGORIES = [
	'Persons',
	'Foundations',
	'Series'
]

@app.route('/')
@app.route('/index')
def index():
	"""This function handles requests for the landing page. It renders a Jinja2 template and returns the resulting HTML code."""

	return render_template(
		'content.j2',
		title=TITLE,
		authors=AUTHORS,
		categories=CATEGORIES
	)



@app.route('/persons/<year>/<month>/<day>/<language>', methods=["GET"])
def what_happened_persons(year, month, day, language):
	"""this function handles GET requests for JSON data from DBPedia. The URL contains data, which will be used to query the server."""

	print('Received request!')
	print('year:', year)
	print('month:', month)
	print('day:', day)
	print('language:', language)

	result_data = get_data_from_hadoop('persons', year, month, day, language)
	print('got result data')

	return jsonify(result_data)

@app.route('/foundations/<year>/<language>', methods=["GET"])
def what_happened_foundations(year, language):
	print('Foundations called.')

	result_data = get_data_from_hadoop('foundations', year, None, None, language)
	return result_data

@app.route('/series/<year>/<language>', methods=["GET"])
def what_happened_series(year, language):
	print('Series called.')
	result_data = get_data_from_hadoop('series', year, None, None, language)
	return result_data
	return 'not yet implemented'


def get_data_from_hadoop(category, year, month, day, language):
	"""This function takes care of building a query from its parameters."""

	print('getting data from Hadoop ...')
	sleep(1.5)  # TODO: Remove this in production code!

	if category == 'persons':
		print('Getting persons.')
		if language == 'english':
			lines = HDFSFileReader.read('Persons_en')
		elif language == 'german':
			lines = HDFSFileReader.read('Persons_de')
		else:
			print('Language unknown.')

		parser = HadoopPersonsParser()
		return parser.parse(lines)


	elif category == 'foundations':
		file_reader = FoundationsFileReader()
		print('Getting Foundations')
		if language == 'english':
			lines = file_reader.read('/home/hadoop/PigSPARQL_v2.0/dist/Data_prep/Foundations_en')
		elif language == 'german':
			lines = file_reader.read('/home/hadoop/PigSPARQL_v2.0/dist/Data_prep/Foundations_de')
		else:
			print('Language unknown.')

		#parser = HadoopFoundationsParser()
		#result = parser.parse(lines)  # returns a dictionary

		#return jsonify(result)
		lines_attributes = [attr for attr in lines_attributes if attr['start_date_year'] == year]
		result = jsonify(result=lines_attributes)
		#print(lines_attributes)
		#print(result)
		return jsonify(result=lines_attributes)


	elif category == 'series':
		file_reader = SeriesFileReader()
		print('Getting Series')
		if language == 'english':
			lines_attributes = file_reader.read('/home/hadoop/PigSPARQL_v2.0/dist/Data_prep/Serien_en')
			#lines = HDFSFileReader.read('Series_en')
		elif language == 'german': # TODO
			lines_attributes = file_reader.read('/home/hadoop/PigSPARQL_v2.0/dist/Data_prep/Serien_de')
			#lines = HDFSFileReader.read('Series_de')
		else:
			print('Language unknown.')

		#parser = HadoopSeriesParser()
		#json_result = parser.parse(lines)
		#json_result = [elem for elem in json_result if elem['foundation_date_year'] == year]  # only return the ones of the year specified by the user

		#return jsonify(json_result)
		lines_attributes = [attr for attr in lines_attributes if attr['start_date_year'] == year]
		result = jsonify(result=lines_attributes)
		#print(lines_attributes)
		#print(result)
		return jsonify(result=lines_attributes)

