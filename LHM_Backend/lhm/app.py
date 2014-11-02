from flask import Flask, jsonify, request, session, render_template, redirect, abort
import models
from jinja2 import TemplateNotFound
from auth import requires_auth, check_auth

app = Flask(__name__)
models.db.init_app(app)


def perform_search():
	query = models.Vehicle.query
	status = request.args.get('status')
	make = request.args.get('make')
	model = request.args.get('model')
	color = request.args.get('color')
	sort = request.args.get('sort')
	location = request.args.get('location')

	if status:
		query = query.filter_by(status=status)
	if make:
		query = query.filter_by(make=make)
	if model:
		query = query.filter_by(model=model)
	if color:
		query = query.filter_by(color=color)
	if location:
		query = query.filter_by(location_id=int(location))

	if sort:
		query.order_by(models.Vehicle.__dict__[sort])

	vehicles = query.all()
	return vehicles

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

@app.route('/makes')
def view_makes():
	vehicles = perform_search()
	return jsonify(makes=sorted(list(set([v.make for v in vehicles]))))

@app.route('/models')
def view_models():
	vehicles = perform_search()
	return jsonify(models=sorted(list(set([v.model for v in vehicles]))))

@app.route('/colors')
def view_colors():
	vehicles = perform_search()
	return jsonify(colors=sorted(list(set([v.color for v in vehicles]))))

@app.route('/years')
def view_years():
	vehicles = perform_search()
	return jsonify(years=sorted(list(set([v.year for v in vehicles]))))

@app.route('/user', methods=['POST', 'GET'])
def create_user():
	if request.method == 'GET':
		email = request.args['email']
		password = request.args['password']
		u = models.User.query.filter_by(email=email).first()
		if u and u.verify_password(password):
			return jsonify(user=u.to_json())
		else:
			return jsonify(user=None)

	email = request.form['email']
	password = request.form['password']
	notes = request.form.get('notes')

	new = models.User()
	new.email = email
	new.notes = notes
	new.set_password(password)
	new.name = request.form.get('name')
	new.image_url = request.form.get('image_url')
	new.latitude = request.form.get('latitude')
	new.longitude = request.form.get('longitude')

	new.put()

	return jsonify(user=new.to_json())


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
	vehicles = perform_search()
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


# Location Data Handlers
@app.route('/location', methods=['GET', 'POST'])
@requires_auth
def get_locations():
	if request.method == 'GET':
		locations = models.Location.query.all()
		lat, long = request.args.get('latitude'), request.args.get('longitude')

		def distance(p1, p2):
			x1, y1 = p1
			x2, y2 = p2
			import math
			return math.sqrt(((x1 - x2)**2) + ((y1 - y2)**2))

		if lat and long:
			filt_point = lat, long
			locations.sort(key=lambda l: distance((l.latitude, l.longitude), filt_point))
		return jsonify(locations=[v.to_json() for v in locations])

	location = models.Location()
	location.name = request.form.get('name')
	location.type = request.form.get('type')
	location.zipcode = request.form.get('zipcode')
	lat = request.form.get('latitude')
	location.latitude = float(lat) if lat else None
	long = request.form.get('longitude')
	location.longitude = float(long) if long else None
	location.address = request.form.get('address')
	location.notes = request.form.get('notes')
	location.put()
	return jsonify(location=location.to_json())


@app.route('/vehicle/<string:vin>', methods=['GET', 'POST'])
@requires_auth
def get_vehicle(vin):
	vehicle = models.Vehicle.query.filter_by(vin=vin).first()
	if not vehicle:
		vehicle = models.Vehicle.query.filter_by(stock_num=vin).first()
	if not vehicle:
		abort(404)
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
	models.db.create_all()
	import os, csv
	FILE_PATH = os.path.abspath(os.path.dirname(__file__))
	vehicles = models.Vehicle.query.all()

	locations = models.Location.query.all()
	for l in locations:
		models.db.session.delete(l)
	models.db.session.commit()

	all_locations = []

	with open(os.path.join(FILE_PATH, "../sample_locations.csv")) as csvfile:
		csvreader = csv.reader(csvfile)
		first = True
		for row in csvreader:
			if first:
				first = False
				continue

			l = models.Location()
			l.name = row[0]
			l.type = row[1]
			l.zipcode = row[2]
			l.latitude = float(row[3])
			l.longitude = float(row[4])
			l.address = row[5]
			l.notes = row[6]
			models.db.session.add(l)
			all_locations.append(l)
	models.db.session.commit()

	users = models.User.query.all()
	for u in users:
		models.db.session.delete(u)
	models.db.session.commit()

	with open(os.path.join(FILE_PATH, "../sample_users.csv")) as csvfile:
		csvreader = csv.reader(csvfile)
		first = True
		for row in csvreader:
			if first:
				first = False
				continue

			l = models.User()
			l.name = row[0]
			l.image_url = row[1]
			l.latitude = float(row[2])
			l.longitude = float(row[3])
			l.email = row[4]
			l.set_password(row[5])
			l.notes = row[6]
			for i in [int(s) for s in row[7].split()]:
				all_locations[i - 1].users.append(l)
			models.db.session.add(l)
	for l in all_locations:
		models.db.session.add(l)
	models.db.session.commit()

	csvfile = open(os.path.join(FILE_PATH, "../sample_data.csv"))
	csvreader = csv.reader(csvfile)

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
