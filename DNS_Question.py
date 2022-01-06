import binascii
import struct

import Header_DNS_packet


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
            length=len(elem)
            length_hex=hex(length)[2:]
            if len(length_hex)<2:
                #self.QNAME_hex.append('0')
                self.QNAME_hex.append('0'+length_hex)
            #print(elem.encode('utf-8').hex())
            self.QNAME_hex.append(elem.encode('utf-8').hex())
        self.QNAME_hex.append('00')
        self.QNAME_hex=bytes.fromhex(''.join(self.QNAME_hex))

    def dns_question_pack(self):
        self.header_dns_packet = self.get_header()
        #print(self.header)
        self.packet=b''.join([self.header_dns_packet,self.QNAME_hex, self.QTYPE, self.QCLASS])
        #print(self.packet)
        return self.packet

    def get_dns_question(self):
        return self.dns_question_pack()

#a=DNS_Question(DNS_Question.TYPE_A,DNS_Question.QCLASS_INTERNET,'MYPC.local')
#print(a.get_dns_question())
