import logging
from time import strptime
import urllib2
import json
import datetime
now = str(datetime.date.today())
now = strptime(now,"%Y-%m-%d")

from google.appengine.ext import db
def main(section,hosturl):
  toview = []
  #url = urllib2.urlopen(hosturl+"/json")
  #content = url.read()
  #jsondata = json.loads(content)
  #for data in jsondata:
  #  if (data["type"] == section): 
  #      toview.append({"latitude":data["latitude"],"longitude":data["longitude"],"type":data["type"],"title":data["title"],"link":data["link"],"address":data["address"],"content":data["content"]})
  
  data = db.GqlQuery("SELECT * FROM blurb") 
  for d in data:
    if (d.section == section): 
      toview.append({"date":str(d.date_of_publish),"latitude":d.latitude,"longitude":d.longitude,"type":d.section,"title":d.title,"link":d.link,"address":d.address,"content":d.content})
  return toview
    
