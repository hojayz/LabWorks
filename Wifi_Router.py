import sys
import csv
from datetime import datetime
from jnpr.junos import  Device
from jnpr.junos.op.ospf import OspfNeighborTable
from jnpr.junos.op.phyport import PhyPortErrorTable, PhyPortTable
from prettytable import PrettyTable
from getpass import getpass
import os

# Check for module dependencies:
not_installed_modules = []

try:
    from jnpr.junos import Device
except ImportError:
    not_installed_modules.append("PyEz")

try:
    from prettytable import PrettyTable
except ImportError:
    not_installed_modules.append("prettytable")

if not_installed_modules:
    print("Please install following Python modules:")

    for module in not_installed_modules:
        print(f" .   {module}")

    sys.exit(1)

if not os.path.exists("Reports"):
    os.makedirs("Reports")
   
host = None
uname = None
pw = None

if uname == None:
    uname = input("Username: ")

if pw == None:
    pw = getpass()

filename = "MyList.csv"

# def csv_file():

#     filename= "./reports/{}.csv".format(
#     datetime.now().strftime("{}_%Y_%m_%d_{}_%H_%M_%S".format("Date", "Time"))
#     )
#     compliance_file = open(filename, "w")
#     with compliance_file:
#         headers = ["SN","Device Name","Device IP","OSPF Adjacency Age","Uplink Stability","Uplink Port Tx Error","Uplink Port Rx Error"]
#         writer = csv.DictWriter(
#             compliance_file,
#             fieldnames=headers,
#             delimiter=",",
#             quoting=csv.QUOTE_MINIMAL,
#             lineterminator="\n\n",
#         )
#         writer.writeheader()

def OspfLinkAge(dev, int):
    adj =OspfNeighborTable(dev).get(int)
    for spf in adj:
        OspfAge =spf.neighbor_adjacency_time
                
        return OspfAge
        

def FlapInt(dev, int):
    flap =PhyPortTable(dev).get(int)
    for itf in flap:
        IntFlap = itf.flapped

        return IntFlap

def IntError(dev, int):
    Int = PhyPortErrorTable(dev).get(int)
    for itf in Int:
        Tx_Int =itf.tx_err_drops
        Rx_int = itf.rx_err_drops
    return  Tx_Int, Rx_int

  
def main():
    filename= "./Reports/{}.csv".format(
    datetime.now().strftime("{}_%Y_%m_%d_{}_%H_%M_%S".format("Date", "Time"))
    )
    file = open(filename, "x")
    with file:
        headers = ["SN","Device Name","Device IP", "Uplink Interface", "OSPF Adjacency Age","Uplink Stability","Uplink Port Tx Error","Uplink Port Rx Error"]
        writer = csv.DictWriter(
            file,
            fieldnames=headers,
            delimiter=",",
        )
        writer.writeheader()

        table = PrettyTable()
        table.field_names =["SN","Device Name","Device IP", "Uplink Interface", "OSPF Adjacency Age","Uplink Stability","Uplink Port Tx Error","Uplink Port Rx Error"]   
        with open("Device_list.csv") as f:
            file =csv.DictReader(f, skipinitialspace=True)
            for row in file:
                host=row['Device IP']
                int=row['Uplink Interface'] 
                sn =row["SN"]
                with Device(host=host, user=uname, password=pw) as dev:
                    Devicename =dev.facts["hostname"]
                    OspfAge = OspfLinkAge(dev, int)
                    UplinkFlap =FlapInt(dev, int)
                    TxErr, RxErr =IntError(dev, int)

                    table.add_row([sn, Devicename, host, int, OspfAge, UplinkFlap, TxErr, RxErr])
                   
                    writer.writerow({"SN": sn , "Device Name": Devicename, "Device IP": host, "Uplink Interface": int, "OSPF Adjacency Age": OspfAge, "Uplink Stability": UplinkFlap,  "Uplink Port Tx Error": TxErr, "Uplink Port Rx Error": RxErr })
        
        print(table)
        print("Currently Generating CSV Report...")
        print("Filename: {}".format(filename))

if __name__ == "__main__":
    main()