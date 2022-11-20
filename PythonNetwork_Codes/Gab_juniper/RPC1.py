from jnpr.junos import Device
from lxml import etree

with Device(host="192.168.137.100", user="lab", password="lab123") as dev:
    sw_info_text = dev.rpc.get_lldp_neighbors_information({'format': 'text'})
    print(etree.tostring(sw_info_text, encoding='unicode'))