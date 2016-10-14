import re
import sys
from bs4 import BeautifulSoup
import datetime
#from app import readUrl
reload(sys)
sys.setdefaultencoding('utf-8')
from my_api import readUrl, striphtml
from pymongo import MongoClient
import random
import time
#===========================================================================================================
#
#===========================================================================================================
def addAddress(address):
    client = MongoClient()
    db = client.sher
    db.shop_address.update({"shop" : address},{"shop" : address, "dateAdded" : datetime.datetime.utcnow()}, upsert=True)

def findLinks():
    client = MongoClient()
    db = client.sher
    dump = db.address_links.find({ "crawling.status": { "$exists": False } })
    links = []
    for link in dump:
        links.append(link)
    return list(links)
#============================================================================================================
#
#============================================================================================================
def parseShop(url):
    data = readUrl(url)
    soup = BeautifulSoup(data, 'html.parser')
    store = {}
    store['store_name'] = soup.h1.string
    store['short_location'] = soup.find("span", { "class" : "muted" }).string
    details = soup.find_all("div", { "class" : "profile-details" })
    address = ""
    try:
        for addr in details[1].div.address.find_all('span'):
            addr = addr.text.replace(",", "")
            address += ", %s" % str(addr)
            if "," in address[0]:
                address = str(address[2:])
        store['address'] = str(address)
    except:
        pass
    for ch in details:
        try:
            if ch.div.string == None:
	        continue
	    store[ch.strong.string] = ch.div.string
        except:
    	    pass
    return store
#============================================================================================================
#
#=============================================================================================================

links = findLinks()

print links


for link in links:
    addAddress(parseShop(link['url']))
#     print link['url']
    client = MongoClient()
    db = client.sher
    db.address_links.update({"_id" : link['_id']}, {"$set" : {"crawling" : {"status" : "Done", "date" : datetime.datetime.utcnow()}}})
    print "Done : %s " % link['url']
    time.sleep(random.randint(0,20))













