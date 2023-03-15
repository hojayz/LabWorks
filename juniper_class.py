from jnpr.junos import Device

user = 'failover'
password = 'P@ss2netz'

class Juniper:
    def __init__ (self,host):
        self.host = host
        

    def login(self):
        return Device(host = self.host, user = user, password =password)
        

henry_oroh_rtr = Juniper('102.89.15.22')

r1= henry_oroh_rtr.login()
r1.open()
print(r1.connected)
r1.close()