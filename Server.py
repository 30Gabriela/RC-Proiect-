import socket
import struct
import threading
import time

import Local_network
import DNS_Question
import DNS_Answer
from Device import Device

multicast_group=('224.3.29.71',5353)
class UDP:
    def __init__(self):
        self.mDNS_port = 5353
        self.mDNS_address = '224.0.0.251'
        self.address='224.3.29.71'
        self.local_address= '127.0.0.1'  #'192.168.60.220'
        self.receive_port=20001
        #self.receive_port=10000
        self.port=10000
        #self.receive_port=10001
        self.clients=[]
        self.clients_address=[]
        self.running=False
        self.local_network=None
        self.servers_receive=[]

        try:
            # Creare socket UDP
            self.server_send=self.multicast_socket()
            ttl = struct.pack('b', 10)
            self.server_send.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, ttl)
            print("UDP server(used for sending messages) up")

            self.server_receive=self.multicast_socket()
            self.server_receive.bind(('127.0.0.1',self.receive_port))
        except BaseException as error:
            print("Error: " + str(error))

    def multicast_socket(self):
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
            #print(f"Lista cu dispozitivele conectate: {self.clients}")
            self.local_network.register_device(newDevice)
            self.notify_server=1
            #server=self.multicast_socket()
            add=newDevice.get_router_address()
            port=newDevice.get_port()
            print(add,port)
            #server.bind((add,port))
            #self.servers_receive.append(server)
            #thread1=threading.Thread(target=self.receive_server,args=index_socket)
            #thread1.start()
        except Exception as err:
            print(err)

        if self.notify_server==1:
            msg=f"S-a inregistrat device-ul cu numele {name}"
            self.send_all(msg)
            self.notify_server=0

    def receive_server(self):
        #print(server_receive)
        msgFromServer = "Server started"
        bytesToSend = str.encode(msgFromServer)
        bufferSize=1024

        while True:
            print("Server waiting for receive....")
            try:
                message, address = self.server_receive.recvfrom(bufferSize)
                print(f"Server receives: {message}....pe interfata {address}")
                self.clients_address.append(address)
                print(self.clients_address)
            except Exception as err:
                print(err)
                print("Server")

            # Sending a reply to client
            #self.server_send.sendto(bytesToSend, address)

    def send_all(self,msg):
        time.sleep(1)
        print(msg)
        #o functie care va trimite un mesaj tuturor dispozitivelor conectate
        print("\nServer sends a broadcast message")
        msgFromServer = "Here is the server. This message is for all connected devices!"
        try:
            #msgFromClient = DNS_Question.DNS_Question(DNS_Question.DNS_Question.TYPE_A, DNS_Question.DNS_Question.QCLASS_INTERNET, "myPersonalPc.local").get_dns_question()
            msgFromClient=DNS_Answer.DNS_Answer(DNS_Answer.DNS_Answer.TYPE_A, DNS_Answer.DNS_Answer.CLASS_INTERNET, "MyPersonalPC.local").get_dns_response('192.168.0.9')
        except Exception as err:
            print(err)
        bytesToSend = str.encode(msgFromServer)
        #self.server_send.sendto(bytesToSend,mlt_group)
        self.server_send.sendto(msgFromClient, multicast_group)

    def set_local_network(self,network):
        self.local_network=network