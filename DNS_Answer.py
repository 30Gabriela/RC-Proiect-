import socket
import struct
import logging
logging.basicConfig(filename='LOGS.log', encoding='utf-8',format='%(asctime)s----%(message)s', datefmt='%d/%m/%Y %I:%M:%S %p', level=logging.DEBUG)

import time

import Header_DNS_packet


class DNS_Answer(Header_DNS_packet.DNS_Header):
    PACKET_TYPE_REQUEST  = 0
    PACKET_TYPE_RESPONSE = 1

    TTL = 255

    TYPE_A      = b'\x00\x01'  # 1              #a host address
    TYPE_NS     = b'\x00\x02'  # 2              #an authoritative name server
    TYPE_CNAME  = b'\x00\x05'  # 5              #the canonical name for an alias
    TYPE_WKSD   = b'\x00\x0b'  # 11             #a well known service description
    TYPE_HINFO  = b'\x00\x0d'  # 13             #host information

    CLASS_INTERNET = b'\x00\x01'
    CLASS_RESERVED = b'\x00\x00'
    CLASS_ANY      = b'\x00\xFF'

    def __init__(self, TYPE_ANSWER,CLASS,host_name):
        #NAME - The domain name that was queried, in the same format as the QNAME in the questions.
        #TYPE - Two octets containing one of the type codes. This field specifies the meaning of the data in the RDATA field. You should be prepared to interpret:
            #type 0x0001 (A record)
            #type 0x0002 (name servers)
        #CLASS - Two octets which specify the class of the data in the RDATA field. ( 0x0001 - Internet addresses)
        #TTL - The number of seconds the results can be cached. (a 32 bit signed integer) - 4 octeti
        #RDLENGTH - The length of the RDATA field (unsigned 16 bit integer) - 2 octeti
        #RDATA - The data of the response. The format is dependent on the TYPE field:
            #if the TYPE is 0x0001 for A record, then this is the IP address (4 octets).
            #If the type is 0x0002 for name servers, then this is the name of the server
            #If the type is 0x0005 for CNAMEs, then this is the name of the alias.

        #pachetul este de tip raspuns
        opcode = self.PACKET_TYPE_RESPONSE
        answer = 1
        super(DNS_Answer, self).__init__(opcode, answer)

        self.NAME=host_name
        self.TYPE=TYPE_ANSWER
        self.CLASS=CLASS
        self.TTL=b'\x00\x00\x00\xff'
        self.RDLENGTH=0
        self.RDATA=''

        name_elements = self.NAME.split('.')
        self.NAME_hex = []
        for elem in name_elements:
            # se adauga pentru fiecare eticheta un octet cu lungimea ei, iar apoi continutul etichetei
            length = len(elem)
            #print("lungime nume: ",length)
            length_hex = hex(length)[2:]
            if len(length_hex) < 2:
                self.NAME_hex.append('0' + length_hex)
            elif len(length_hex) == 2:
                self.NAME_hex.append(length_hex)
            self.NAME_hex.append(elem.encode('utf-8').hex())
        # numerele se termina cu un octet null
        self.NAME_hex.append('00')
        self.NAME_hex = bytes.fromhex(''.join(self.NAME_hex))

    def dns_answer_pack(self, address):
        self.header_dns_packet = self.get_header()
        self.RDATA=[]
        self.RDATA_bytes=[]
        ip=address.split('.')
        for i in ip:
            ip_hex=hex(int(i))[2:]
            ip_append=''
            if len(ip_hex)<2:
                ip_append='0'+str(ip_hex)
            else:
                ip_append=ip_hex
            self.RDATA_bytes.append(bytes.fromhex(ip_append))

        ip1 = self.RDATA_bytes[0]
        ip2 = self.RDATA_bytes[1]
        ip3 = self.RDATA_bytes[2]
        ip4 = self.RDATA_bytes[3]

        self.RDLENGTH=len(ip)
        self.RDLENGTH_hex = hex(self.RDLENGTH)[2:]
        self.RDLENGTH_hex_list=[]
        for i in range(0,4-len(self.RDLENGTH_hex)):
            self.RDLENGTH_hex_list.append('0')
        self.RDLENGTH_hex_list.append(self.RDLENGTH_hex)
        self.RDLENGTH_hex=bytes.fromhex(''.join(self.RDLENGTH_hex_list))

        self.packet=b''.join([self.header_dns_packet,self.NAME_hex, self.TYPE, self.CLASS, self.TTL,self.RDLENGTH_hex,ip1,ip2,ip3,ip4]) #mai trebuie adaugat rdlength si rdata
        #print(self.packet)
        return self.packet

    def get_dns_answer(self,address):
        packet=self.dns_answer_pack(address)
        return packet


def dns_answer_unpack(message):
        time.sleep(1)
        #print(message)
        bytes=[byte for byte in message]
        #print(bytes)
        lungime=bytes[12]
        index_start=12+1
        etichete=[]
        while lungime!=0:
            eticheta=''.join(map(chr,message[index_start:index_start+lungime]))
            #eticheta=struct.unpack(f'{lungime}s',message[13:13+lungime])
            index_start = index_start + lungime + 1
            lungime=bytes[index_start-1]
            etichete.append(eticheta)
        HostName=[]
        HostName.append(etichete[0])
        for i in range(1,len(etichete)):
            HostName.append('.')
            HostName.append(etichete[i])
        HostName=''.join(HostName)

        logging.info('Hostname extras din DNS_Answer: {}'.format(HostName))

        #print("\nHostname extras din DNS_Answer: ", HostName)
        address=''
        for i in range(0,4):
            address+=str(bytes[-4+i])
            address+='.'
        address=address[:-1]

        logging.info('Ip extras din DNS_Answer: {}'.format(address))

        #print("Adresa ip extrasa din DNS_Answer: ", address)

        question = bytes[5]
        answer = bytes[7]
        id=''.join((str(i) for i in bytes[0:2]))
        return id, question, answer, HostName,address

#a=DNS_Answer(DNS_Answer.TYPE_A,DNS_Answer.CLASS_INTERNET,"slkta.local")
#print(a.get_dns_answer('192.169.0.3'))
#a.get_dns_answer('192.168.75.1')