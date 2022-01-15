import binascii
import struct

import Header_DNS_packet
import logging
logging.basicConfig(filename='LOGS.log', encoding='utf-8',format='%(asctime)s----%(message)s', datefmt='%d/%m/%Y %I:%M:%S %p', level=logging.DEBUG)

class DNS_Question(Header_DNS_packet.DNS_Header):
    PACKET_TYPE_REQUEST  = 0
    PACKET_TYPE_RESPONSE = 1

    QCLASS_INTERNET = b'\x00\x01'
    QCLASS_RESERVED = b'\x00\x00'
    QCLASS_ANY      = b'\x00\xFF'

    TYPE_A     =  b'\x00\x01'    #1              #a host address
    TYPE_WKSD  =  b'\x00\x0b'    #11             #a well known service description
    TYPE_DNPTR =  b'\x00\x0c'    #12             #a domain name pointer
    TYPE_HINFO =  b'\x00\x0d'    #13             #host information
    TYPE_SRV   =  b'\x00\x21'    #33             #server selection
    TYPE_ANY   =  b'\x00\xff'    #255            #a request for some or all records the server has available

    END_OF_THE_NAME = b'\x00'

    def __init__(self,TYPE_QUESTION,CLASS,host_name):
        #QNAME - the domain for which the query is sent - 2 bytes
        #QTYPE - in cazul nostru va fi host address - 2 bytes
        #QCLASS - 2 bytes

        self.QNAME = host_name  #".local"
        self.QTYPE = TYPE_QUESTION
        self.QCLASS = CLASS
        #self.QU_question=

        #pachetul va fi de tip cerere, nu raspuns
        opcode=self.PACKET_TYPE_REQUEST
        answer=0
        super(DNS_Question,self).__init__(opcode,answer)

        name_elements=self.QNAME.split('.')
        self.QNAME_hex=[]
        for elem in name_elements:
            #se adauga pentru fiecare eticheta un octet cu lungimea ei, iar apoi continutul etichetei
            length=len(elem)
            length_hex=hex(length)[2:]
            if len(length_hex)<2:
                self.QNAME_hex.append('0'+length_hex)
            elif len(length_hex)==2:
                self.QNAME_hex.append(length_hex)
            self.QNAME_hex.append(elem.encode('utf-8').hex())
        #numerele se termina cu un octet null
        self.QNAME_hex.append('00')
        self.QNAME_hex=bytes.fromhex(''.join(self.QNAME_hex))

    def dns_question_pack(self):
        self.header_dns_packet = self.get_header()
        #print(self.header)
        self.packet=b''.join([self.header_dns_packet,self.QNAME_hex, self.QTYPE, self.QCLASS])
        #print(self.packet)
        return self.packet

    def get_dns_question(self):
        packet = self.dns_question_pack()
        #self.dns_question_unpack(packet)
        return packet

def dns_question_unpack(message):
        #print(message)
        bytes = [byte for byte in message]
        #print(bytes)
        lungime = bytes[12]
        index_start = 12 + 1
        etichete = []
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
        logging.info('Hostname extras din DNS_Question: {}'.format(HostName))
        #print("\nHostname extras din DNS_Question: ", HostName)

        question=bytes[5]
        answer=bytes[6]
        id=''.join((str(i) for i in bytes[0:2]))

        return id,question, answer,HostName


#a=DNS_Question(DNS_Question.TYPE_A,DNS_Question.QCLASS_INTERNET,'MYPC.local')
#print(a.get_dns_question())
