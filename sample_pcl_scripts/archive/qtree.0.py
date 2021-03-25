#! /usr/bin/env python3.7

"""
ONTAP 9.7 REST API Python Client Library Scripts

This script performs the following:
	- Create a qtree (or quota tree)
	- Create a quota policy rule
	- Create a QoS (Quality of Service) policy on an existing SVM

usage: python3.7 qtree.py [-h] -c cluster -v VOLUME_NAME -vs VSERVER_NAME -q QTREE_NAME
               -qos QOS_POLICY_NAME -sh SPACE_HARD -fh FILE_HARD -un USER_NAME [-u API_USER] [-p API_PASS]
The following arguments are required: -v/--volume_name, -vs/--vserver_name,
          -q/--qtree_name, -qos/--qos_policy_name, -sh/--space_hard, -fh/--file_hard -un/--user_name
"""

import argparse
from getpass import getpass
import logging

from netapp_ontap import config, HostConnection, NetAppRestError
from netapp_ontap.resources import Aggregate, Svm, Volume, Qtree, QuotaRule, QosPolicy

def create_qtree_pycl(volume_name: str, vserver_name: str, qtree_name: str) -> None:
    """Creates a new quota tree in a volume"""

    data = {
        'name': qtree_name,
        'volume': {'name': volume_name},
        'svm': {'name': vserver_name},
        'security_style': 'unix',
        'unix_permissions': 744,
        'export_policy_name': 'default',
        'qos_policy': {'max_throughput_ops': 1000}
    }
    qtree = Qtree(**data)
    try:
        qtree.post()
        print("Qtree %s created successfully" % qtree.name)
    except NetAppRestError as err:
        print("Error: QTree was not created: %s" % err)
    return

def create_policy_rule_pycl(volume_name: str, vserver_name: str, qtree_name: str, user_name: str, space_hard: int, file_hard: int) -> None:
    """Creates a new policy rule for the qtree"""

    data = {
        'qtree': {'name': qtree_name},
        'volume': {'name': volume_name},
        'svm': {'name': vserver_name},
        'files': {'hard_limit': file_hard, 'soft_limit': 100},
        'space': {'hard_limit': space_hard, 'soft_limit': 100},
        #'user_mapping': 'on',
        #'type': 'user',
        #'users': {'name': user_name}
        'type': 'tree',
        #'group': {'name': 'others'}
    }
    quotarule = QuotaRule(**data)
    try:
        quotarule.post()
        print("Rule 'tree' created successfully for %s" % qtree_name)
    except NetAppRestError as err:
        print("Error: Rule was not created: %s" % err)
    return

def create_qos_policy_pycl(vserver_name: str, qos_policy_name: str) -> None:
    """Creates a new QoS policy for the SVM"""

    data = {
        'name': qos_policy_name,
        'svm': {'name': vserver_name},
        'adaptive': {
            'expected_iops': 5000,
            'peak_iops': 6000,
            'absolute_min_iops': 1000
        }
    }
    qospolicy = QosPolicy(**data)
    try:
        qospolicy.post()
        print("QoS Policy %s created successfully" % qos_policy_name)
    except NetAppRestError as err:
        print("Error: Rule was not created: %s" % err)
    return

def parse_args() -> argparse.Namespace:
    """Parse the command line arguments from the user"""

    parser = argparse.ArgumentParser(
        description="This script will create a new qtree."
    )
    parser.add_argument(
        "-c", "--cluster", required=True, help="API server IP:port details"
    )
    parser.add_argument(
        "-v", "--volume_name", required=True, help="Volume name to create qtree from"
    )
    parser.add_argument(
        "-vs", "--vserver_name", required=True, help="SVM to create the volume from"
    )
    parser.add_argument(
        "-q", "--qtree_name", required=True, help="QTree to create the qutoa tree"
    )
    parser.add_argument(
        "-qos", "--qos_policy_name", required=True, help="QoS Policy to create on the SVM"
    )
    parser.add_argument(
        "-sh", "--space_hard", required=True, help="Hard limit on space in bytese"
    )
    parser.add_argument(
        "-fh", "--file_hard", required=True, help="hard limit on files in bytes"
    )
    parser.add_argument(
        "-un", "--user_name", required=True, help="User name who can access the qtree"
    )
    parser.add_argument("-u", "--api_user", default="admin", help="API Username")
    parser.add_argument("-p", "--api_pass", help="API Password")
    parsed_args = parser.parse_args()

    # collect the password without echo if not already provided
    if not parsed_args.api_pass:
        parsed_args.api_pass = getpass()

    return parsed_args


if __name__ == "__main__":
    logging.basicConfig(
        level=logging.INFO,
        format="[%(asctime)s] [%(levelname)5s] [%(module)s:%(lineno)s] %(message)s",
    )
    args = parse_args()
    config.CONNECTION = HostConnection(
        args.cluster, username=args.api_user, password=args.api_pass, verify=False,
    )

    # Create a quota tree and a policy rule for the qtree
    #create_qtree_pycl(args.volume_name, args.vserver_name, args.qtree_name)
    #create_policy_rule_pycl(args.volume_name, args.vserver_name, args.qtree_name, args.user_name, args.space_hard, args.file_hard)
    create_qos_policy_pycl(args.vserver_name, args.qos_policy_name)
