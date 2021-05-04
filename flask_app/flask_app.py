#!/usr/bin/env python3

import json, os, sys, logging
from netapp_ontap import config, HostConnection, NetAppRestError
from netapp_ontap.resources import Volume, CifsService, Svm, Igroup
#from flask_bootstrap import Bootstrap
#from flask import Flask


def get_vols_list():
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


	# Volume
	myvols = []
	try:
		for volume in Volume.get_collection(**{"svm.name":global_vars["PRI_SVM"], "name":"!*_root"}):
			myvols.append(volume.name)
		print(json.dumps(myvols))
	except NetAppRestError as err:
		print("--> Error: Volume was not deleted:\n{}".format(err))

	return(myvols)

from flask import Flask, render_template, request
app = Flask(__name__)
#bootstrap = Bootstrap(app)
app.debug = True



@app.route('/', methods=['GET'])
def dropdown():
    myvols = get_vols_list()
    return render_template('test.html', myvols=myvols)

if __name__ == "__main__":
    app.run(host="0.0.0.0")
