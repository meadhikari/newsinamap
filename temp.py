import urllib2
import feedparser
from xml.dom.minidom import parseString   
from HTMLParser import HTMLParser
import re
class MLStripper(HTMLParser):
    def __init__(self):
        self.reset()
        self.fed = []
    def handle_data(self, d):
        self.fed.append(d)
    def get_data(self):
        return ''.join(self.fed)
             
def strip_tags(html):
    s = MLStripper()
    s.feed(html)
    return s.get_data()
def add2latlong(add):
  
  try:
	#print "Yes I came to change lat and long"
	file = urllib2.urlopen('http://where.yahooapis.com/geocode?q='+add+'&appid=4fdcJM6m')
	data = file.read()
	file.close()
	dom = parseString(data)
	longxml = dom.getElementsByTagName('longitude')[0].toxml()
	latxml = dom.getElementsByTagName('latitude')[0].toxml()
	longitude =longxml.replace('<longitude>','').replace('</longitude>','')
	latitude=latxml.replace('<latitude>','').replace('</latitude>','')
	longitude =longitude.encode('utf-8')
	latitude = latitude.encode('utf-8')
	print (latitude,longitude)
	print add
  except:
	  (longitude,latitude) = (0,0)
	  print "I can't"
	  
  
  return (longitude,latitude)
  
def main(feed="http://feeds.reuters.com/Reuters/worldNews"):
  
  d = feedparser.parse(feed)
  for entries in  d.entries:
	
	content = entries.description
	content = strip_tags(content)
	content = content.encode('utf-8')
	try:
		address = re.findall("^[A-Z]+ [A-Z]+|[A-Z]+",content)[0].replace(" ","")
		
		
	except:
		continue
	address = "NEW YORK".replace(" ","")
	add2latlong(address)


main()

