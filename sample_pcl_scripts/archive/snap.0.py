#! /usr/bin/env python3

"""
ONTAP REST API Python Sample Scripts

Purpose: Script to create snapshot using the netapp_ontap library.
         It will also create a policy for the snapshot.
         It will also create a schedule for the policy.

Usage: snap.py [-h] -c CLUSTER -v VOLUME_NAME -s SNAPSHOT_NAME -vs VSERVER_NAME
                    -sc SCHEDULE_NAME, -p POLICY_NAME, [-u API_USER] [-p API_PASS]
create_snap.py: The following arguments are required: -c/--cluster, -v/--volume_name
                -s/--snapshot_name -vs/--vserver_name, -sc/--schedule_name, -sp/--policy_name
"""

import argparse
from getpass import getpass
import logging

from netapp_ontap import config, HostConnection, NetAppRestError
from netapp_ontap.resources import Volume, Snapshot, SnapshotPolicySchedule, SnapshotPolicy

def make_snap_pycl(vol_name: str, snapshot_name: str) -> None:
    """Create a new snapshot with default settings for a given volume"""

    volume = Volume.find(name=vol_name)
    snapshot = Snapshot(volume.uuid, name=snapshot_name)

    try:
        snapshot.post()
        print("Snapshot %s created successfully" % snapshot.name)
    except NetAppRestError as err:
        print("Error: Snapshot was not created: %s" % err)
    return

def create_snapshot_policy_pycl(policy_name: str, vserver_name: str, schedule_name: str) -> None:
    """Creates a Snapshot copy policy"""

    data = {
        'name': policy_name,
        'svm': {'name': vserver_name},
        'comment': 'Snapshot Copy Policy',
        'copies': [{'schedule': {'name': schedule_name}, 'count': '5'}]
    }

    snapshotpolicy = SnapshotPolicy(**data) 
    
    try:
        snapshotpolicy.post()
        print("Snapshot policy %s created successfully" % snapshotpolicy.name)
    except NetAppRestError as err:
        print("Error: Snapshot policy was not created: %s" % err)
    return

def create_snapshot_schedule_pycl(policy_name: str, schedule_name: str) -> None:
    """Adding schedule to a snapshot copy policy"""

    schedule1 = SnapshotPolicySchedule.find(name=schedule_name)
    policy = SnapshotPolicy.find(name=policy_name)
    snapshotpolicyschedule = SnapshotPolicySchedule(policy.uuid, count =5, prefix='new_weekly', schedule=schedule1)
   
    try:
        snapshotpolicyschedule.post()
        print("Snapshot schedule %s created successfully" % snapshotpolicyschedule.name)
    except NetAppRestError as err:
        print("Error: Snapshot schedule was not created: %s" % err)
    return

def parse_args() -> argparse.Namespace:
    """Parse the command line arguments from the user"""

    parser = argparse.ArgumentParser(
        description="This script will create a new snapshot for an existing ONTAP volume"
    )
    parser.add_argument(
        "-c", "--cluster", required=True, help="API server IP:port details"
    )
    parser.add_argument(
        "-v", "--volume_name", required=True, help="Volume to create"
    )
    parser.add_argument(
        "-s", "--snapshot_name", required=True, help="Snapshot to create"
    )
    parser.add_argument(
        "-sp", "--policy_name", required=True, help="Snapshot Policy to create"
    )
    parser.add_argument(
        "-sc", "--schedule_name", required=True, help="Snapshot Policy Schedule to create"
    )
    parser.add_argument(
        "-vs", "--vserver_name", required=True, help="VServer name to create Snapshot copy"
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

    make_snap_pycl(args.volume_name, args.snapshot_name)
    create_snapshot_policy_pycl(args.policy_name, args.vserver_name, args.schedule_name)
    create_snapshot_schedule_pycl(args.policy_name, args.schedule_name)
