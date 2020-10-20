import re
from urllib.parse import unquote
from urllib.request import urlopen

from bs4 import BeautifulSoup


# Text Processing for enforcing encodings
def cleanupLatinEncoding(word):
    try:
        return unquote(word, errors='strict')
    except UnicodeDecodeError:
        return unquote(word, encoding='latin-1')
        

def getLinks(url):
	# Append the url tag to wiki
	html = urlopen("https://en.wikipedia.org" + url)
	bsObj = BeautifulSoup(html, "lxml")
	newLinks = list()
	# The url tags are always i) found in bodycontent tag
	for each in bsObj.findAll("div", {"id": "bodyContent"}):
		for link in bsObj.findAll("a", href=re.compile("^(/wiki/)((?!:).)*$")):
			if 'href' in link.attrs:
				stripped = re.sub('/wiki/', "", link.attrs['href'])
				stripped = re.sub('_', " ", stripped)
				stripped = cleanupLatinEncoding(stripped)
				newLinks.append(stripped)
	return newLinks