from scrapli.driver.core import IOSXEDriver

command  = input("Enter your command: ")

my_device = [
    {
        "host" : "192.168.137.137",
        "auth_username" : "lab",
        "auth_password" : "lab123",
        "ssh_config_file": "ssh_config",
        "auth_strict_key":  False,
    },
    {
        "host" : "192.168.137.139",
        "auth_username" : "lab",
        "auth_password" : "lab123",
        "ssh_config_file": "ssh_config",
        "auth_strict_key":  False,  
    }   
]

for device in my_device:
    with IOSXEDriver(**device) as conn:
        response = conn.send_command(command)
    print(response.result)
    print("\n")



