import socket
import struct
import threading

import DNS_Question
import Header_DNS_packet

serverAddressPort = ("127.0.0.1", 20002)
multicast_group=('224.3.29.71',5353)
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
            self.server_receive = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
            self.server_receive.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
            self.server_receive.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            #print(self.server_send)
            ttl = struct.pack('b', 1)
            self.server_receive.bind(('',5353))


            group = socket.inet_aton('224.3.29.71')
            mreq = struct.pack('4sL', group, socket.INADDR_ANY)
            self.server_receive.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)
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

    def multicast_socket(self,port):
        server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
        server.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        #ttl=struct.pack('b',6)
        #server.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, ttl)
        #loop = struct.pack(b'B', 1)
        #server.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_LOOP, loop)
        server.bind(('', port))
        return server

    def device_receive(self):
        msgFromClient = "Hello UDP Server"
        msgFromClient=DNS_Question.DNS_Question(DNS_Question.DNS_Question.TYPE_A,
                                                DNS_Question.DNS_Question.QCLASS_INTERNET,"myPersonalPc.local").get_dns_question()
        #bytesToSend = str.encode(msgFromClient)
        #bytesToSend=msgFromClient
        #self.server_send.sendto(bytesToSend, multicast_group)
        while 1:
            msgFromServer = self.server_receive.recvfrom(1024)
            msg = f"Device-ul {self.router_address} a primit de la server : {msgFromServer[0]}"
            print(msg)
            msgFromClient = "akg"
            bytesToSend = str.encode(msgFromClient)
            #self.server_receive.sendto(bytesToSend, multicast_group)

    def set_router_address(self,IP):
        self.router_address=IP


    def close(self):
        #inchide conexiunea
        self.s.close()
