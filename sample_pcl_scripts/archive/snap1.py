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
from typing import Optional

from netapp_ontap import config, HostConnection, NetAppRestError
from netapp_ontap.resources import Volume, Snapshot, SnapshotPolicy, Schedule

def make_snap_pycl(vol_name: str, snapshot_name: str) -> Optional[Snapshot]:
    """Create a new snapshot with default settings for a given volume"""

    volume = Volume.find(name=vol_name)
    snapshot = Snapshot(volume.uuid, name=snapshot_name)

    try:
        snapshot.post(hydrate=True)
        print("Snapshot %s created successfully\n%s" % (snapshot.name, snapshot))
        return snapshot
    except NetAppRestError as err:
        print("Error: Snapshot was not created: %s" % err)
    return None

def create_snapshot_policy_pycl(policy_name: str, vserver_name: str, schedule_name: str) -> Optional[SnapshotPolicy]:
    """Creates a Snapshot copy policy"""

    data = {
        'name': policy_name,
        'svm': {'name': vserver_name},
        'comment': 'Snapshot Copy Policy',
        'copies': [{'schedule': {'name': schedule_name}, 'count': '5'}]
    }

    snapshot_policy = SnapshotPolicy(**data)

    try:
        snapshot_policy.post(hydrate=True)
        print("Snapshot policy %s created successfully\n%s" % (snapshot_policy.name, snapshot_policy))
        return snapshot_policy
    except NetAppRestError as err:
        print("Error: Snapshot policy was not created: %s" % err)
    return None

def create_schedule_pycl(schedule_name: str) -> Optional[Schedule]:
    """Creating a schedule that will be used to create a snapshot policy"""

    try:
        schedule = Schedule(
            name=schedule_name, cron={"days": [1], "hours": [3], "minutes": [15]},
        )
        schedule.post(hydrate=True)
        print("Schedule %s created successfully\n%s" % (schedule.name, schedule))
        return schedule
    except NetAppRestError as err:
        print("Error: Shedule was not created: %s" % err)
    return None

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

    snapshot = make_snap_pycl(args.volume_name, args.snapshot_name)
    schedule = create_schedule_pycl(args.schedule_name)
    policy = create_snapshot_policy_pycl(args.policy_name, args.vserver_name, args.schedule_name)
