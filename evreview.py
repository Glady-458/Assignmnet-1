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
from datetime import datetime
JINJA_ENVIRONMENT = jinja2.Environment(
	loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
	extensions=['jinja2.ext.autoescape'],
	autoescape=True)
class evReview(webapp2.RequestHandler):
    def get(self):
        self.response.headers['Content-Type'] = 'text/html'
        user = users.get_current_user()
        reviews = EvReview.query().fetch()
        ev = ElecVel.query().fetch()
        template_values = {
        "reviews" : reviews,
        "ev" : ev,
        "user" : user
        }
        template = JINJA_ENVIRONMENT.get_template("review.html")
        self.response.write(template.render(template_values))
    def post(self):
        self.response.headers['Content-Type'] = 'text/html'
        user = users.get_current_user()
        if self.request.get('button')=="Submit":
            if user:
                review = EvReview()
                review.user = user.email()
                review.car = int(self.request.get('car'))
                car = ndb.Key(ElecVel,int(self.request.get("car"))).get()
                review.car_name = car.name
                review.car_review = self.request.get('review')
                review.rating = int(self.request.get('rating'))
                review.date = datetime.now()
                review.put()
                self.redirect("/evreview")
            else:
                template = JINJA_ENVIRONMENT.get_template("error.html")
                template_values = {
                    "error" : "Please login first!" ,
                    "url" : "/"
                    }
                self.response.write(template.render(template_values))
        elif self.request.get('button')=="Cancel":
            self.redirect('/')
