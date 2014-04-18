from app import app
from config import *

app.config.update(dict(
	SQLALCHEMY_DATABASE_URI=DATABASE_URL,
	DEBUG=False,
	SECRET_KEY=SECRET_KEY,
))
