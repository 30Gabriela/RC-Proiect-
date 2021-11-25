#pentru reteaua locala, adrese IP: 169.254.0.0/16
from Local_network import Local
class Device:
    def __init__(self,domain_name):
        self.router_address=''
        self.subnet_mask=''
        self.port=0
        self.domain_name=domain_name
        self.services=[] #o lista in care se vor inregistra serviciile oferite

    def set_router_address(self,IP):
        self.router_address=IP
