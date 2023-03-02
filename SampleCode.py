import sys
import csv
from datetime import datetime
from jnpr.junos import Device
from jnpr.junos.op.ospf import OspfNeighborTable
from jnpr.junos.op.phyport import PhyPortErrorTable, PhyPortTable
from prettytable import PrettyTable
from getpass import getpass
from jnpr.junos.exception import ConnectError
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


host = None
uname = None
pw = None

if uname == None:
    uname = input("Username: ")

if pw == None:
    pw = getpass()

filename = "MyList.csv"


def OspfLinkAge(dev, int):

    """This function returns OSPF neighborship age. """

    adj = OspfNeighborTable(dev).get(int)
    for spf in adj:
        OspfAge = spf.neighbor_adjacency_time

        return OspfAge


def FlapInt(dev, int):

    """This function returns number of times intf flapped. """

    flap = PhyPortTable(dev).get(int)
    for itf in flap:
        IntFlap = itf.flapped

        return IntFlap


def IntError(dev, int):

    """This function returns Tx  and Rx interface errors. """

    Int = PhyPortErrorTable(dev).get(int)
    for itf in Int:
        Tx_Int = itf.tx_err_drops
        Rx_int = itf.rx_err_drops
        Rx_fr = itf.rx_err_frame
        Rx_dr = itf.rx_err_drops
        Tx_dr = itf.tx_err_drops
    return Tx_Int, Rx_int, Rx_fr, Rx_dr, Tx_dr

# Check if Reports folder exists, else create it.
if not os.path.exists("Reports"):
    os.mkdir("Reports")


def main():
    filename = "./Reports/{}.csv".format(
        datetime.now().strftime("{}_%Y_%m_%d_{}_%H_%M_%S".format("Date", "Time"))
    )
    file = open(filename, "x")
    with file:
        headers = [
            "SN",
            "Device Name",
            "Device IP",
            "Device Uptime",
            "Intf",
            "OSPF Adj",
            "Uplink Last Flapped",
            "Tx Error",
            "Rx Error",
            "Frame Err",
            "Tx Drp",
            "Rx Drp",
        ]

        writer = csv.DictWriter(
            file,
            fieldnames=headers,
            delimiter=",",
        )
        writer.writeheader()

        table = PrettyTable()
        table.field_names = [
            "SN",
            "Device Name",
            "Device IP",
            "Device Uptime",
            "Intf",
            "OSPF Adj",
            "Uplink Last Flapped",
            "Tx Err",
            "Rx Err",
            "Frame Err",
            "Tx Drp",
            "Rx Drp",
        ]

        with open("Device_list.csv") as f:
            file = csv.DictReader(f, skipinitialspace=True)
            sn = 1
            for row in file:
                host = row["Device IP"]
                int = row["Uplink Interface"]
                try:
                    with Device(host=host, user=uname, password=pw) as dev:

                        Devicename = dev.facts["hostname"]
                        Sysuptime = dev.facts["RE0"]["up_time"]
                        OspfAge = OspfLinkAge(dev, int)
                        UplinkFlap = FlapInt(dev, int)
                        TxErr, RxErr, Fr_Err, Rx_dr, Tx_dr = IntError(dev, int)

                        table.add_row(
                            [
                                sn,
                                Devicename,
                                host,
                                Sysuptime,
                                int,
                                OspfAge,
                                UplinkFlap,
                                TxErr,
                                RxErr,
                                Fr_Err,
                                Rx_dr,
                                Tx_dr,
                            ]
                        )
                        writer.writerow(
                            {
                                "SN": sn,
                                "Device Name": Devicename,
                                "Device IP": host,
                                "Device Uptime": Sysuptime,
                                "Intf": int,
                                "OSPF Adj": OspfAge,
                                "Uplink Last Flapped": UplinkFlap,
                                "Tx Error": TxErr,
                                "Rx Error": RxErr,
                                "Frame Err": Fr_Err,
                            }
                        )

                        sn += 1
                except ConnectError as err:
                    print("Cannot connect to device: {0}".format(err))
                    pass
                except Exception as err:
                    print(err)
                    pass

        print(table)
        print("Currently Generating CSV Report...")
        print("Filename: {}".format(filename))


if __name__ == "__main__":
    main()
