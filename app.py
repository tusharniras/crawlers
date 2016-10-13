from bs4 import BeautifulSoup
import urllib2
import time
from pymongo import MongoClient
import datetime
import random
#from my_api import readUrl
#===============================================================================
# This Function is to read url and generate HTML Output for bs4.
#===============================================================================
HOST='http://yellowpages.sulekha.com'
def readUrl(url):
    try:
        f = urllib2.urlopen(url)
    except:
	return 1
    return f.read()

#=====================================================================================
# This Function is to add recods (links) into MongoDB Database. (sher.address_links) 
#=====================================================================================
def add_to_database(link, host):
    client = MongoClient()
    db = client.sher
    db.address_links.update({"url": link}, {"url" : link, "host": host, "dateAdded" : datetime.datetime.utcnow()}, upsert=True)

#===============================================================================
#data = readUrl('http://yellowpages.sulekha.com/book-shops_mumbai_1')
#soup = BeautifulSoup(data, "html.parser")
#address_links = soup.findAll("a", { "class" : "GAQ_C_BUSL" })

#====================================================================================
# This function is to find all this links from provided HTML Document/String
#====================================================================================
def link_finder(data):
            address_links = data.findAll("a", { "class" : "GAQ_C_BUSL" })
            for link in address_links:
                    address_link = "%s%s" % (HOST, link['href'])
                    add_to_database(address_link, "Sulekha")
                    print "Added: {%s}" % address_link 
                    time.sleep(random.randint(0,20))
            try:
                next_link = data.find("li", { "class" : "next" })
                next_link = next_link.find('a')['href']
                next_link_full = "%s%s" % (HOST, next_link)
                return next_link_full
            except:
                return 1
#====================================================================================
# This Funtion finds 'a' tags from the HTML and add records to the MongoDB 
#====================================================================================
def all_work(base_url):
    data1 = readUrl(base_url)
    soup = BeautifulSoup(data1, "html.parser")
    next_link = link_finder(soup)
    while (next_link != 1):
        data1 = readUrl(next_link)
        soup = BeautifulSoup(data1, "html.parser")
        next_link = link_finder(soup)
#====================================================================================
# Execute Main Function : Crawler
#====================================================================================
all_work('http://yellowpages.sulekha.com/book-shops_mumbai_1')


