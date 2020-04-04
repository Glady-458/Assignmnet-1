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
class EvAdd(webapp2.RequestHandler):
	def get(self):
		self.response.headers['Content-Type'] = 'text/html'
		user = users.get_current_user()
		ev_key = ndb.Key('ElecVel', user.user_id())
		ev = ev_key.get()
		table = ElecVel.query()
		a = table.fetch()
		keyno = int(time.time()*1000)+int(user.user_id())-18580476580402176403-167224289223619601419+99999999
		template_values = {
		'ev' : ev,
		'a' : a,
		'keyno' : keyno,
		'table' : table,
		}
		template = JINJA_ENVIRONMENT.get_template('evadd.html')
		self.response.write(template.render(template_values))
#{{e.key.id().delete()}}
	def post(self):
		self.response.headers['Content-Type'] = 'text/html'
		#date = int(time.time()*1000)
        #ev_key = ndb.Key('ElecVel', 123)
		user=users.get_current_user()
		table = ElecVel.query()
		#keyno = table.count()
		#ev = None
		#keyno = date+int(user.user_id())-185804765802701624389
		if user:
			if self.request.get('button')=='Cancel':
				self.redirect('/')
			#185804765802701624389  111111111111111111111
			# name, manufacturer, year, battery size (Kwh), WLTP range (Km), cost, power (Kw).
			elif self.request.get('button') == 'add':
				id = int(self.request.get('ID'))
				ev = ElecVel(id=id)
				ev.name = self.request.get('car_name')
				ev.manufacturer = self.request.get('car_mfc')
				ev.year = int(self.request.get('car_year'))
				ev.battery_size = float(self.request.get('car_btr_sz'))
				ev.WLTP = float(self.request.get('car_WLTP'))
				ev.power = float(self.request.get('car_power'))
				ev.cost = float(self.request.get('car_cost'))
				#temp2 = ElecVel.name
				#temp3 = ElecVel.query().filter(ndb.GenericProperty(temp2)).get()
				query=ElecVel.query(ndb.AND(ElecVel.name==ev.name,ElecVel.manufacturer==ev.manufacturer,ElecVel.year==ev.year))
				if query.count()==0:
					ev.put()
					self.redirect('/evadd')

				else:
					template = JINJA_ENVIRONMENT.get_template("error.html")
	                template_values = {
	                "error" : "Vehicle already exist!" ,
	                "url" : "evadd"
	                }
	                self.response.write(template.render(template_values))
