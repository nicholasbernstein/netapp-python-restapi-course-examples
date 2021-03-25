################################################################################
# NetApp-Jenkins Integration Scripts
#          This script was developed by NetApp to help demonstrate NetApp
#          technologies.  This script is not officially supported as a
#          standard NetApp product.
#
# Purpose: Script to list all the clones in a cluster.
#
#
# Usage:   %> list_clones.py <args>
#
# Author:  Akshay Patil (akshay.patil@netapp.com)
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
import base64
import argparse
import sys
import requests
import ssl
import subprocess
import time
import os
from subprocess import call
import texttable as tt

requests.packages.urllib3.disable_warnings()

def get_clones():
    base64string = base64.encodestring('%s:%s' %(apiuser,apipass)).replace('\n', '')

    url = "https://{}/api/storage/volumes/?clone.is_flexclone=true".format(api)
    headers = {
        "Authorization": "Basic %s" % base64string,
        "Content-Type": "application/json",
        "Accept": "application/json"
    }

    r = requests.get(url, headers=headers,verify=False)
    return r.json()

def disp_vol():
    ctr = 0
    tmp = dict(get_clones())
    #print tmp
    vols = tmp['records']
    tab = tt.Texttable()
    header = ['Clone name']
    tab.header(header)
    tab.set_cols_align(['c'])
    for i in vols:
            ctr = ctr + 1
            vol = i['name']
            row = [vol]
            tab.add_row(row)
            tab.set_cols_align(['c'])
    print "Number of Volumes for this Storage Tenant:{}".format(ctr)
    s = tab.draw()
    print s

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Passing variables to the program')
    parser.add_argument('-a','--api', help='API server IP:port details',dest='api')
    parser.add_argument('-vs','--vs', help='SVM Name',dest='vs')
    parser.add_argument('-apiuser','--apiuser', help='Add APIServer Username',dest='apiuser',required=True)
    parser.add_argument('-apipass','--apipass', help='Add APIServer Password',dest='apipass',required=True)
    globals().update(vars(parser.parse_args()))
    disp_vol()
