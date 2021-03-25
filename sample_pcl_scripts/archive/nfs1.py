#! /usr/bin/env python3

"""
Purpose: Script to create sn SVM by using the netapp_ontap library.
         It will create a Data Interface, Network Default, Gateway.
         It will also create a DNS Domain, CIFS Server and CIFS Share.

Usage: nfs.py [-h] -c CLUSTER -a AGGR_NAME, -vs VSERVER_NAME, -ip DATA_LIF, -g GATEWAY, -d DOMAIN, -s SEVER_IP,
                    -nm NET_MASK -se NFS_SERVER, -sh EXPORT_PATH, [-u API_USER] [-p API_PASS]
python3.7 nfs.py: -c cluster -a aggr_name, -vs/--vserver_name, -ip/--ip_address, -g/--gateway_ip, -d/--domain,
                -s/--server_ip, -nm/--net_mask -se/--nfs_server, -sh/--nfs_path
"""

import argparse
from getpass import getpass
import logging
from typing import Optional

from netapp_ontap import config, utils, HostConnection, NetAppRestError
from netapp_ontap.resources import Svm, IpInterface, NetworkRoute , Dns, NfsService, ExportPolicy, KerberosRealm, KerberosInterface, NfsClients, ExportClient, ExportRule

def create_svm(vserver_name: str, aggr_name: str) -> None:
    """Create an SVM on the specified aggregate"""

    svm = Svm.from_dict({
    'name': vserver_name,
    'aggregates': [{'name': aggr_name}],
    'nfs': {'enabled': "true"}
    })

    try:
        svm.post()
        print("SVM %s created successfully" % svm.name)
    except NetAppRestError as err:
        print("Error: SVM was not created: %s" % err)
    return

def create_data_interface(vserver_name: str, ip_address: str, ip_netmask) -> None:
    """Creates an SVM-scoped IP Interface"""

    data = {
        'name': 'Data1',
        'ip': {'address': ip_address, 'netmask': ip_netmask},
        'enabled': True,
        'scope': 'svm',
        'svm': {'name': vserver_name},
        'location': {
           'auto_revert': True,
           'broadcast_domain': {'name': 'Default'},
        }
    }

    ip_interface = IpInterface(**data)

    try:
        ip_interface.post()
        print("Ip Interface %s created successfully" % ip_interface.ip.address)
    except NetAppRestError as err:
        print("Error: IP Interface was not created: %s" % err)
    return

def create_route(vserver_name: str, net_gateway_ip: str) -> None:
    """Creates a network route"""
    """The default destination will be set to "0.0.0.0/0" for IPv4 gateway addresses""" 

    data = {
        'gateway': net_gateway_ip,
        'svm': {'name': vserver_name}
    }

    route = NetworkRoute(**data)

    try:
        route.post()
        print("Route %s created successfully" % route.gateway)
    except NetAppRestError as err:
        print("Error: IP Interface was not created: %s" % err)
    return

def create_dns(vserver_name: str, domain: str, dns_server_ip: str) -> None:
    """Creates a DNS server"""

    data = {
        'domains': [domain],
        'servers': [dns_server_ip],
        'svm': {'name': vserver_name}
    }

    dns = Dns(**data)

    try:
        dns.post()
        print("Route %s created successfully" % dns.domains)
    except NetAppRestError as err:
        print("Error: IP Interface was not created: %s" % err)
    return

def create_nfs_server(vserver_name: str, domain_name: str, nfs_server: str, server_ip: str) -> None:
    """Creates a NFS server"""

    SVM = Svm.find(name=vserver_name)

    data = {
        'scope': 'svm',
        'svm': {'name': vserver_name, 'uuid': SVM.uuid},
        'protocol': {'v4_id_domain': domain_name},
        'enabled': 'True'
    }

    nfs_service = NfsService(**data)

    try:
        nfs_service.post()
        print("NFS Server %s created successfully" % nfs_service.name)
    except NetAppRestError as err:
        print("Error: NFS Server was not created: %s" % err)
    return

def create_export_policy(ex_path: str, host_name: str) -> None:
    """Creates an export policy for an SVM"""
    
    data = {
        'name': ex_path,
        'rules': [
            {
                'clients': [{'match': host_name}],'ro_rule': ['unix'], 'rw_rule': ['ntlm'], 'anonymous_user': 'any',
            },
            {
                'clients': [{'match': host_name}],'ro_rule': ['unix'], 'rw_rule': ['ntlm'], 'superuser': ['any'],
            }
        ] 
    }

    export_policy = ExportPolicy(**data)

    try:
        export_policy.post()
        print("Export Policy for NFS Server %s created successfully" % export_policy.name)
    except NetAppRestError as err:
        print("Error: Export Policy was not created: %s" % err)
    return

def parse_args() -> argparse.Namespace:
    """Parse the command line arguments from the user"""

    parser = argparse.ArgumentParser(
        description="This script will create a new CIFS Share for a given VServer"
    )
    parser.add_argument(
        "-c", "--cluster", required=True, help="API server IP:port details"
    )
    parser.add_argument(
        "-a", "--aggr_name", required=True, help="Aggregate name"
    )
    parser.add_argument(
        "-vs", "--vserver_name", required=True, help="VServer name to create CIFS Share"
    )
    parser.add_argument(
        "-ip", "--ip_address", required=True, help="Data Interface IP Address"
    )
    parser.add_argument(
        "-g", "--gateway_ip", required=True, help="Default Gateway IP Address"
    )
    parser.add_argument(
        "-d", "--domain", required=True, help="DNS DOmain Name"
    )
    parser.add_argument(
        "-s", "--server_ip", required=True, help="DNS Server IP Address"
    )
    parser.add_argument(
        "-nm", "--ip_netmask", required=True, help="DNS Server IP Address"
    )
    parser.add_argument(
        "-se", "--nfs_server", required=True, help="NFS Server"
    )
    parser.add_argument(
        "-sh", "--ex_path", required=True, help="Export Path"
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
    #    level=logging.DEBUG,
        level=logging.INFO,
        format="[%(asctime)s] [%(levelname)5s] [%(module)s:%(lineno)s] %(message)s",
    )

    #utils.LOG_ALL_API_CALLS = 1

    args = parse_args()
    config.CONNECTION = HostConnection(
        args.cluster, username=args.api_user, password=args.api_pass, verify=False,
    )

    #create_svm(args.vserver_name, args.aggr_name)
    create_data_interface(args.vserver_name, args.ip_address, args.ip_netmask)
    create_route(args.vserver_name, args.gateway_ip)
    create_dns(args.vserver_name, args.cluster, args.server_ip)
    create_nfs_server(args.vserver_name, args.domain, args.nfs_server, args.server_ip)
    create_export_policy(args.ex_path, args.vserver_name)
