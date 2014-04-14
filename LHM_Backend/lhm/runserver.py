from app import app
from config import *

app.config.update(dict(
	SQLALCHEMY_DATABASE_URI=DATABASE_URL,
	DEBUG=DEBUG,
	SECRET_KEY=SECRET_KEY,
))

app.run(host=HOST, port=PORT, debug=DEBUG)
