################################################################################
# NetApp-Jenkins Integration Scripts
#          This script was developed by NetApp to help demonstrate NetApp
#          technologies.  This script is not officially supported as a
#          standard NetApp product.
#
# Purpose: Script to create a new SVM using ONBOX REST API's.
#
#
# Usage:   %> create_svm.py <args>
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


def get_size(vol_size):
    tmp = int(vol_size) * 1024 * 1024
    return tmp

def make_volume(vol_name,svm_name,vol_size,aggr_name,export_policy_name):
    #print "^^^^^^^^^^^^^^^SVM KEy : {}".format(svm_key)
    base64string = base64.encodestring('%s:%s' %(apiuser,apipass)).replace('\n', '')
    v_size=get_size(vol_size)
    print "Vol Size is :{}".format(v_size)

    url = "https://{}/api/storage/volumes".format(api)
    payload = {
    "aggregates.name" : [aggr_name],
    "svm.name": svm_name,
    "name": vol_name,
    "size": v_size,
    "nas": {
    		"export_policy": {
      				"name": export_policy_name
    				 } 
    	   }
    }
    headers = {
    'authorization': "Basic %s" % base64string,
    'content-type': "application/hal",
    'accept': "application/hal"
    }
    response = requests.post(url,headers=headers,json=payload,verify=False)
    tt = time.time()
    print "Request Sent at: {}".format(tt)
    url_text = response.json()
    print url_text
    job_status = "https://{}/{}".format(api,url_text['job']['_links']['self']['href'])
    job_response = requests.get(job_status,headers=headers,verify=False)
    job_status = job_response.json()
    check_vol_job_status(job_status,headers)
    tt = time.time()
    print "Request succesful at: {}".format(tt)
    return


def get_key_svms(svm_name):
    tmp = dict(get_svms())
    svms = tmp['records']
    for i in svms:
        if i['name'] == svm_name:
            # print i
            return i['uuid']

def get_svms():
    base64string = base64.encodestring('%s:%s' %(apiuser,apipass)).replace('\n', '')

    url = "https://{}/api/svm/svms".format(api)
    headers = {
        "Authorization": "Basic %s" % base64string,
        "Content-Type": "application/json",
        "Accept": "application/json"
    }

    r = requests.get(url, headers=headers,verify=False)
    #print r.json()
    return r.json()


def create_export_policy(export_policy_name,export_policy_rule,svm_name):
    base64string = base64.encodestring('%s:%s' %(apiuser,apipass)).replace('\n', '')
    url = "https://{}/api/protocols/nfs/export-policies".format(api)
    svm_uuid = get_key_svms(svm_name)
    payload = {
  	"name": export_policy_name,
  	"rules": [
    			{
                         "clients": [
        			{
          			"match": export_policy_rule
        			}
      				    ],
                          "protocols": [
         				 "any"
      					],
      					"ro_rule": [
        						"any"
      						   ],
      					"rw_rule": [
        						"any"
      						   ]     			
    			}
  		 ],
  	"svm.uuid": svm_uuid
    }
    
    headers = {
    'authorization': "Basic %s" % base64string,
    'content-type': "application/json",
    'accept': "application/json"
    }
    response = requests.post(url,headers=headers,json=payload,verify=False)
    url_text = response.json()
    print url_text

def check_job_status(job_status,headers):    
    if (job_status['state'] == "failure"):
        if (job_status['code'] == 460770):
		print "SVM Already Exists, hence using it to create export policy"
		create_export_policy(export_policy_name,export_policy_rule,svm_name)
		make_volume(vol_name,svm_name,vol_size,aggr_name,export_policy_name)
	else:
        	print "SVM creation failed due to :{}".format(job_status['message'])
        	return
    elif(job_status['state'] == "success"):
        print "SVM created successfully"
        create_export_policy(export_policy_name,export_policy_rule,svm_name)
	make_volume(vol_name,svm_name,vol_size,aggr_name,export_policy_name)
        return
    else:
        job_status_url = "https://{}/api/cluster/jobs/{}".format(api,job_status['uuid'])
	job_response = requests.get(job_status_url,headers=headers,verify=False)
        job_status = job_response.json()
        print job_status
        check_job_status(job_status,headers)

def check_vol_job_status(job_status,headers):
    if (job_status['state'] == "failure"):
        if (job_status['code'] == 460770):
                print "Volume Already Exists"
                
        else:
                print "Volume creation failed due to :{}".format(job_status['message'])
                return
    elif(job_status['state'] == "success"):
        print "Volume created successfully"
        return
    else:
        job_status_url = "https://{}/api/cluster/jobs/{}".format(api,job_status['uuid'])
        job_response = requests.get(job_status_url,headers=headers,verify=False)
        job_status = job_response.json()
        print job_status
        check_job_status(job_status,headers)

def make_svm(svm_name,aggr_name):
    base64string = base64.encodestring('%s:%s' %(apiuser,apipass)).replace('\n', '')
    url = "https://{}/api/svm/svms".format(api)
    payload = {
    "name": svm_name
    }

    headers = {
    'authorization': "Basic %s" % base64string,
    'content-type': "application/json",
    'accept': "application/json"
    }
    response = requests.post(url,headers=headers,json=payload,verify=False)
    tt = time.time()
    print "Request Sent at: {}".format(tt)
    url_text = response.json()
    #print url_text
    job_status = "https://{}{}".format(api,url_text['job']['_links']['self']['href'])
    #print job_status
    job_response = requests.get(job_status,headers=headers,verify=False)
    job_status = job_response.json()
    #print job_status
    check_job_status(job_status,headers)
    tt = time.time()
    print "Request succesful at: {}".format(tt)
    return


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Passing variables to the program')
    parser.add_argument('-v','--vol_name', help='Volume to create or clone from',dest='vol_name',required=True)
    parser.add_argument('-vs','--vs name', help='Select SVM',dest='svm_name',required=True)
    parser.add_argument('-r','--export_policy_rule', help='export_policy_rule',dest='export_policy_rule')
    parser.add_argument('-ep','--export_policy_name', help='export_policy_name',dest='export_policy_name')
    parser.add_argument('-a','--api', help='API server IP:port',dest='api',required=True)
    parser.add_argument('-apiuser','--apiuser', help='Add APIServer Username',dest='apiuser',required=True)
    parser.add_argument('-apipass','--apipass', help='Add APIServer Password',dest='apipass',required=True)
    parser.add_argument('-s','--vol_size', help='Size of Volume in MB',dest='vol_size',required=True)
    parser.add_argument('-aggr','--aggr_name', help='Name of Aggregate',dest='aggr_name',required=True)
    globals().update(vars(parser.parse_args()))
    make_svm(svm_name,aggr_name)
    print "Script Complete"
    
