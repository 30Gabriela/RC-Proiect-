import socket
import threading
from Device import Device

class Server:
    def __init__(self):
        self.mDNS_port = 5253
        self.mDNS_address = '224.0.0.251'
        self.clients=[]
        self.running=False
        self.local_network=None
        try:
            # Creaza un socket IPv4, TCP
            self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            # Asociere la adresa locala, portul 5000
            self.server.bind(('127.0.0.1', 5000))
            # Coada de asteptare pentru conexiuni de lungime 10
            self.server.listen(10)

            #vom avea nevoie de un thread pentru asteptarea noilor conexiuni
            self.ThreadForNewConnections = threading.Thread(target=self.start, args=())
            self.ThreadForNewConnections.start()
        except BaseException as error:
            print("Error "+error)
            raise
        self.running=True

    #pornirea socket-ului = asteptarea conexiunilor
    def start(self):
        # server-ul va astepta noi conexiuni de la clienti
        try:
            self.server.listen()
        except BaseException as error:
            print("Error "+error)
        print(f'Asteapta conexiuni (oprire server cu Ctrl‐C) pe adresa ({self.mDNS_address},{self.mDNS_port})')
        while self.running:
            #aici se face legatura cu clientii server-ului
            try:
                # Asteapta cereri de conectare, apel blocant
                # La conectarea unui client, functia returneaza un nou socket si o tupla (ip_address,port)
                connection, addr = self.server.accept()

                #adaugam un nou dispozitiv
                newDevice=Device("nume device")
                newDevice.thread = threading.Thread(target=self.handleDevice) #functia va receptiona mesajele de la Device
                self.clients.append(newDevice)
                self.local_network.register_device(newDevice)

            #apasarea tastelor Ctrl‐C se iese din blucla while 1
            except KeyboardInterrupt:
                print("Bye bye")

            print('S‐a conectat clientul', addr)
            try:
                newDevice.thread.start()
            except:
                print("Eroare la pornirea thread‐ului")


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