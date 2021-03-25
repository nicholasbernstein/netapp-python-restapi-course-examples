################################################################################
# NetApp-Jenkins Integration Scripts
#          This script was developed by NetApp to help demonstrate NetApp 
#          technologies.  This script is not officially supported as a 
#          standard NetApp product.
#         
# Purpose: Script to create a new checkpoint of the base partition.
#          
#
# Usage:   %> snapshot_create.py <args> 
#
# Author:  Akshay Patil (akshay.patil@netapp.com)
#           
#
# NETAPP CONFIDENTIAL
# -------------------
# Copyright 2016 NetApp, Inc. All Rights Reserved.
#
# NOTICE: All information contained herein is, and remains the property
# of NetApp, Inc.  The intellectual and technical concepts contained
# herein are proprietary to NetApp, Inc. and its suppliers, if applicable,
# and may be covered by U.S. and Foreign Patents, patents in process, and are
# protected by trade secret or copyright law. Dissemination of this
# information or reproduction of this material is strictly forbidden unless
# permission is obtained from NetApp, Inc.
#
################################################################################
import subprocess
from subprocess import call
import base64
import argparse
import sys
import requests
import ssl
import time
import os

requests.packages.urllib3.disable_warnings()

def get_volumes():
    base64string = base64.encodestring('%s:%s' %(apiuser,apipass)).replace('\n', '')
    url = "https://{}/api/storage/volumes/".format(api)
    headers = {
        "Authorization": "Basic %s" % base64string,
        "Content-Type": "application/json",
        "Accept": "application/json"
    }

    r = requests.get(url, headers=headers,verify=False)
    #print r.json()
    return r.json()

def get_key(vol_name):
    tmp = dict(get_volumes())
    vols = tmp['records']
    for i in vols:
        if i['name'] == vol_name:
            # print i
            return i['uuid']

def check_job_status(job_status_url,job_status,headers):
    if (job_status['state'] == "failure"):
        print "Snapshot creation failed due to :{}".format(job_status['message'])
        return
    elif(job_status['state'] == "success"):
        print "Snapshot created successfully"
        return
    else:
        job_response = requests.get(job_status_url,headers=headers,verify=False)
        job_status = job_response.json()
        check_job_status(job_status_url,job_status,headers)

def make_snap(vol_name,snapshot_name):
    base64string = base64.encodestring('%s:%s' %(apiuser,apipass)).replace('\n', '')
    vol_uuid = get_key(vol_name)

    data= {
      #"volume.uuid": vol_uuid,
      "name":snapshot_name
    }

    snap_api_url= "https://{}/api/storage/volumes/{}/snapshots".format(api,vol_uuid)
    headers = {
        "Authorization": "Basic %s" % base64string,
        "Content-Type": "application/json",
        "Accept": "application/json"
    }
    r = requests.post(snap_api_url, headers=headers,json=data,verify=False)
    url_text = r.json()
    print url_text
    job_status_url = "https://{}/{}".format(api,url_text['job']['_links']['self']['href'])
    job_response = requests.get(job_status_url,headers=headers,verify=False)
    job_status = job_response.json()
    check_job_status(job_status_url,job_status,headers)
    return



if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Passing variables to the program')
    parser.add_argument('-v','--vol_name', help='Volume to create or clone from',dest='vol_name',required=True)
    parser.add_argument('-s','--snapshot_name', help='Snapshot to create or clone from',dest='snapshot_name')
    parser.add_argument('-a','--api', help='API server IP:port details',dest='api')
    parser.add_argument('-apiuser','--apiuser', help='Add APIServer Username',dest='apiuser',required=True)
    parser.add_argument('-apipass','--apipass', help='Add APIServer Password',dest='apipass',required=True)
    globals().update(vars(parser.parse_args()))
    make_snap(vol_name,snapshot_name)
    #print "Checkpoint {} of Development Branch {} recorded.".format(snapshot_name,vol_name)
    print "Snapshot {} on volume {} created successfully.".format(snapshot_name,vol_name)
    
