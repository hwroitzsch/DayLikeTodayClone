from flask import render_template
from app import app

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
	return(render_template('base.j2', title=title, authors=authors))

@app.route('/date')
def specific_date():
	return render_template('content.j2')