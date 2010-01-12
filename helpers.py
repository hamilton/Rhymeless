import re
import htmlentitydefs
import urllib2
import simplejson
import helpers
from time import sleep
from random import randint

##
# Removes HTML or XML character references and entities from a text string.
#
# @param text The HTML (or XML) source text.
# @return The plain text, as a Unicode string, if necessary.

def unescape(text):
    def fixup(m):
        text = m.group(0)
        if text[:2] == "&#":
            # character reference
            try:
                if text[:3] == "&#x":
                    return unichr(int(text[3:-1], 16))
                else:
                    return unichr(int(text[2:-1]))
            except ValueError:
                pass
        else:
            # named entity
            try:
                text = unichr(htmlentitydefs.name2codepoint[text[1:-1]])
            except KeyError:
                pass
        return text # leave as is
    return re.sub("&#?\w+;", fixup, text)


class Search(object):
	def __init__(self):
		self.last_query = None
	
	
	def _single_search(self, query=None, results=None, pages=1):
		"""
		hidden search function that does the real bulk.  I.e. - makes the query.
		
		For some reason, next_page doesn't seem to work.
		"""
		if query != None and results != None:
			url = "http://search.twitter.com/search.json?q=%s&rpp=%s&page=%s" % (query, results, pages)
		else:
			raise ValueError, "no specified query (values %s)" % (query)
		response = urllib2.urlopen(url)
		json = simplejson.loads(response.read())
		#next_page = json['next_page']
		#print next_page == next_query
		json = json['results']
		
		return json
	
	
	def search(self, query, results=500):
		"""
		search function.  Set query, and results (result count).
		Also caches the function, as self_query.
		"""
		result_set = []
		if results <=100:
			json = self._single_search(query=query, results=results)
			result_set.extend(json)
		else:
			queries_to_make = results / 100
			total = 0
			json = self._single_search(query, results)
			result_set.extend(json)
			total += 1
			for i in xrange(queries_to_make - 1):
				json = self._single_search(query=query, results=100, pages = i+2)
				result_set.extend(json)
		self.last_query = result_set
		return self.last_query
