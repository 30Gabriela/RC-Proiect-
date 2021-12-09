import socket
import threading
import time

import Local_network
from Device import Device

class UDP:
    def __init__(self):
        self.mDNS_port = 5353
        self.mDNS_address = '224.0.0.251'
        self.local_address='127.0.0.1'
        self.local_port=20001
        self.clients=[]
        self.clients_address=[]
        self.running=False
        self.local_network=None

        try:
            # Creare socket UDP
            self.server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            self.server.bind((self.local_address,self.local_port))
            print("UDP server up and listening")
        except BaseException as error:
            print("Error " + str(error))
            raise

    def start(self):
        #print(f'Asteapta conexiuni (oprire server cu Ctrl‐C) pe adresa ({self.mDNS_address},{self.mDNS_port})')
        try:
            receive_thread = threading.Thread(target=self.receive_server)
            receive_thread.start()
            print("Se porneste thread ul pentru receive")
        except:
            print("Eroare la pornirea thread‐ului")

    def registerDevice(self,name):
        try:
            print(f"\nSe va inregistra un nou device cu numele {name}")
            # adaugam un nou dispozitiv
            newDevice = Device(str(name))
            #newDevice.thread = threading.Thread(target=self.handleDevice)  # functia va receptiona mesajele de la Device
            self.clients.append(newDevice)
            print(f"Lista cu dispozitivele conectate: {self.clients}")
            self.local_network.register_device(newDevice)

            # apasarea tastelor Ctrl‐C se iese din blucla while 1
        except KeyboardInterrupt:
            print("Bye bye")
        self.send_all()

    def receive_server(self):
        msgFromServer = "Hello UDP Client"
        bytesToSend = str.encode(msgFromServer)
        bufferSize=1024
        while True:
            bytesAddressPair = self.server.recvfrom(bufferSize)
            message = bytesAddressPair[0]
            address = bytesAddressPair[1]

            self.clients_address.append(address)
            print(address)
            clientMsg = "Message from Client:{}".format(message)
            clientIP = "Client IP Address:{}".format(address)
            print(clientMsg)
            print(clientIP)

            # Sending a reply to client
            self.server.sendto(bytesToSend, address)

    def send_all(self):
        time.sleep(1)
        #o functie care va trimite un mesaj tuturor dispozitivelor conectate
        print("\n\nServer sends a broadcast message\n")
        msgFromServer = "Hello! Here is the server. This message is for all connected devices!"
        bytesToSend = str.encode(msgFromServer)
        bufferSize = 1024
        for i in self.clients_address:
            self.server.sendto(bytesToSend, i)


    def set_local_network(self,network):
        self.local_network=network