"""
The Maintenance module simplifies custom network routine checks carried out on
critical Data Center devices - IP Fabric Leaf(s) and Spines both in HQ and DR
locations.

Checks covered includes:
    * Hardware - Interface Errors, Interface Flaps, Interface Queue Drops.
    * Software - System Processes Crash, 
    * Chassis - Chassis Errors & Failure

A report is produced at the end for review 

"""

#! /usr/bin/env python

from code import interact
from jnpr.junos import Device
from getpass import getpass
from jnpr.junos.exception import ConnectError
from jnpr.junos.utils.start_shell import StartShell
from pprint import pprint
import os
import sys



#   Input for number of interfaces and Interface types 

int_num = int(input("Enter number of interfaces supported on the platform: "))

#   Check for Aggregated Interfaces

#   Define a function to check interface Errors

print(f"defining function 'int_error_check' ...........")

def int_error_check(*args):                 # Interface Error Checking function
    print(f"Checking for interface errors on dev.facts['hostname']")
    for int in range(0, int_num):
        # print(f"show interfaces ge-0/0/{int} extensive | match error")
        print('cli -c' + f" run show interfaces ge-0/0/{int} extensive | match error")

print(f"Defining function 'int_flap_check'........")
def int_flap_check(*args):                 # Interface Flap Checking function
    print(f"Checking for interface flap on dev.facts['hostname']")
    for int in range(0, int_num):
        # print(f"show interfaces ge-0/0/{int} extensive | match flap")
        print('cli -c' + f" run show interfaces ge-0/0/{int} extensive | match flap")

print(f"Connecting to network device.......")

with Device(host='192.168.137.100', user='lab', password='lab123') as dev:
    try:
        with StartShell(dev) as ss:
            print("*" * 10 + f" Performing maintenace operations on {dev.facts['hostname']}......." +  "*" * 10)
            print(f"Interface Error check on {dev.facts['hostname']}.............")
            core_dump = ss.run('cli -c  "run show system core-dump"')
            int_error = ss.run('cli -c  "show interfaces ge-0/0/0 extensive | match error"')
            log_error = ss.run('cli -c  "run show log messages | match error"')
            log_fail = (ss.run('cli -c  "run show log messages | match fail"')).textfsm_parse_out()
            #pprint(core_dump)
            #pprint(int_error)
            #pprint(log_error)
            pprint(log_fail)
           
            
            

    except ConnectError as err:
        print(err)
        print(f"Closing programe.....")
        sys.exit()

        
