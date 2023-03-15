import Netmiko
import re
from pprint import pprint

conn = Netmiko.ConnectHandler('10.254.0.1', username='cisco,
    password='cisco', device_type='cisco_ios')

sh_ip_int_br =conn.send_command('show ip int brief')

interface_pattern = r'(GigabitEthernet[1-9])\s'
status_pattern = r'GigabitEthernet[1-9]\s.*?|up\administratively down\down)'

interface_names =re.findall(interface_pattern, sh_ip_int_br)
interface_statuses = re.findall(status_pattern, sh_ip_int_br)

interface_dict = dict(zip(interface_names, interface_statuses))

print(interface_names)
print(interface_statuses)
pprint(interface_dict)