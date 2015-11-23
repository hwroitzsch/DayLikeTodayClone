import json
from flask import render_template, request, jsonify
from app import app

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

@app.route('/')
@app.route('/index')
def index():
	return render_template(
		'content.j2', 
		title=TITLE, 
		authors=AUTHORS, 
		months=MONTHS, 
		days=DAYS,
		languages=LANGUAGES
	)

@app.route('/what_happened/<month>/<day>/<language>', methods=["GET"])
def what_happened(month, day, language):
	print('Received request!')
	print('day:', month)
	print('month:', day)
	print('language:', language)

	result_data = get_data_from_hadoop(month, day, language)
	print('got result data')
	return jsonify(result_data)

def get_data_from_hadoop(month, day, language):
	# TODO
	print('getting data from Hadoop ...')
	
	#with open('app/static/json/minimal_example.json') as json_data_file:
	with open('app/timeline_json_example.json') as json_data_file:
		print('returning result data')
		return json.load(json_data_file)
		#resp = Response(
			#response=json.load(json_data_file),
			#status=200, 
			#mimetype="application/json"
		#)
		#return(resp)
	#pass

