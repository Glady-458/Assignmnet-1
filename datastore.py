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
	WLTP_min = ndb.FloatProperty()
	WLTP_max = ndb.FloatProperty()
	cost = ndb.FloatProperty()
	power = ndb.FloatProperty()


# name, manufacturer, year, battery size (Kwh), WLTP range (Km), cost, power (Kw).
