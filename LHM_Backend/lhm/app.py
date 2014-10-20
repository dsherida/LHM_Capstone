from flask import Flask, jsonify, request, session, render_template, redirect
import models
from jinja2 import TemplateNotFound
from auth import requires_auth, check_auth

app = Flask(__name__)
models.db.init_app(app)


# User Management Handlers
# TODO: Secure User Management Handlers with Admin Authentication
"""
@app.before_request
def extend_form():
	if request.method == 'GET':
		request.args.extend(dict(request.get_json()) or {})
	else:
		request.form.extend(dict(request.get_json()) or {})
"""
@app.route('/', defaults={'page': 'login'})
@app.route('/<page>')
def show(page):
	try:
		return render_template('%s.html' % page)
	except TemplateNotFound:
		abort(404)


@app.route('/login', methods=['POST'])
def login():
	email = request.form['email']
	password = request.form['password']
	check_auth(email, password)
	return render_template('home.html')


@app.route('/view/vehicle', methods=['GET', 'POST'])
def view_vehicle():
	vin = request.args['vin']
	vehicle = models.Vehicle.query.filter_by(vin=vin).first()
	return render_template('vehicle.html', vehicle=vehicle)


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

	return jsonify(user=user.to_json())


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

	return jsonify(user=user.to_json())


@app.route('/search', methods=['GET'])
@requires_auth
def search_vehicles():
	query = models.Vehicle.query
	status = request.args.get('status')
	make = request.args.get('make')
	model = request.args.get('model')
	color = request.args.get('color')
	sort = request.args.get('sort')

	if status:
		query = query.filter_by(status=status)
	if make:
		query = query.filter_by(make=make)
	if model:
		query = query.filter_by(model=model)
	if color:
		query = query.filter_by(color=color)

	if sort:
		query.order_by(models.Vehicle.__dict__[sort])

	vehicles = query.all()

	return jsonify(vehicles=[v.to_json() for v in vehicles])


# Vehicle Data Handlers
@app.route('/vehicle', methods=['GET', 'POST'])
@requires_auth
def get_vehicles():
	if request.method == 'GET':
		vehicles = models.Vehicle.query.all()
		return jsonify(vehicles=[v.to_json() for v in vehicles])

	vehicle = models.Vehicle()
	vehicle.status = request.form.get('status')
	vehicle.make = request.form.get('make')
	vehicle.model = request.form.get('model')
	vehicle.color = request.form.get('color')
	vehicle.notes = request.form.get('notes')
	vehicle.put()
	return jsonify(vehicle=vehicle.to_json())


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
	return jsonify(vehicle=vehicle.to_json())


@app.route('/updatedata')
def update_data():
	import os, csv
	FILE_PATH = os.path.abspath(os.path.dirname(__file__))
	csvfile = open(os.path.join(FILE_PATH, "../sample_data.csv"))
	csvreader = csv.reader(csvfile)
	vehicles = models.Vehicle.query.all()
	for v in vehicles:
		models.db.session.delete(v)
	first = True
	for row in csvreader:
		if first:
			first = False
			continue
		v = models.Vehicle()
		v.year = row[0]
		v.vin = row[1]
		v.make = row[2]
		v.model = row[3]
		v.color = row[4]
		v.status = row[5]
		models.db.session.add(v)
	models.db.session.commit()
	return "All sample data up to date!"
