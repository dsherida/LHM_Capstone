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


class User(db.Model, ModelUtils):
	id = db.Column(db.Integer, primary_key=True)
	email = db.Column(db.String(255), unique=True)
	password = db.Column(db.String(255))
	notes = db.Column(db.Text)

	def __dict__(self):
		return {
			'email': self.email,
			'notes': self.notes,
		}

	def set_password(self, password):
		self.password = bcrypt.encrypt(password)

	def verify_password(self, password):
		return bcrypt.verify(password, self.password)


class Vehicle(db.Model, ModelUtils):
	id = db.Column(db.Integer, primary_key=True)
	vin = db.Column(db.String(255))
	make = db.Column(db.String(255))
	model = db.Column(db.String(255))
	color = db.Column(db.String(255))
	status = db.Column(db.String(255))
	notes = db.Column(db.Text)

