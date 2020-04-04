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
class EvCompare(webapp2.RequestHandler):
    def get(self):
        self.response.headers['Content-Type'] = 'text/html'
        ev = ElecVel.query().fetch()
        template_values = {
        "ev" : ev
        }
        template = JINJA_ENVIRONMENT.get_template("evcompare.html")
        self.response.write(template.render(template_values))

    def post(self):
        if self.request.get('button') == 'Compare':
            Car1 = self.request.get("car1")
            Car2 = self.request.get("car2")
            if Car1 == Car2:
                template = JINJA_ENVIRONMENT.get_template("error.html")
                template_values = {
                "error" : "Cannot compare same ev!" ,
                "url" : "evcompare"
                }
                self.response.write(template.render(template_values))
            elif  Car1 != "" and Car2 != "":
                ev = ElecVel.query().fetch()
                car1 = ndb.Key(ElecVel,int(Car1)).get()
                car2 = ndb.Key(ElecVel,int(Car2)).get()
                reviews1 = EvReview.query(EvReview.car == int(Car1)).fetch()
                reviews2 = EvReview.query(EvReview.car == int(Car2)).fetch()
                template_values = {
                "ev" : ev,
                "car1" : car1,
                "car2" : car2
                }
                template = JINJA_ENVIRONMENT.get_template("evcompare.html")
                self.response.write(template.render(template_values))
            else:
                template = JINJA_ENVIRONMENT.get_template("error.html")
                template_values = {
                "error" : "Select 2 ev to compare!",
                "url" : "evcompare"
                }
                self.response.write(template.render(template_values))
        elif self.request.get('button') == 'Cancel':
            self.redirect('/')
