from functools import wraps
from flask import request, Response, session
from models import User


def check_auth(username, password):
	"""This function is called to check if a username /
	password combination is valid.
	"""
	u = User.query.filter_by(email=username).first()
	v = u and u.verify_password(password)
	if v:
		session['email'] = username
		session['password'] = password
	return v

def authenticate():
	"""Sends a 401 response that enables basic auth"""
	return Response(
	'Could not verify your access level for that URL.\n'
	'You have to login with proper credentials', 401,
	{'WWW-Authenticate': 'Basic realm="Login Required"'})

def requires_auth(f):
	@wraps(f)
	def decorated(*args, **kwargs):
		email, passw = session.get('email'), session.get('password')
		if email and passw:
			return f(*args, **kwargs)
		if request.method == 'GET':
			email, passw = request.args.get('email'), request.args.get('password')
		else:
			email, passw = request.form.get('email'), request.form.get('password')
		if not (email and passw and check_auth(email, passw)):
			auth = request.authorization
			if not auth or not check_auth(auth.username, auth.password):
				return authenticate()
		return f(*args, **kwargs)
	return decorated
