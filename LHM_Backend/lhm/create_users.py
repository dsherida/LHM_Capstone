import lhm
from lhm import models

from lhm.config import *

lhm.app.test_request_context().push()

lhm.app.config.update(dict(
	SQLALCHEMY_DATABASE_URI=DATABASE_URL,
	DEBUG=False,
	SECRET_KEY=SECRET_KEY,
))


models.db.init_app(lhm.app)
new = models.User()

p = "helloworld"
ems = ["jbaldwi6@asu.edu", "Abhishek.Gohil@asu.edu", "nyalama1@asu.edu", "dsherida@asu.edu", "shantanu@asu.edu"]

for e in ems:
	new = models.User()
	new.email = e
	new.set_password(p)
	new.put()

make = ['Toyota', 'Ford', 'Nissan']
model = ['A', 'B' 'C', 'D']
color = ['Black', 'Blue', 'Silver']
status = ['Tent', 'Inventory', 'Sold', 'Test Drive']

import uuid

for a in make:
	for b in model:
		for c in color:
			for d in status:
				new = models.Vehicle()
				new.make = a
				new.model = b
				new.color = c
				new.status = d
				new.vin = str(uuid.uuid4())
				new.put()

