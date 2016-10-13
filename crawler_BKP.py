from bs4 import BeautifulSoup
import urllib2
import re
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
#============================================================================================================

def readUrl(url):
	response = urllib2.urlopen(url)
	html = response.read()
	return html

def striphtml(data):
    p = re.compile(r'<.*?>')
    return p.sub('', data)

data = readUrl('http://yellowpages.sulekha.com/mumbai/ambika-book-depot-kandivali-east-mumbai_contact-address')
soup = BeautifulSoup(data, 'html.parser')

store = {}

store['store_name'] = soup.h1.string
store['short_location'] = soup.find("span", { "class" : "muted" }).string

#streetAddress = find(itemprop="streetAddress").string


#soup.find("span", { "class" : "muted" }).string
details = soup.find_all("div", { "class" : "profile-details" })
address = ""
for addr in details[1].div.address.find_all('span'):
    address += ", %s" % addr.text.replace(",", "")
    address = address[2:]
store['address'] = str(address)

for ch in details:
    #'<span itemprop="streetAddress">No. 3/453</span>'
    #print(ch.find(itemprop="streetAddress").string)
    try:
        if ch.div.string == None:
	    continue
	store[ch.strong.string] = ch.div.string
    #print ch.div.text
        #print "%s : %s" % (ch.strong.string, ch.div)
    	#print ch.find(itemprop="streetAddress").next_sibling.string
    	#print ch.find(itemprop="streetAddress").next_sibling.next_sibling.string
    	#print ch.find(itemprop="streetAddress").next_sibling.next_sibling.string
    except:
    	pass
    #print re.sub('<[^>]*>', '', str(ch.div.div.find('address')))
print store

#print(store)
