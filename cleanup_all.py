#!/usr/bin/env python3

################################################################################
#
# Title:	cleanup_all.py
# Author:	Adrian Bronder (modified by Ronald Feist)
# Date:		2020-03-17
# Description:	Clean up the entire environment
#		with ONTAP Python client library
#
# Resources:	netapp_ontap.resources.volume
#		netapp_ontap.resources.cifs_service
#		netapp_ontap.resources.svm
#
# URLs:		http://docs.netapp.com/ontap-9/index.jsp
#		https://pypi.org/project/netapp-ontap/
#		https://library.netapp.com/ecmdocs/ECMLP2858435/html/index.html
#
################################################################################

import json, os, sys, logging
from netapp_ontap import config, HostConnection, NetAppRestError
from netapp_ontap.resources import Volume, CifsService, Svm, Igroup
import netapp_ontap


### Step 1 - Read in global variables
#with open(os.path.dirname(sys.argv[0])+'/global.vars') as json_file:
with open(os.getcwd()+'/global.vars') as json_file:
	global_vars = json.load(json_file)


### Step 2 - Configure connection
config.CONNECTION = HostConnection(
	global_vars["PRI_CLU"],
	username=global_vars["PRI_CLU_USER"],
	password=global_vars["PRI_CLU_PASS"],
	verify=False
)


### Step 3 - Delete operation
# Volume
print("--> Starting volume delete operation")
try:
	for volume in Volume.get_collection(
		**{"svm.name":global_vars["PRI_SVM"], "name":"!*_root"}):
		volume.delete()
		print("--> Volume {} deleted successfully".format(volume.name))
except NetAppRestError as err:
	print("--> Error: Volume was not deleted:\n{}".format(err))
print("")

# Volume
print("--> Starting IGroup delete operation")
try:
	for ig in netapp_ontap.resources.Igroup.get_collection("*"):
		ig.delete()
		print("--> IGroup {} deleted successfully".format(ig.name))
except NetAppRestError as err:
	print("--> Error: IGroup was not deleted:\n{}".format(err))
print("")

# CIFS Server
print("--> Starting CIFS server delete operation")
try:
	cifs = CifsService.find(name=global_vars["PRI_SVM"])
	if cifs:
		cifs.delete(body={
			"ad_domain": {
				"fqdn": global_vars["PRI_AD_DOMAIN"],
				"user": global_vars["PRI_AD_USER"], 
				"password": global_vars["PRI_AD_PASS"]
			}
		})
		print("--> CIFS server {} deleted successfully".format(cifs.name))
except NetAppRestError as err:
	print("--> Error: CIFS server was not deleted:\n{}".format(err))
print("")

# SVM
print("--> Starting SVM delete operation")
try:
	svm = Svm.find(**{"name": global_vars["PRI_SVM"]})
	if svm:
		svm.delete()
		print("--> SVM {} deleted successfully".format(svm.name))
except NetAppRestError as err:
	print("--> Error: SVM was not deleted:\n{}".format(err))
print("")
