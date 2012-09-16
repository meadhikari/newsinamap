#!/usr/bin/env python
import webapp2
import jinja2
import logging
import os
import json
import datetime
from  backend import main
from HTMLParser import HTMLParser
from google.appengine.ext import db
jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader("templates"), autoescape = True)
tosend = []

from google.appengine.ext import db




class blurb(db.Model):
      date_of_publish = db.DateProperty(auto_now=True)
      title = db.StringProperty()
      longitude = db.StringProperty()
      latitude = db.StringProperty()
      address = db.StringProperty()
      link = db.StringProperty()
      content = db.StringProperty(multiline=True)
      section = db.StringProperty()
class Handler(webapp2.RequestHandler):
  def write(self,*a,**kw):
    self.response.out.write(*a,**kw)
  def render_str(self,template,**params):
    t = jinja_env.get_template(template)
    return t.render(params)
  def render(self,template,**kw):
    self.write(self.render_str(template, **kw))

class JsonHandler(Handler):
  def get(self):
    data = db.GqlQuery("SELECT * FROM blurb") 
    for d in data:
      tosend.append({"date":str(d.date_of_publish),"latitude":d.latitude,"longitude":d.longitude,"type":d.section,"title":d.title,"link":d.link,"address":d.address,"content":d.content})
    content = json.dumps(tosend);
    self.response.out.write(content);
class deleteHandler(Handler):
  def post(self):
    username = self.request.get('username')
    content  = self.request.get('content')
    q = db.GqlQuery("SELECT * FROM blurb WHERE content = :1",content )
    results = q.fetch(1)
    while results:
      db.delete(results)
      results = q.fetch(1, len(results))
    self.redirect(self.request.host_url+"/social")

class socialinputHandler(Handler):
  def get(self):
    self.render("social.html")
  def post(self):
    title = self.request.get('title')
    poster = self.request.get('poster')
    content = self.request.get('content')
    latitude = self.request.get('latitude')
    longitude = self.request.get('longitude')
    link = "http://facebook.com/"+self.request.get('username')
    address = ""
    content = "["+poster+"] " + content
    b = blurb(key_name=title+str(datetime.datetime.now()),title=title,longitude=longitude,latitude=latitude,link=link,address=address,content=content,section="social")
    
    b.put()
    self.response.out.write("<script> alert('Data Successfully Written')</script>")
    self.redirect(self.request.host_url+"/social")
class delete(Handler):
  def get(self):
    q = db.GqlQuery("SELECT * FROM blurb")
    results = q.fetch(1000)
    while results:
      print results
      db.delete(results)
      results = q.fetch(1000, len(results))
class socialNewsHandler(Handler):
  def get(self):
    self.render("index.html",tosend=main("social",self.request.host_url),section="Social")
class entertainmentNewsHandler(Handler):
  def get(self):
    self.render("index.html",tosend=main("entertainment",self.request.host_url),section="Entertainment")
class SportsNewsHandler(Handler):
  def get(self):
    self.render("index.html",tosend=main("sports",self.request.host_url),section="Sports")
class TechNewsHandler(Handler):
  def get(self):
    self.render("index.html",tosend=main("tech",self.request.host_url),section="Technology")
class WorldNewsHandler(Handler):
  def get(self):
    self.render("index.html",tosend=main("world",self.request.host_url),section="World")
app = webapp2.WSGIApplication([('/',WorldNewsHandler),('/entertainment',entertainmentNewsHandler),('/sports',SportsNewsHandler),('/tech',TechNewsHandler),('/social',socialNewsHandler),('/json',JsonHandler),('/socialinput',socialinputHandler),('/delete',delete),('/deletepost',deleteHandler)],debug=True)
