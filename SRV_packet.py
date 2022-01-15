import time

import Header_DNS_packet


class SRV_packet(Header_DNS_packet.DNS_Header):
    PACKET_TYPE_REQUEST  = 0
    PACKET_TYPE_RESPONSE = 1

    TTL = 255

    TYPE_SRV    = b'\x00\x21'  # 33             #server selection

    CLASS_INTERNET = b'\x00\x01'
    CLASS_ANY      = b'\x00\xFF'

    def __init__(self, dates):
        #dates:
        #dates[0]=name_service
        #dates[1]=priority
        #dates[2]=domain_name
        #dates[3]=ttl
        #dates[4]=weight
        #dates[5]=port
        #dates[6]=target

        opcode = self.PACKET_TYPE_RESPONSE
        answer = 1
        super(SRV_packet, self).__init__(opcode, answer)

        self.NAME = '_'+dates[0]+'._UDP.'+dates[2] #doar .local
        self.TYPE = SRV_packet.TYPE_SRV
        self.CLASS = SRV_packet.CLASS_INTERNET
        self.TTL = b'\x00\x00\x00\xff'
        self.RDLENGTH = 0
        self.RDATA = ''
        self.srv_TTL=hex(int(dates[3]))[2:]
        self.priority=hex(int(dates[1]))[2:]
        self.weight=hex(int(dates[4]))[2:]
        self.port=hex(int(dates[5]))[2:]
        self.target=dates[6]

        target_elements = self.target.split('.')
        self.target_hex = []
        for elem in target_elements:
            # se adauga pentru fiecare eticheta un octet cu lungimea ei, iar apoi continutul etichetei
            length = len(elem)
            # print("lungime nume: ",length)
            length_hex = hex(length)[2:]
            if len(length_hex) < 2:
                self.target_hex.append('0' + length_hex)
            elif len(length_hex) == 2:
                self.target_hex.append(length_hex)
            self.target_hex.append(elem.encode('utf-8').hex())
        # numerele se termina cu un octet null
        self.target_hex.append('00')
        self.target_hex = bytes.fromhex(''.join(self.target_hex))

        #print(self.target_hex)

        name_elements = self.NAME.split('.')
        self.NAME_hex = []
        for elem in name_elements:
            # se adauga pentru fiecare eticheta un octet cu lungimea ei, iar apoi continutul etichetei
            length = len(elem)
            # print("lungime nume: ",length)
            length_hex = hex(length)[2:]
            if len(length_hex) < 2:
                self.NAME_hex.append('0' + length_hex)
            elif len(length_hex) == 2:
                self.NAME_hex.append(length_hex)
            self.NAME_hex.append(elem.encode('utf-8').hex())
        # numerele se termina cu un octet null
        self.NAME_hex.append('00')
        self.NAME_hex = bytes.fromhex(''.join(self.NAME_hex))

    def dns_answer_srv_pack(self, address):
            self.header_dns_packet = self.get_header()
            #self.RDATA = []
            self.RDATA_bytes = []

            if len(self.srv_TTL) < 8:
                aux = self.srv_TTL
                self.srv_TTL = ''
                for i in range(1,8-len(self.srv_TTL)):
                    self.srv_TTL+='0'
                self.srv_TTL+=str(aux)
            self.srv_TTL=bytes.fromhex(self.srv_TTL)

            if len(self.priority)<4:
                aux=self.priority
                self.priority=''
                for i in range(1,4-len(self.priority)):
                    self.priority+='0'
                self.priority+=str(aux)
            self.RDATA_bytes.append(bytes.fromhex(self.priority))

            if len(self.weight)<4:
                aux=self.weight
                self.weight=''
                for i in range(1,4-len(self.weight)):
                    self.weight+='0'
                self.weight+=str(aux)

            self.RDATA_bytes.append(bytes.fromhex(self.weight))

            #print(self.port)
            if len(self.port)<4:
                aux=self.port
                self.port=''
                for i in range(1,4-len(self.port)):
                    self.port+='0'
                self.port+=str(aux)

            self.RDATA_bytes.append(bytes.fromhex(self.port))

            self.RDATA=b''.join(self.RDATA_bytes)

            self.RDLENGTH = len(self.RDATA)+len(self.target_hex)
            self.RDLENGTH_hex = hex(self.RDLENGTH)[2:]
            self.RDLENGTH_hex_list = []
            for i in range(0, 4 - len(self.RDLENGTH_hex)):
                self.RDLENGTH_hex_list.append('0')
            self.RDLENGTH_hex_list.append(self.RDLENGTH_hex)
            self.RDLENGTH_hex = bytes.fromhex(''.join(self.RDLENGTH_hex_list))

            self.packet = b''.join(
                [self.header_dns_packet, self.NAME_hex, self.TYPE, self.CLASS, self.srv_TTL, self.RDLENGTH_hex,self.RDATA,self.target_hex])

            return self.packet

    def get_dns_srv_answer(self,address):
        packet=self.dns_answer_srv_pack(address)
        return packet

    def dns_answer_srv_unpack(message):
        #print(message)
        bytes = [byte for byte in message]
        #print(bytes)
        lungime = bytes[12]
        index_start = 12 + 1
        etichete = []
        while lungime != 0:
            eticheta = ''.join(map(chr, message[index_start:index_start + lungime]))
            # eticheta=struct.unpack(f'{lungime}s',message[13:13+lungime])
            index_start = index_start + lungime + 1
            lungime = bytes[index_start - 1]
            etichete.append(eticheta)
        Name_service = []
        Name_service.append(etichete[0])
        for i in range(1, len(etichete)):
            Name_service.append('.')
            Name_service.append(etichete[i])
        Name_service = ''.join(Name_service)
        #print("\nName_service extras din DNS_Answer_SRV: ", Name_service)

        index_start+=1
        type_srv=bytes[index_start]
        index_start=index_start+15
        #print("tip srv: ",type_srv)
        #print(bytes[index_start:])
        lungime=bytes[index_start]
        index_start+=1
        etichete = []
        while lungime != 0:
            eticheta = ''.join(map(chr, message[index_start:index_start + lungime]))
            # eticheta=struct.unpack(f'{lungime}s',message[13:13+lungime])
            index_start = index_start + lungime + 1
            lungime = bytes[index_start - 1]
            etichete.append(eticheta)
        #print(etichete)
        target=[]
        target.append(etichete[0])
        for i in range(1, len(etichete)):
            target.append('.')
            target.append(etichete[i])
        target = ''.join(target)
        #print("\nName_target extras din DNS_Answer_SRV: ", target)

        question = bytes[5]
        answer = bytes[7]

        return question, answer, type_srv,Name_service,target