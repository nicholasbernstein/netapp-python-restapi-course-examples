from urllib import response
from requests.auth import HTTPBasicAuth
import requests
import json


def auth_sg_api(datadict):
  authurl = 'https://dc1-adm1.demo.netapp.com/api/v3/authorize'
  
  auth = requests.post(url=authurl, data=json.dumps(datadict), verify=False)
  token = auth.json()
  return(token)

def get_sg_rules(token):
  url = "https://dc1-adm1.demo.netapp.com/api/v3/grid/alert-rules"
  myheaders = {"Authorization": "Bearer " + token['data']}
  response = requests.get(url, 
    headers=myheaders,
    verify=False)
  checks = response.json()
  return(checks)

def print_rules(checks):
  for rule in checks['data']:
    print(f"Rule: {rule['id']}: {rule['name']}" )

if __name__ == "__main__":
  datadict={
    "X-Csrf-Token": "f00332aa326a7bed888c03b05a4bf8a8",
    "username": "root",
    "password": "Netapp1!",
    "cookie": 'true',
    "csrfToken": 'true'
  }
  token = auth_sg_api(datadict=datadict)
  checks = get_sg_rules(token=token)
  print_rules(checks=checks)

  