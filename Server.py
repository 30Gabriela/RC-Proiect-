import logging
logging.basicConfig(filename='LOGS.log',format='%(asctime)s----%(message)s', datefmt='%d/%m/%Y %I:%M:%S %p', level=logging.DEBUG)


import socket
import struct
import threading
import time

import Local_network
import DNS_Question
import DNS_Answer
import SRV_packet
from Device import Device
from Resolver import addDevices

multicast_group=('224.3.29.71',5353)
class UDP:
    def __init__(self):
        self.mDNS_port = 5353
        self.mDNS_address = '224.0.0.251'

        self.address='224.3.29.71'
        self.local_address= '127.0.0.1'  #'192.168.60.220'
        self.receive_port=20001

        self.clients=[]
        self.clients_address={}

        self.responds_sockets=[]

        self.interogate_name=0

        try:
            # Creare socket UDP
            self.server_send=self.create_socket()
            ttl = struct.pack('b', 10)
            self.server_send.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, ttl)
            logging.info('UDP server(used for sending messages) up')
            #print("UDP server(used for sending messages) up")
            loop = struct.pack(b'B', 1)
            self.server_send.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_LOOP, loop)

            self.server_receive=self.create_socket()
            self.server_receive.bind(('127.0.0.1',self.receive_port))

        except BaseException as error:
            logging.error('Server error: {}'.format(error))
            #print("Error: " + str(error))

    def create_socket(self):
        server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
        server.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        return server

    def start(self):
        try:
            start_thread = threading.Thread(target=self.receive_server)
            start_thread.start()
            logging.info('Se porneste thread ul pentru receive')
            #print("\nSe porneste thread ul pentru receive")
        except:
            logging.error('Eroare la pornirea thread‐ului')
            #print("Eroare la pornirea thread‐ului")

    def registerDevice(self,name):
        self.notify_server=0
        try:
            self.queried_name = 0
            logging.info('Se va inregistra un nou device cu numele {}'.format(name))
            #print(f"\nSe va inregistra un nou device cu numele: {name}")
            self.query_name(name)
            newDevice = Device(str(name))
            self.local_network.register_device(newDevice)

            self.clients.append(newDevice)
            # print(f"Lista cu dispozitivele conectate: {self.clients}")

            add=newDevice.get_router_address()
            port=newDevice.get_port()

            self.clients_address.update({name:add})
            logging.info('Dispozitivele inregistrate si adresele lor: {}'.format(self.clients_address))
            logging.info('Device nou inregistrat: {},{}'.format(add,port))
            #print("Dispozitivele inregistrate si adresele lor: ",self.clients_address)
            #print("Adresa completa device inregistrat: ",add,port)
            self.notify_server = 1

            #se trimite un DNSAnswer catre toate dispozitivele pentru a memora adresa noului device
            self.send_DNS_answer(add,name)

            respond_socket=self.create_socket() #??? nu stiu la ce il voi folosi inca
            # trebuie setata adresa interfetei pentru grupul de multicast
            nume=list(self.clients_address.keys())
            ip=list(self.clients_address.values())

            #print(nume[-1])
            addDevices([nume[-1],ip[-1]])

            try:
                respond_socket.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_IF, socket.inet_aton(add))
            except Exception as err:
                logging.error('Server register_device Error: {}'.format(err))

                #print(err)
            self.responds_sockets.append(respond_socket)

        except Exception as err:
            logging.error('Server register_device Error: {}'.format(err))

            #print(err)

        if self.notify_server==1:

            msg=f"S-a inregistrat device-ul cu numele: {name}"
            self.send_all(msg)
            self.notify_server=0

    def receive_server(self):
        #print(server_receive)
        msgFromServer = "Server started"
        bytesToSend = str.encode(msgFromServer)
        bufferSize=1024

        while True:
            logging.info('Server waiting for devices')

            #print("Server waiting for receive....")
            try:
                message, address = self.server_receive.recvfrom(bufferSize)
                logging.info('Server receives: {} from {}'.format(message,address))
                #print(f"Server receives: {message}....de la {address}")
            except Exception as err:
                logging.error('Server receiver_server error : {}'.format(err))
                #print(err)

            # Sending a reply to client
            #self.server_send.sendto(bytesToSend, address)

    def send_all(self,msg):
        time.sleep(1)
        #print(msg)
        #o functie care va trimite un mesaj tuturor dispozitivelor conectate
        #print("\nServer sends a broadcast message")
        #msgFromServer = str.encode("Here is the server. This message is for all connected devices!")
        try:
            pass
            #msgFromClient = DNS_Question.DNS_Question(DNS_Question.DNS_Question.TYPE_A, DNS_Question.DNS_Question.QCLASS_INTERNET, "myPersonalPc.local").get_dns_question()
            #msgFromClient=DNS_Answer.DNS_Answer(DNS_Answer.DNS_Answer.TYPE_A, DNS_Answer.DNS_Answer.CLASS_INTERNET, 'MyPersonalPC.local').get_dns_answer('192.168.0.9')
        except Exception as err:
            logging.error('Server send_all  Error: {}'.format(err))

            #print(err)
        #print(msgFromClient)
        #bytesToSend = str.encode(msgFromServer)
        #self.server_send.sendto(bytesToSend,mlt_group)
        #self.server_send.sendto(msgFromClient, multicast_group)

    def query_name(self,name="user"):
        #print(name)
        msgFromServer = DNS_Question.DNS_Question(DNS_Question.DNS_Question.TYPE_A,
                                                  DNS_Question.DNS_Question.QCLASS_INTERNET,
                                                  name).get_dns_question()
        self.server_send.sendto(msgFromServer,multicast_group)
        self.interogate_name=1

    def send_DNS_answer(self,address,name="user"):
        time.sleep(1)
        try:
            msgFromClient=DNS_Answer.DNS_Answer(DNS_Answer.DNS_Answer.TYPE_A, DNS_Answer.DNS_Answer.CLASS_INTERNET, name).get_dns_answer(address)
        except Exception as err:
            logging.error('Server send_dns_answer Error: {}'.format(err))

            #print(err)
        self.server_send.sendto(msgFromClient, multicast_group)

    def send_SRV_answer(self,dates):
        time.sleep(1)
        try:
            msgFromClient = SRV_packet.SRV_packet(dates).get_dns_srv_answer()
        except Exception as err:
            print(err)
        self.server_send.sendto(msgFromClient, multicast_group)


    def set_local_network(self,network):
        self.local_network=network



