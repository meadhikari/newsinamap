from time import strptime
import datetime
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
now = datetime.date.today()
#now = strptime(now,"%Y-%m-%d")
#print now
data = db.GqlQuery("SELECT * FROM blurb")
for d in data:
  #date = strptime(data["date"],"%Y-%m-%d")
  if (d.date_of_publish != now):
    print d
    db.delete(d)
