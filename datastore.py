#! python2
from google.appengine.ext import ndb

class MyUser(ndb.Model):
	email_address = ndb.StringProperty()
	name = ndb.StringProperty()
	age = ndb.IntegerProperty()
class ElecVel(ndb.Model):
	name = ndb.StringProperty()
	manufacturer = ndb.StringProperty()
	year = ndb.IntegerProperty()
	battery_size = ndb.FloatProperty()
	WLTP = ndb.FloatProperty()
	cost = ndb.FloatProperty()
	power = ndb.FloatProperty()
class EvReview(ndb.Model):
	user = ndb.StringProperty()
	car = ndb.IntegerProperty()
	car_name = ndb.StringProperty()
	car_review = ndb.StringProperty()
	rating = ndb.IntegerProperty()
	date = ndb.DateTimeProperty()



# name, manufacturer, year, battery size (Kwh), WLTP range (Km), cost, power (Kw).
