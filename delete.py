
import webapp2
from google.appengine.api import db

q = db.GqlQuery("SELECT * FROM blurb")
results = q.fetch(1000)

while results:
    db.delete(results)
    results = fetch(1000, len(results))
