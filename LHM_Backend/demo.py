import requests

email = "shantanu@asu.edu"
password = "helloworld"

auth = email, password

url = "http://asu-websvr.lhmauto.com/"

print "Fetching first ten vehicles..."
r = requests.get(url + "vehicle", auth=auth)
print "Fetched first ten vehicles."

for i, v in enumerate(r.json()['vehicles']):
	if i > 10:
		break

	print i, v['vin']

vin = raw_input("Enter the VIN you would like to look up: ")
print "Fetching vehicle with VIN:", vin
r = requests.get(url + 'vehicle/' + vin, auth=auth)
print "Fetched vehicle data."

print "\n"
print "--- Raw JSON Object ---"
print r.content
print "--- END RAW OUTPUT ---"
print "\n"

notes = raw_input("Enter notes for the vehicle: ")
print "Saving notes to vehicle with VIN:", vin
r = requests.post(url + 'vehicle/' + vin, auth=auth, data={'notes': notes})
print "Saved vehicle data."

print "\n"
print "--- Raw JSON Object ---"
print r.content
print "--- END RAW OUTPUT ---"
print "\n"


