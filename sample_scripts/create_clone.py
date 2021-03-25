################################################################################
# NetApp-Jenkins Integration Scripts
#          This script was developed by NetApp to help demonstrate NetApp
#          technologies.  This script is not officially supported as a
#          standard NetApp product.
#
# Purpose: Script to create a new FlexClone using ONBOX REST API's.
#
#
# Usage:   %> create_clone.py <args>
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


import time
import base64
import argparse
import json
import requests 
requests.packages.urllib3.disable_warnings()

def get_svms():
    base64string = base64.encodestring('%s:%s' %(apiuser,apipass)).replace('\n', '')
    
    url = "https://{}/api/svm/svms".format(api)
    headers = {
    'authorization': "Basic %s" % base64string,
    'content-type': "application/hal",
    'accept': "application/hal"
    }

    r = requests.get(url, headers=headers,verify=False)
    #print r.json()
    return r.json()


def get_key_svms(svm_name):
    tmp = dict(get_svms())
    svms = tmp['records']
    #print svms
    for i in svms:
        if i['name'] == svm_name:
            #print i
            return i['uuid']

def get_key_vol(vol_name):
    tmp = dict(get_vols())
    vols = tmp['records']
    #print svms
    for i in vols:
        if i['name'] == vol_name:
            #print i
            return i['uuid']

    
def get_vols():
    base64string = base64.encodestring('%s:%s' %(apiuser,apipass)).replace('\n', '')
    url = "https://{}/api/storage/volumes/".format(api)

    headers = {
    'authorization': "Basic %s" % base64string,
    'content-type': "application/hal",
    'accept': "application/hal"
    }
    r = requests.get(url, headers=headers,verify=False)
    return r.json()
      
def get_size(vol_size):
    tmp = int(vol_size) * 1024 * 1024
    return tmp

def check_job_status(job_status):    
    if (job_status['state'] == "failure"):
        print "Clone creation failed due to :{}".format(job_status['message'])
        return
    elif(job_status['state'] == "success"):
        print "Clone created successfully"
        return
    else:
        print job_status['state']
        check_job_status(job_status)

def make_clone(vol_name,svm_name,snap_name,aggr_name,clone_name):
    vol_key=get_key_vol(svm_name)
    #print "^^^^^^^^^^^^^^^SVM KEy : {}".format(svm_key)
    base64string = base64.encodestring('%s:%s' %(apiuser,apipass)).replace('\n', '')
    #v_size=get_size(vol_size)
    #print "Vol Size is :{}".format(v_size)

    url = "https://{}/api/storage/volumes".format(api) 
    payload = {
    "svm.name": svm_name,
    "clone.is_flexclone": "true",
    "clone.parent_snapshot.name": snap_name,
    "clone.parent_volume.name": vol_name,
    "name": clone_name
    }
 
    headers = {
    'authorization': "Basic %s" % base64string,
    'content-type': "application/hal",
    'accept': "application/hal"
    }
    response = requests.post(url,headers=headers,json=payload,verify=False)
    url_text = response.json()
    print url_text
    job_status = "https://{}/{}".format(api,url_text['job']['_links']['self']['href'])
    job_response = requests.get(job_status,headers=headers,verify=False)
    job_status = job_response.json()
    check_job_status(job_status)
    return


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Passing variables to the program')
    parser.add_argument('-v','--vol_name', help='Volume to create or clone from',dest='vol_name',required=True)
    parser.add_argument('-vs','--vs name', help='Select SVM',dest='svm_name',required=True)
    parser.add_argument('-s','--snapshot_name', help='Name of Snapshopt',dest='snap_name',required=True)
    parser.add_argument('-a','--api', help='API server IP:port',dest='api',required=True)
    parser.add_argument('-c','--clone_name', help='API server IP:port',dest='clone_name',required=True)
    parser.add_argument('-apiuser','--apiuser', help='Add APIServer Username',dest='apiuser',required=True)
    parser.add_argument('-apipass','--apipass', help='Add APIServer Password',dest='apipass',required=True)
    parser.add_argument('-aggr','--aggr_name', help='Name of Aggregate',dest='aggr_name',required=True)
    globals().update(vars(parser.parse_args()))
    make_clone(vol_name,svm_name,snap_name,aggr_name,clone_name)
    print "Script Complete"
    
