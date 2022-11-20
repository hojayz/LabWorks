from scrapli.driver.core import IOSXEDriver
import json


command_to_send = input ("Enter your command: ")

MY_DEVICE = [
    {
    "host": "192.168.137.137",
    "auth_username": "lab",
    "auth_password":  "lab123",
    "auth_strict_key":  False,
     "ssh_config_file": "ssh_config",
    },
    {
    "host": "192.168.137.139",
    "auth_username": "lab",
    "auth_password":  "lab123",
    "auth_strict_key":  False,
     "ssh_config_file": "ssh_config",
    }
]
for device in MY_DEVICE:
    with IOSXEDriver(**device) as conn:
        response = conn.send_command(command_to_send)
    #print(dir(response))
     #structured_data = json.dumps(response.textfsm_parse_output(), indent=2)
    structured_data = response.textfsm_parse_output()
    for info in structured_data:
        # print(info["hostname"])
        # print(info["uptime"])
        # print(info["serial"])
        print(f"Router {info['hostname']} with the serial_num: {info['serial']} has uptime: {info['uptime']}")



    