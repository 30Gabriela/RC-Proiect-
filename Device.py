import socket
import struct
import threading
import time

import DNS_Question
import Header_DNS_packet

server_address='127.0.0.1'
multicast_group=('224.3.29.71',5353)
class Device:
    def __init__(self,domain_name):
        self.router_address=''
        self.subnet_mask='255.255.255.0'
        self.port=0
        self.domain_name=domain_name
        self.services=[] #o lista in care se vor inregistra serviciile oferite
        self.multicast_address='244.0.0.251'    #???
        self.mDNS_port=5353
        self.thread=None

        try:
            self.server_receive = self.multicast_socket()
            self.server_receive.bind(('',self.mDNS_port))
            group = socket.inet_aton('224.3.29.71')
            mreq = struct.pack('4sL', group, socket.INADDR_ANY)
            self.server_receive.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)
            print("S-a creat un socket_receive pentru device........")
        except BaseException as error:
            print("Error " + error)

        try:
            receive_thread = threading.Thread(target=self.device_receive)
            receive_thread.start()
            print("Se porneste thread ul pentru receive din device")
        except:
            print("Eroare la pornirea thread‐ului")

    def multicast_socket(self):
        server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
        server.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        #server.bind(('127.0.0.1', port))
        return server

    def device_receive(self):
        msgFromClient = "Hello UDP Server"
        #msgFromClient=DNS_Question.DNS_Question(DNS_Question.DNS_Question.TYPE_A,
        #                                        DNS_Question.DNS_Question.QCLASS_INTERNET,"myPersonalPc.local").get_dns_question()
        bytesToSend = str.encode(msgFromClient)
        #bytesToSend=msgFromClient
        #self.server_send.sendto(bytesToSend, multicast_group)
        while 1:
            try:
                msgFromServer = self.server_receive.recvfrom(1024)
                msg = f"Device-ul {self.router_address} a primit de la server : {msgFromServer[0]}"
                print(msg)
                time.sleep(1)
                self.device_send("Am primit salutul")
            except Exception as err:
                print(err)

    def device_send(self, msg):
        try:
            self.server_send.sendto(str.encode(msg),('127.0.0.1',self.port))
        except Exception as err:
            print(err)
        #self.server_send.sendto(str.encode(msg), (self.router_address, self.port))

    def set_router_address(self,IP):
        self.router_address=IP

    def set_port(self,port):
        self.port=port
        self.server_send = self.multicast_socket()
        try:
            self.server_send.bind((server_address,self.port))
        except Exception as err:
            print(err)
            print("device..........")

    def get_router_address(self):
        return self.router_address

    def get_port(self):
        return self.port

    def close(self):
        #inchide conexiunea
        self.s.close()
