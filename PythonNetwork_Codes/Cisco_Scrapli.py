from datetime import datetime
from scrapli.driver.core import IOSXEDriver

my_time = datetime.now().strftime("%H:%M:%S")

command_to_send = input ("Enter your command: ")

MY_DEVICE = {
    "host": "192.168.137.131",
    "auth_username": "lab",
    "auth_password":  "lab123",
    "auth_strict_key":  False,
     "ssh_config_file": "ssh_config",
}

with IOSXEDriver(**MY_DEVICE) as conn:
    response = conn.send_command(command_to_send)

my_list =response.result.splitlines()

with open(f"{command_to_send}-{my_time}.txt", "x") as f:
    for line in my_list:
        f.write(line + "\n")

    