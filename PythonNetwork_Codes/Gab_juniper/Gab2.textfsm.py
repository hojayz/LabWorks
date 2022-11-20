""" This is a Junos Script for Shell Operations
"""


from cgi import print_arguments
from distutils.version import Version
from jnpr.junos import Device
from jnpr.junos.utils.start_shell import StartShell
from jnpr.junos.exception import ConnectError
from jnpr.junos.factory.factory_loader import FactoryLoader
from rich import print as rprint
import yaml


yaml_data="""
---
junos_lldp_neighbors_detail_table:
  rpc: get-lldp-neighbors-information
  args:
    interface_name: '[afgx]e*'
  item: lldp-neighbor-information
  key: lldp-local-port-id
  view: junos_lldp_neighbors_detail_view

junos_lldp_neighbors_detail_view:
  fields:
    interface: lldp-local-port-id
    parent_interface: lldp-local-parent-interface-name
    remote_port: lldp-remote-port-id
    remote_chassis_id: lldp-remote-chassis-id
    remote_port: lldp-remote-port-id
    remote_port_description: lldp-remote-port-description
    remote_system_name: lldp-remote-system-name
    remote_system_description: lldp-system-description/lldp-remote-system-description
    remote_system_capab: lldp-remote-system-capabilities-supported
    remote_system_enable_capab: lldp-remote-system-capabilities-enabled
"""


# print(f"Creating network device instance................\n")
with Device(host="192.168.137.100", user="lab", password="lab123") as dev:
#     print(f"Network device instance for {dev.facts['hostname']} successful...... \n")
#     print(f"Creating Junos Shell instance for {dev.facts['hostname']} \n")
    globals().update(FactoryLoader().load(yaml.load(yaml_data)))
    lldp = junos_lldp_neighbors_detail_table(dev)
    lldp.get()

# Get list of interfaces
    interfaces = lldp.get().keys()

    lldp.GET_RPC = 'get-lldp-interface-neighbors'

# Get details of each interface
    for interface in interfaces:
        lldp.get(interface)
        for item in lldp:
          print ('Remote system description: ', item.remote_system_description)
          print ("Remote system capabiltiy:", item.remote_system_capab)
        

    
    # with StartShell(dev) as ss:
    #     print(f"Junos shell instance for {dev.facts['hostname']} successful...... \n")
    #     version = ss.run('cli -c "show lldp neigh | no-more "')
    #     print("*" * 40 + f"  Junos version details running on {dev.facts['hostname']}  "   + "*" * 40 + "\n")
    #     for line in version:
    #         rprint(line)
    #     print(type(version))
    
    







        
    
