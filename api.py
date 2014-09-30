import requests, re
import cPickle as pickle
from bs4 import BeautifulSoup

the_libraries=pickle.load(open("dictionary.p","rb"))


def get_source (url):
	#get the source code for a particular link
	r=requests.get(url)
	source_code=r.content
	pretty_source_code=BeautifulSoup(source_code)
	return pretty_source_code

def keyword_url(keyword):
	#retur url for keyword search
	url="http://nypl.bibliocommons.com/search?utf8=%13&t=smart&search_category=keyword&q="+\
	 keyword+"&commit=Search&searchOpt=catalogue&formats=PAPERBACK|BK"
	return url

def find_link_to_copies(source_code):

	#find the link to availability on that page
	link_section=source_code.find(id=re.compile("circ_info_trigger_"))
	items_link=link_section.attrs["href"]
	base="http://nypl.bibliocommons.com"

	return base+items_link

def check_spelling(source_code):
	#check to see if there are books by that name, and return any alternate spellings
	chunk=source_code.findAll(testid="link_didyoumean")
	if chunk:
		alt= str(chunk[0].text).split[0]
		return alt
	return None



def places_available(content):
	
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
	return [places_av]

def check_availability(content):
	if str(content.findAll("h1")[1].text[:3])=="Not":
		return False
	return True
