#pentru reteaua locala, adrese IP: 169.254.0.0/16
#Device-urile vor fi clientii care se vor conecta la server

from Local_network import Local
import socket
import time

serverAddressPort = ("127.0.0.1", 20001)

class Device:
    def __init__(self,domain_name):
        self.router_address=''
        self.subnet_mask=''
        self.port=0
        self.domain_name=domain_name
        self.services=[] #o lista in care se vor inregistra serviciile oferite
        self.multicast_address='244.0.0.251'    #???
        self.mDNS_port=5353
        self.thread=None

        try:
            self.s = socket.socket(socket.AF_INET, type=socket.SOCK_DGRAM)
            print("Se creeaza un socket pentru device........")
        except BaseException as error:
            print("Error " + error)
            raise

    def set_router_address(self,IP):
        self.router_address=IP


    def close(self):
        #inchide conexiunea
        self.s.close()
