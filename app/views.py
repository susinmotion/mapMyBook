# from CONTAINING FOLDER OF RUN.PY import MODULE NAMED BELOW
from app import app
from flask import render_template, url_for, request
import pygeocoder
from pygeocoder import Geocoder
import requests
import googlemaps

import requests, re
import cPickle as pickle
from bs4 import BeautifulSoup
the_libraries=pickle.load(open("dictionary.p","rb"))


def find_link_to_copies(keyword):
	url="http://nypl.bibliocommons.com/search?utf8=%13&t=smart&search_category=keyword&q="+\
	 keyword+"&commit=Search&searchOpt=catalogue&formats=PAPERBACK|BK"
	pretty_source_code=get_source(url)
	link_section=pretty_source_code.find(id=re.compile("circ_info_trigger_"))
	items_link=link_section.attrs["href"]
	base="http://nypl.bibliocommons.com"
	return base+items_link


def get_source (url):
	r=requests.get(url)
	source_code=r.content
	pretty_source_code=BeautifulSoup(source_code)
	return pretty_source_code

def places_available(link):
	content=get_source(link)
	table=content.find("table")
	places=table.find_all(testid="item_branch_name")
	places_av=[]
	for place in places:
		libName=str(place.text).strip().replace("'", "")
		if libName.endswith(")"):
			libName=libName[:-5]
		if libName in the_libraries:
			places_av.append([libName, the_libraries[libName].latLng[0], the_libraries[libName].latLng[1], the_libraries[libName].address[:-1]])	
	#for i in range(len(places)):
	#	places_av.append(places[i].text)
	return places_av

@app.route('/', methods=['GET','POST'])
#@app.route('/start', methods=['GET','POST'])
#@app.route('/start/<location>', methods=['GET','POST'])
#these include the data itself that could be part of the view. The html page controls how it looks and what gets shown

def index():

	if request.method=="GET":
		return render_template ("start.html")
	else:
		keyword=request.form.get('keyword')
		return (map(keyword))


@app.route('/map')

def map(keyword):
	api_key=open('api_key').read()
	url="https://maps.googleapis.com/maps/api/js?key=%s"%api_key
	
	return render_template("libMap.html", libraries=places_available(find_link_to_copies(keyword)), url=url)
#these include the data itself that could be part of the view. The html page controls how it looks and what gets shown
#def THE NAME OF THE THING AFTER THE SLASH--different page views
