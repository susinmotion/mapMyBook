# from CONTAINING FOLDER OF RUN.PY import MODULE NAMED BELOW
from app import app
from flask import render_template, url_for, request, redirect
import pygeocoder
from pygeocoder import Geocoder
import requests
import googlemaps
from api import get_source, find_link_to_copies, check_spelling, check_availability,places_available, title_url



@app.route('/', methods=['GET','POST'])
#@app.route('/start', methods=['GET','POST'])
#@app.route('/start/<location>', methods=['GET','POST'])
#these include the data itself that could be part of the view. The html page controls how it looks and what gets shown

def index():

	if request.method=="GET":
		return render_template ("start.html")
	else:
		title=request.form.get('title')
		return  redirect(url_for("map",title=title))


@app.route('/map/<title>', methods=['GET','POST'])

def map(title):
	api_key=open('api_key').read()
	url="https://maps.googleapis.com/maps/api/js?key=%s"%api_key
	source=get_source(title_url(title))
	alt= (check_spelling(source, url))
	#if alt=="no books":
	#	return redirect(url_for("nobooks", title=title))
	if alt:
		return redirect(url_for("alt",alt=alt))

	page_w_books=get_source(find_link_to_copies(source))
	if request.method=='GET':
		if check_availability(page_w_books)==False:
			return redirect(url_for("checkedOut", title=title))
	libraries=places_available(page_w_books)[0]
	fulltitle= libraries.pop()
	return render_template("libMap.html", libraries=libraries, url=url, fulltitle=fulltitle)

@app.route('/didyoumean/<alt>')

def alt(alt):
	return render_template ("didyoumean.html",alt=alt)

@app.route('/checkedOut/<title>')
def checkedOut(title):
	return render_template("noneFound.html", title=title)

@app.route('/noBooks/<title>')
def noBooks(title):
	return render_template("nobooks.html", title=title)

#these include the data itself that could be part of the view. The html page controls how it looks and what gets shown
#def THE NAME OF THE THING AFTER THE SLASH--different page views
