import requests
import ssl
import json

# The requests module likes to complain about stuff.
requests.packages.urllib3.disable_warnings()

# You could break the base of api up, that might be nicer
api_url = 'https://cluster1.demo.netapp.com/api/storage/aggregates'

# When you use the web interface to run a command in the ontap api, the token is listed, just grab it from there
token = "YWRtaW46TmV0YXBwMSE="

# we need to be able to pass the token as part of our headers
myheaders = {"accept": "application/json",  "authorization": "Basic " + token}

# headers = myheaders so we can pass the token
# verify=False so we don't get ssl certificate errors when using self signed certs
r = requests.get(api_url, headers=myheaders, verify=False)
j = r.json()


def show_aggrs():
    if j['num_records'] == 0:
        print("No aggregates have been created")
    else:
        print(json.dumps(j, indent=4))

show_aggrs()
