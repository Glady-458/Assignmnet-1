#! python2
import webapp2
import jinja2
from google.appengine.api import users
from google.appengine.ext import ndb
import os
from datastore import MyUser
from datastore import ElecVel
from edit import Edit
from evadd import EvAdd

JINJA_ENVIRONMENT = jinja2.Environment(
	loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
	extensions=['jinja2.ext.autoescape'],
	autoescape=True)
class MainPage(webapp2.RequestHandler):
	def get(self):
		self.response.headers['Content-Type'] = 'text/html'
		url = ''
		url_string = ''
		welcome = 'Welcome back'
		myuser = None
		user = users.get_current_user()
		if user:
			url = users.create_logout_url(self.request.uri)
			url_string = 'logout'
			myuser_key = ndb.Key('MyUser', user.user_id())
			myuser = myuser_key.get()
			if myuser == None:
				welcome = 'Welcome to the application'
				myuser = MyUser(id=user.user_id())
				myuser.put()

		else:
			url = users.create_login_url(self.request.uri)
			url_string = 'login'

		template_values = {
			'url' : url,
			'url_string' : url_string,
			'user' : user,
			'welcome' : welcome,
			'myuser' : myuser
		}
		template = JINJA_ENVIRONMENT.get_template('main.html')
		self.response.write(template.render(template_values))

	def post(self):
		self.response.headers['Content-Type'] = 'text/html'
		user = users.get_current_user()
		myuser_key = ndb.Key('MyUser', user.user_id())
		myuser = myuser_key.get()
		myuser.name = self.request.get('users_name')
		myuser.age = int(self.request.get('users_age'))
		myuser.put()
		self.redirect('/')

app = webapp2.WSGIApplication([
('/', MainPage),
('/edit', Edit),
('/evadd', EvAdd),
], debug=True)
