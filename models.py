from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

import geocoder
import requests
import json


#CREATE DATABASE OBJECT

db = SQLAlchemy()


#CREATE A CLASS TO MODEL USERS

class User(db.Model):
	__tablename__='users'
	uid = db.Column(db.Integer, primary_key = True)
	firstname = db.Column(db.String(100))
	lastname = db.Column(db.String(100))
	email = db.Column(db.String(120), unique = True )
	pwdhash = db.Column(db.String(100))

def __init__(self,firstname,lastname,email,pwdhash):
	self.firstname = firstname.title()
	self.lastname = lastname.title()
	self.email = email.lower()
	self.set_password(pwdhash)

def set_password(self,pwdhash):
    self.pwdhash = generate_password_hash(pwdhash)

def check_password(self,pwdhash):
    return bcrypt.check_password_hash(self.pwdhash, pwdhash)


class Place(object):
	'''
	Wikipedia API Wrapper
	'''
	def address_to_latlng(self,address):
		g = geocoder.google(address)
		return(g.lat,g.lng)

	def meters_to_walking_time(self,meters):
		return int(meters / 80)	 #80 meters is one minute walking time

	def query(self,address):
		lat, lng = self.address_to_latlng(address)

		query_url = 'https://en.wikipedia.org/w/api.php?action=query&list=geosearch&gsradius=10000&gscoord={0}%7C{1}&gslimit=20&format=json'.format(lat,lng)

		r = requests.get(query_url)
		results = r.text

		data = json.loads(results)

		places = []

		for place in data['query']['geosearch']:
			name = place['title']
			meters = place['dist']
			lat = place['lat']
			lng = place['lon']

			walking_time = self.meters_to_walking_time(meters)

			d = {'name' : name,
			     'time' : walking_time,
			     'url' : '#',
			     'lat' : lat,
			     'lng' : lng



			}

			places.append(d)

		return places	


