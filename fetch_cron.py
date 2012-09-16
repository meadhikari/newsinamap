#!/usr/bin/env python
import urllib2
import re
import datetime
import feedparser
import unicodedata
import logging
import urllib2
from xml.dom.minidom import parseString
import json
from HTMLParser import HTMLParser

import datetime
from google.appengine.ext import db
from google.appengine.api import users



class blurb(db.Model):
      date_of_publish = db.DateProperty(auto_now=True)
      title = db.StringProperty()
      longitude = db.StringProperty()
      latitude = db.StringProperty()
      address = db.StringProperty()
      link = db.StringProperty()
      content = db.StringProperty(multiline=True)
      section = db.StringProperty()
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
titlecache = [] 
addcache = {}
def add2latlong(add):
  if addcache.has_key(add):
    return addcache[add]
  try:
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
  except:
    longitude,latitude = ("0","0")
  addcache[add] = (longitude,latitude) 
  return (longitude,latitude)

def main(feed,section):
  """main handler"""
  toview = []
  d = feedparser.parse(feed)
  #addres = ["Kathmandu","Pokhara","London","Islamabad"]
  #d = feedparser.parse("http://fulltextrssfeed.com/www.myrepublica.com/portal/rss.php")
  for entries in  d.entries:
  #for entries , address in  zip(d.entries,addres):

     now = str(datetime.date.today())
     title = entries.title
     content = entries.description
     link = entries.link
     link = link.encode('utf-8')
     content = strip_tags(content)
     content = content.encode('utf-8')
     title = title.encode('utf-8')
     #address = content.split()[0]
     #address = re.split("\(Reuters\)",content)[0].replace(" ","+")
     try:
      address = re.findall("^[A-Z]+ [A-Z]+|[A-Z]+",content)[0].replace(" ","")
     except:
      continue
     #address = re.findall(".*\(",content)[0].replace("(","").replace(" ","+")
     #address = content[0:content.find('Reuters')].split(" ")[0] #future me die in hell while understanding this shit you wrote
     longitude,latitude =  add2latlong(address)
     if latitude != "0" or longitude != "0" or latitude.isdigit() or longitude.isdigit():
       #toview.append((latitude,longitude,title,link,address,json.dumps(content)))
       if title in titlecache:
         continue
       else:
         b = blurb(key_name=title,title=title,longitude=longitude,latitude=latitude,link=link,address=address,content=json.dumps(content),section=section)
         titlecache.append(title);
         #toview.append({"latitude":latitude,"longitude":longitude,"title":title,"link":link,"address":address,"content":json.dumps(content)})
         b.put()
         #return toview
main("http://feeds.reuters.com/Reuters/worldNews",section="world")
main("http://feeds.reuters.com/reuters/technologyNews",section="tech")
main("http://feeds.reuters.com/reuters/sportsNews",section="sports")
main("http://feeds.reuters.com/reuters/entertainment",section="entertainment")

