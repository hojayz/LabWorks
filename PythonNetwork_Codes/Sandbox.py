from datetime import datetime
from scrapli.driver.core import IOSXEDriver

my_time = datetime.now().strftime("%H:%M:%S")

command_to_send = input ("Enter your command: ")

MY_DEVICE = {
    "host": "sandbox-iosxe-recomm-1.cisco.com",
    "auth_username": "developer",
    "auth_password":  "C1sco12345",
    "port": 22,
    "ssh_config_file": "ssh_config",
}

with IOSXEDriver(**MY_DEVICE) as conn:
    response = conn.send_command(command_to_send)

my_list = response.result.splitlines()
print(my_list)