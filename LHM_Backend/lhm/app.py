from flask import Flask, jsonify, request, session
import models
from auth import requires_auth

app = Flask(__name__)
models.db.init_app(app)


# User Management Handlers
# TODO: Secure User Management Handlers with Admin Authentication


@app.route('/user', methods=['POST'])
def create_user():
	email = request.form['email']
	password = request.form['password']
	notes = request.form['notes']

	new = models.User()
	new.email = email
	new.notes = notes
	new.set_password(password)
	new.put()

	return jsonify(user=dict(user))


@app.route('/user/<int:id>', methods=['POST'])
def update_user(id):
	email = request.form.get('email')
	password = request.form.get('password')
	notes = request.form.get('notes')

	user = models.User.query.get(id)
	user.email = email or user.email
	user.notes = notes or user.notes
	if password:
		user.set_password(password)
	user.put()

	return jsonify(user=dict(user))


# Vehicle Data Handlers
@app.route('/vehicle', methods=['GET', 'POST'])
@requires_auth
def get_vehicles():
	if request.method == 'GET':
		vehicles = models.Vehicle.query.all()
		return jsonify(vehicles=[dict(v) for v in vehicles])

	vehicle = models.Vehicle()
	vehicle.status = request.form.get('status')
	vehicle.make = request.form.get('make')
	vehicle.model = request.form.get('model')
	vehicle.color = request.form.get('color')
	vehicle.notes = request.form.get('notes')
	vehicle.put()
	return jsonify(vehicle=dict(vehicle))


@app.route('/vehicle/<string:vin>', methods=['GET', 'POST'])
@requires_auth
def get_vehicle(vin):
	vehicle = models.Vehicle.query.filter_by(vin=vin).first()
	if request.method == 'POST':
		vehicle.status = request.form.get('status') or vehicle.status
		vehicle.make = request.form.get('make') or vehicle.make
		vehicle.model = request.form.get('model') or vehicle.model
		vehicle.color = request.form.get('color') or vehicle.color
		vehicle.notes = request.form.get('notes') or vehicle.notes
		vehicle.put()
	return jsonify(vehicle=dict(vehicle))

