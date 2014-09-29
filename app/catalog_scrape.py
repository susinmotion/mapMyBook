import requests, re
import cPickle as pickle
from bs4 import BeautifulSoup
from libraries import Library
the_libraries=pickle.load(open("dictionary.p","rb"))

def user_search():
	#this will get search terms from the user, hopefully from a webpage
	keyword="mockingjay"
	return keyword

def find_link_to_copies():
	keyword=user_search()
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
			places_av.append({libName:the_libraries[libName].latLng})	
	#for i in range(len(places)):
	#	places_av.append(places[i].text)
	return places_av


places_available(find_link_to_copies())
#print libraries
