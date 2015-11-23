import json
from flask import render_template, request
from app import app

days = [x+1 for x in range(31)]
months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
languages = ['English', 'German']

@app.route('/')
@app.route('/index')
def index():
	authors = [
		'Hans-Werner Roitzsch',
		'Christian Günther',
		'Christopher Rohrlack',
		'Jonny Leuschner',
		'Johannes Reger',
		'Christian Wille'
	]
	title = 'Hadoop!!!'
	
	return render_template(
		'content.j2', 
		title=title, 
		authors=authors, 
		months=months, 
		days=days,
		languages=languages
	)

@app.route('/what_happened/<month>/<day>/<language>', methods=["GET"])
def what_happened(month, day, language):
	print('Received request!')

	print('day:', month)
	print('month:', day)
	print('language:', language)

	result_data = get_data_from_hadoop(month, day, language)
	return json.dumps(result_data)

def get_data_from_hadoop(month, day, language):
	# TODO
	with open('app/static/json/minimal_example.json') as json_data_file:
		return json.load(json_data_file)
	pass

