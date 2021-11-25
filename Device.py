#pentru reteaua locala, adrese IP: 169.254.0.0/16
#Device-urile vor fi clientii care se vor conecta la server

from Local_network import Local
import socket
import time

# Creaza un socket IPv4, TCP
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# Conectare la serverul care asculta pe portul 5000
s.connect(('127.0.0.1', 5001))

class Device:
    def __init__(self,domain_name):
        self.router_address=''
        self.subnet_mask=''
        self.port=0
        self.domain_name=domain_name
        self.services=[] #o lista in care se vor inregistra serviciile oferite
        self.multicast_address='244.0.0.251'    #???
        self.mDNS_port=5353

        # Creaza un socket IPv4, TCP
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # Conectare la serverul care asculta pe portul 5000
        self.s.connect(('127.0.0.1', 5000))

    def set_router_address(self,IP):
        self.router_address=IP


    def close(self):
        #inchide conexiunea
        self.s.close()
