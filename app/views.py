"""This file contains route definitions and handles requests for these routes."""
import json
from flask import render_template, request, jsonify
from app import app
from time import sleep

from .src.HadoopResultParser import HadoopResultParser

# import importlib.util
# spec = importlib.util.spec_from_file_location(
# 	'app.src.HadoopResultParser',
# 	'/home/xiaolong/development/verteilte-systeme/dayliketoday_clone/app/HadoodResultParser.py'
# )
# HadoodResultParser = importlib.util.module_from_spec(spec)
# spec.loader.exec_module(HadoodResultParser)

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
	'Johannes Reger',
	'Christian Wille'
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

	# with open('app/timeline_json_example.json') as json_data_file:
	# 	print('returning result data')
	# 	return json.load(json_data_file)

	if category == 'persons':
		hadoop_result_parser = HadoopResultParser()

		json_result = None
		with open('app/example_hadoop_result') as opened_file:
			json_result = hadoop_result_parser.parse(opened_file)

	elif category == 'companies':
		print('Getting Companies')

	elif category == 'series':
		print('Getting Series')

	return json_result
