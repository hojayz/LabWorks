import netmiko
import re
from pprint import pprint

ip = "192.168.120.129"
username = 'lab'
password = "Lab123"
device_type = "cisco_ios"
port = "22"

net_connect = netmiko.ConnecHandler(ip=ip, device_type=device_type,
    username=username, password=password, port=port)
csr1kv1_ip_int_br =net_connect.send_command('sh ip int br')
print(csr1kv1_ip_int_br)
print(type(csr1kv1_ip_int_br))