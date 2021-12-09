import socket
import threading

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
            print("S-a creat un socket pentru device........")
        except BaseException as error:
            print("Error " + error)
            raise

        try:
            receive_thread = threading.Thread(target=self.device_receive)
            receive_thread.start()
            print("Se porneste thread ul pentru receive din device")
        except:
            print("Eroare la pornirea thread‐ului")

    def device_receive(self):
        msgFromClient = "Hello UDP Server"
        bytesToSend = str.encode(msgFromClient)
        self.s.sendto(bytesToSend, serverAddressPort)
        while 1:
            msgFromServer = self.s.recvfrom(1024)
            msg = f"\nMessage from Server for Device {self.router_address}: {msgFromServer[0]}"
            print(msg)

    def set_router_address(self,IP):
        self.router_address=IP


    def close(self):
        #inchide conexiunea
        self.s.close()
