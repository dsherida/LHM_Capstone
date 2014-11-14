from flask.ext.sqlalchemy import SQLAlchemy
from passlib.hash import bcrypt

db = SQLAlchemy()


class ModelUtils:
	""" Provide utility functions for saving and deleting individual entities
	stored in the SQLAlchemy database.
	"""
	def put(self):
		db.session.add(self)
		db.session.commit()

	def delete(self):
		db.session.delete(self)
		db.session.commit()

users = db.Table('users',
	db.Column('user_id', db.Integer, db.ForeignKey('user.id')),
	db.Column('location_id', db.Integer, db.ForeignKey('location.id'))
)


class User(db.Model, ModelUtils):
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(255))
	image_url = db.Column(db.String(255))
	latitude = db.Column(db.Float)
	longitude = db.Column(db.Float)
	email = db.Column(db.String(255), unique=True)
	password = db.Column(db.String(255))
	notes = db.Column(db.Text)

	def to_json(self):
		return {
			'id': self.id,
			'email': self.email,
			'notes': self.notes,
			'name': self.name,
			'image_url': self.image_url,
			'latitude': self.latitude,
			'longitude': self.longitude,
			'locations': [l.id for l in self.locations],
		}

	def set_password(self, password):
		self.password = bcrypt.encrypt(password)

	def verify_password(self, password):
		return bcrypt.verify(password, self.password)


class Location(db.Model, ModelUtils):
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(255))
	type = db.Column(db.String(255))
	zipcode = db.Column(db.String(255))
	latitude = db.Column(db.Float)
	longitude = db.Column(db.Float)
	address = db.Column(db.Text)
	notes = db.Column(db.Text)
	users = db.relationship('User', secondary=users,
		backref=db.backref('locations', lazy='dynamic'))
	vehicles = db.relationship('Vehicle', backref='location',
		lazy='dynamic')

	def to_json(self):
		return {
			'id': self.id,
			'name': self.name,
			'type': self.type,
			'zipcode': self.zipcode,
			'latitude': self.latitude,
			'longitude': self.longitude,
			'address': self.address,
			'notes': self.notes,
			'users': [u.id for u in self.users],
		}


class Vehicle(db.Model, ModelUtils):
	id = db.Column(db.Integer, primary_key=True)
	vin = db.Column(db.String(255))
	stock_num = db.Column(db.String(255))
	image = db.Column(db.Text)
	make = db.Column(db.String(255))
	model = db.Column(db.String(255))
	year = db.Column(db.String(255))
	color = db.Column(db.String(255))
	status = db.Column(db.String(255))
	notes = db.Column(db.Text)
	location_id = db.Column(db.Integer, db.ForeignKey('location.id'))
	tent_sale = db.Column(db.Boolean)

	def to_json(self):
		return {
			'id': self.id,
			'vin': self.vin,
			'make': self.make,
			'model': self.model,
			'color': self.color,
			'year': self.year,
			'status': self.status,
			'notes': self.notes,
			'image': self.image or "http://lorempixel.com/640/480/transport/",
			'location': self.location_id,
			'tent_sale': self.tent_sale or False,
		}
