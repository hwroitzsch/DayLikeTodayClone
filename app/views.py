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
	days = [x+1 for x in range(31)]
	months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
	languages = ['English', 'German']
	
	return render_template(
		'content.j2', 
		title=title, 
		authors=authors, 
		months=months, 
		days=days,
		languages=languages
	)