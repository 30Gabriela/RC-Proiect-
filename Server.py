import socket
import struct
import threading
import time

import Local_network
import DNS_Question
from Device import Device

multicast_group = '224.3.29.71'
mlt_group=('224.3.29.71',5353)
class UDP:
    def __init__(self):
        self.mDNS_port = 5353
        self.mDNS_address = '224.0.0.251'
        self.address='192.168.75.1'
        self.local_address= '127.0.0.1'  #'192.168.60.220'
        self.send_port=20001
        self.port=10000
        self.receive_port=10001
        self.clients=[]
        self.clients_address=[]
        self.running=False
        self.local_network=None

        try:
            # Creare socket UDP
            self.server_send=self.multicast_socket(self.port)
            ttl = struct.pack('b', 10)
            self.server_send.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, ttl)
            print("UDP server up and listening")
        except BaseException as error:
            print("Error: " + str(error))

    def multicast_socket(self,port):
        server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
        server.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        return server

    def start(self):
        try:
            start_thread = threading.Thread(target=self.receive_server)
            start_thread.start()
            print("Se porneste thread ul pentru receive")
        except:
            print("Eroare la pornirea thread‐ului")

    def registerDevice(self,name):
        self.notify_server=0
        try:
            print(f"\nSe va inregistra un nou device cu numele: {name}")
            # adaugam un nou dispozitiv
            newDevice = Device(str(name))
            self.clients.append(newDevice)
            print(f"Lista cu dispozitivele conectate: {self.clients}")
            self.local_network.register_device(newDevice)
            self.notify_server=1
        except Exception as err:
            print(err)

        if self.notify_server==1:
            self.send_all()
            self.notify_server=0

    def receive_server(self):
        msgFromServer = "Server started"
        bytesToSend = str.encode(msgFromServer)
        bufferSize=1024

        while True:
            print("Server waiting for receive....")
            try:
                bytesAddressPair = self.server_send.recvfrom(bufferSize)
                print(bytesAddressPair)
            except Exception as err:
                print(err)
            #message = bytesAddressPair[0]
            #address = bytesAddressPair[1]
            #print(bytesAddressPair)
            #self.clients_address.append(address)
            #print(address)
            #clientMsg = "Serverul a primit de la Client:{}".format(message)
            #clientIP = "Client IP Address:{}".format(address)
            #print(clientMsg)
            #print(clientIP)

            # Sending a reply to client
            #self.server_send.sendto(bytesToSend, address)
            self.server_send.sendto(bytesToSend, (multicast_group,self.port))

    def send_all(self):
        time.sleep(1)
        #o functie care va trimite un mesaj tuturor dispozitivelor conectate
        print("\nServer sends a broadcast message")
        msgFromServer = "Here is the server. This message is for all connected devices!"
        try:
            msgFromClient = DNS_Question.DNS_Question(DNS_Question.DNS_Question.TYPE_A,
                                              DNS_Question.DNS_Question.QCLASS_INTERNET,
                                                  "myPersonalPc.local").get_dns_question()
        except Exception as err:
            print(err)
        bytesToSend = str.encode(msgFromServer)
        #self.server_send.sendto(bytesToSend,mlt_group)
        self.server_send.sendto(msgFromClient, mlt_group)

    def set_local_network(self,network):
        self.local_network=network