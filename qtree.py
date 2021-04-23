#! /usr/bin/env python3.7

import argparse
from getpass import getpass
import logging

from netapp_ontap import config, HostConnection, NetAppRestError
from netapp_ontap.resources import Qtree, QuotaRule, QosPolicy

def create_qtree(qtree_name: str, volume_name: str, vserver_name: str) -> None:
    """Creates a new volume in a SVM"""
    print("Creating QTree...")
    data = {
        "name": qtree_name,
        "svm":      {    "name": vserver_name },
        "volume":   {    "name": volume_name }
    }

    qtree = Qtree(**data)

    try:
        qtree.post()
        print("qtree %s created successfully" % qtree.name)
    except NetAppRestError as err:
        print("qtree create: %s" % err)
    return

def make_qos_policy(vserver_name: str, qos_policy_name: str) -> None:
    print("Creating QOS Policy...")
    data = {
        "adaptive": 
        {
            "absolute_min_iops": 100,
            "expected_iops": 100,
            "peak_iops": 100
        },
        "name": qos_policy_name ,
        "svm": { "name": vserver_name }
    }

    qos = QosPolicy(**data)
    try:
        qos.post()
        print("qtree %s created successfully" % qos.name)
    except NetAppRestError as err:
        print("qos policy err: %s" % err)
    return

def create_policy_rule(user_name, space_hard_limit, files_hard_limit, qtree_name, volume_name, vserver_name) -> None:
    print("Creating Quota Rule...")
    data = {
        "files": {     "hard_limit": files_hard_limit       },
        "qtree": {     "name": qtree_name                   },
        "space": {     "hard_limit": space_hard_limit       },
        "svm":   {     "name": vserver_name                 },
        "type":        "user",
        "user_mapping": "off",
        "users": [{    "name": user_name                    }],
        "volume":{     "name": volume_name                  } 
    }

    qr = QuotaRule(**data)

    try:
        qr.post()
        print("quota rule for %s created successfully" % qtree_name)
    except NetAppRestError as err:
        print("Error: Quota Rule: %s" % err)
    return


def parse_args() -> argparse.Namespace:
    """Parse the command line arguments from the user"""

    parser = argparse.ArgumentParser(
        description="This script will create a new volume."
    )
    parser.add_argument(
        "-c", "--cluster", required=True, help="API server IP:port details"
    )
    parser.add_argument(
        "-v", "--volume_name", required=True, help="Volume to create qtree in"
    )
    parser.add_argument(
        "-q", "--qtree_name", required=True, help="qtree name"
    )
    parser.add_argument(
        "-vs", "--vserver_name", required=True, help="SVM to create the qtree in"
    )
    parser.add_argument(
        "-sh", "--space_hard_limit", required=True, help="qtree space hard limit"
    )
    parser.add_argument(
        "-fh", "--files_hard_limit", required=True, help="qtree file hard limit"
    )
    parser.add_argument(
        "-un", "--user_name", required=True, help="username for quota"
    )
    parser.add_argument(
        "-qos", "--qos_policy_name", required=True, help="name of qos policy to create"
    )
    parser.add_argument("-u", "--api_user",
                        default="admin", help="API Username")
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

    # Create a qtree
    create_qtree(args.qtree_name, args.volume_name, args.vserver_name)

    # Set qtree quota
    create_policy_rule(args.user_name, args.space_hard_limit, args.files_hard_limit, args.qtree_name, args.volume_name, args.vserver_name)
    
    # set qos policy
    make_qos_policy(args.vserver_name, args.qos_policy_name)
