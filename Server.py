import socket
import threading

import Local_network
from Device import Device

class UDP:
    def __init__(self):
        self.mDNS_port = 5253
        self.mDNS_address = '224.0.0.251'
        self.clients=[]
        self.running=False
        self.local_network=None

        try:
            # Creare socket UDP
            self.server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            # Asociere la adresa locala, portul 5000
            self.server.bind(('127.0.0.1', 20001))
            print("UDP server up and listening")
        except BaseException as error:
            print("Error " + str(error))
            raise

        #vom avea nevoie de un thread pentru asteptarea noilor conexiuni
        #self.ThreadForNewConnections = threading.Thread(target=self.start, args=())
        #self.ThreadForNewConnections.start()

        self.running=True

    def start(self):
        print(f'Asteapta conexiuni (oprire server cu Ctrl‐C) pe adresa ({self.mDNS_address},{self.mDNS_port})')

    def registerDevice(self):
        try:
            # adaugam un nou dispozitiv
            newDevice = Device("nume device")
            newDevice.thread = threading.Thread(target=self.handleDevice)  # functia va receptiona mesajele de la Device
            self.clients.append(newDevice)
            self.local_network.register_device(newDevice)

            # apasarea tastelor Ctrl‐C se iese din blucla while 1
        except KeyboardInterrupt:
            print("Bye bye")

    def handleDevice(conn, addr):
        #trebuie editata dupa nevoile noastre+pachete de date
        while 1:
            # Asteapta date, buffer de 1024 octeti (apel blocant)
            data = conn.recv(1024)
            # Daca functia recv returneaza None, clientul a inchis conexiunea
            if not data:
                break
            print(addr, ' a trimis: ', data)
            # Trimite inapoi datele receptionate
            conn.sendall(bytes(str(addr) + ' a trimis ' + str(data), encoding="ascii"))
        print("Clientul ", addr, " a inchis conexiunea")
        conn.close()

    def set_local_network(self,network):
        self.local_network=network