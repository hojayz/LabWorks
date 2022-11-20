from scrapli.driver.core import JunosDriver
from getpass import getpass

uname = input("Enter your username: ")
passwd =getpass("Enter your password: ")

ED_devices = [
    { 
        "host": "102.88.7.174",
        "auth_username": uname,
        "auth_password": passwd,
        "auth_strict_key":  False,
        "ssh_config_file": "ssh_config",
    },
    {
        "host": "102.89.15.22",
        "auth_username": uname,
        "auth_password": passwd,
        "auth_strict_key":  False,
        "ssh_config_file": "ssh_config",
    }    
]

for device in ED_devices:
    with JunosDriver(**device) as conn:
        response =conn.send_command("show route 0/0 exact")
    structured_data =response.result
    print(structured_data)
    print("\n")
        