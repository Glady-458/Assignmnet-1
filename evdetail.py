#! python2
import webapp2
import jinja2
import time
import os
from google.appengine.api import users
from google.appengine.ext import ndb
from datastore import MyUser
from datastore import ElecVel
JINJA_ENVIRONMENT = jinja2.Environment(
	loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
	extensions=['jinja2.ext.autoescape'],
	autoescape=True)
class EvDetail(webapp2.RequestHandler):
    def get(self):
        self.response.headers['Content-Type'] = 'text/html'
        user = users.get_current_user()

    	if user:
            myuser_key = ndb.Key('MyUser', user.user_id())
            myuser = myuser_key.get()
            key = self.request.get("car")
            car = ndb.Key(ElecVel,int(key)).get()
            #template_values["car"] = car
        template_values={
        "car" : car
        }
        template = JINJA_ENVIRONMENT.get_template("detail.html")
        self.response.write(template.render(template_values))

    def post(self):
        self.response.headers['Content-Type'] = 'text/html'
        key = self.request.get("car")
        ev = ndb.Key(ElecVel,int(key)).get()
        if self.request.get("button") == "Edit":
            ev.name = self.request.get("name")
            ev.manufacturer = self.request.get("manufacturer")
            ev.year = int(self.request.get("year"))
            ev.battery_size = float(self.request.get("battery"))
            ev.wltp = float(self.request.get("wltp"))
            ev.cost = float(self.request.get("cost"))
            ev.power = float(self.request.get("power"))
            ev.put()
        elif self.request.get("button") == "Delete":
            ev.key.delete()
        self.redirect("/evsearch")
