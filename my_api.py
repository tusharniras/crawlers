import urllib2
from bs4 import BeautifulSoup

def readUrl(url):
    try:
        f = urllib2.urlopen(url)
    except:
        return 1
    return f.read()
#===========================================================================
#
#===========================================================================
def striphtml(data):
    p = re.compile(r'<.*?>')
    return p.sub('', data)
