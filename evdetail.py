#! python2
import webapp2
import jinja2
import time
import os
from google.appengine.api import users
from google.appengine.ext import ndb
from datastore import MyUser
from datastore import ElecVel
from datastore import EvReview
JINJA_ENVIRONMENT = jinja2.Environment(
	loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
	extensions=['jinja2.ext.autoescape'],
	autoescape=True)
class EvDetail(webapp2.RequestHandler):
    def get(self):
        self.response.headers['Content-Type'] = 'text/html'
        car = ndb.Key(ElecVel,int(self.request.get("car"))).get()
        reviews = EvReview.query(EvReview.car == int(self.request.get("car"))).order(-EvReview.date).fetch()
        avg = 0
        for rev in reviews:
            avg += rev.rating
        if len(reviews) != 0:
            avg = float(avg) / len(reviews)
        else:
            avg = 0
        template_values = {
        "car" : car,
        "reviews" : reviews ,
        "avg_rating" : round(avg,2)
        }
        template = JINJA_ENVIRONMENT.get_template("evdetail.html")
        self.response.write(template.render(template_values))
