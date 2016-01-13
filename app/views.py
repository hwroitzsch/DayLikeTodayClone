"""This file contains route definitions and handles requests for these routes."""
import json
from flask import render_template, request, jsonify
from . import app
from time import sleep

from .src.HadoopPersonsParser import HadoopPersonsParser
from .src.HadoopCompaniesParser import HadoopCompaniesParser
from .src.HadoopSeriesParser import HadoopSeriesParser
from .src.HDFSFileReader import HDFSFileReader

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
	'Companies',
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
	"""This function handles GET requests for JSON data from DBPedia. The URL contains data, which will be used to query the server."""

	print('Received request!')
	print('year:', year)
	print('month:', month)
	print('day:', day)
	print('language:', language)

	result_data = get_data_from_hadoop('persons', year, month, day, language)
	print('got result data')

	return jsonify(result_data)

@app.route('/companies/<year>/<language>', methods=["GET"])
def what_happened_companies(year, language):
	print('Companies called.')
	return 'not yet implemented'

@app.route('/series/<year>/<language>', methods=["GET"])
def what_happened_series(year, language):
	print('Series called.')
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


	elif category == 'companies':
		print('Getting Companies')
		if language == 'english':
			lines = HDFSFileReader.read('Company_en')
		elif language == 'german':
			lines = HDFSFileReader.read('Company_de')
		else:
			print('Language unknown.')

		parser = HadoopCompaniesParser()
		json_result = parser.parse(lines)

		return jsonify(json_result)

	elif category == 'series':
		print('Getting Series')
		if language == 'english':
			lines = HDFSFileReader.read('Serien_en')
		elif language == 'german':
			lines = HDFSFileReader.read('Serien_de')
		else:
			print('Language unknown.')

		parser = HadoopSeriesParser()
		json_result = parser.parse(lines)

		return jsonify(json_result)
