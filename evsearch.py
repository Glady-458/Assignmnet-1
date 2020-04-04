#! python2
import webapp2
import jinja2
from google.appengine.api import users
from google.appengine.ext import ndb
import os
from datastore import MyUser
from datastore import ElecVel
JINJA_ENVIRONMENT = jinja2.Environment(
	loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
	extensions=['jinja2.ext.autoescape'],
	autoescape=True)
class EVSearch(webapp2.RequestHandler):
    def get(self):
		self.response.headers['Content-Type'] = 'text/html'
		template = JINJA_ENVIRONMENT.get_template('evsearch.html')
		self.response.write(template.render())

    def post(self):
		self.response.headers['Content-Type'] = 'text/html'
		user = users.get_current_user()
		ev_key = ndb.Key('ElecVel', user.user_id())
		ev = ev_key.get()
		car = []
		if self.request.get('button') == 'Search':
			search_str = self.request.get('vechSearch')
			search_cat = self.request.get('category')
			if search_cat in("Battery","Wltp","Cost","Power") and self.request.get('min') != "" and self.request.get('max') != "":
				min = float(self.request.get('min'))
				max = float(self.request.get('max'))
			elif search_cat in("Year") and self.request.get('min') != "" and self.request.get('max') != "":
				min = int(self.request.get('min'))
				max = int(self.request.get('max'))
			if search_str != "" and search_cat != "" and self.request.get('min') != "" and self.request.get('max') != "":
				car = ElecVel.query(ndb.AND(ndb.OR(ElecVel.name == search_str , ElecVel.manufacturer == search_str), ndb.AND(getattr(ElecVel, search_cat) >= min, getattr(ElecVel, search_cat) <= max))).fetch()
			elif search_str != "":
				car = ElecVel.query(ndb.OR(ndb.OR(ElecVel.name == search_str, ElecVel.manufacturer == search_str))).fetch()
			elif search_cat != "" and self.request.get('min') != "" and self.request.get('max') != "":
				car = ElecVel.query(ndb.AND(getattr(ElecVel, search_cat) >= min, getattr(ElecVel, search_cat) <= max)).fetch()
			else:
				car = ElecVel.query().fetch()

		elif self.request.get('button') == 'Cancel':
			self.redirect('/')
		template_values={}
		template_values["cars"]= car
		template = JINJA_ENVIRONMENT.get_template('evsearch.html')
		self.response.write(template.render(template_values))
