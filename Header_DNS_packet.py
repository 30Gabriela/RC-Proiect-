class DNS_Header(object):
    OPC_REQUEST = 0
    OPC_RESPONSE = 1

    def __init__(self,opcode,answer):
        assert opcode == self.OPC_REQUEST or opcode == self.OPC_RESPONSE, "Invalid opcode"
        self.transaction_id=b'\xdb\x42'
        #b'\x00\x00' # 2 bytes
        self.QR=opcode
        self.OPCODE='0000' #standard query
        if opcode==self.OPC_REQUEST:
            self.AA='0'
        elif opcode==self.OPC_RESPONSE:
            self.AA='1'
        self.TC='0'
        self.RD='0'
        self.RA='0'
        self.Z='000'
        self.RCODE='0000'

        #QCOUNT  - 2 bytes - questions
        #ANCOUNT - 2 bytes - answer RRs
        #NSCOUNT - 2 bytes - authority RRs
        #ARCOUNT - 2 bytes - additional RRs

        if opcode==self.OPC_REQUEST:
            self.QDCOUNT=b'\x00\x01' #it is a question
        else:
            self.QDCOUNT=b'\x00\x00'
        if answer==1:
            self.ANCOUNT=b'\x00\x01' #it is an answer
        elif answer==0:
            self.ANCOUNT=b'\x00\x00'
        self.NSCOUNT=b'\x00\x00'
        self.ARCOUNT=b'\x00\x00'

    def get_header(self):
        self.header_pack()
        return self.header

    def header_pack(self):
        #prima parte a header-ului - parameters/flags -2 octeti
        flags = '0b' + str(self.QR) + self.OPCODE + self.AA + self.TC + self.RD + self.RA + self.Z + self.RCODE
        self.hex_flags = hex(int(flags, 2))

        #print(self.hex_flags)
        if len(self.hex_flags[2:]) < 4:
            buffer = []
            buffer.append('0x')
            for i in range(0, (4 - len(self.hex_flags[2:]))):
                buffer.append('0')
            buffer.append(self.hex_flags[2:])
            self.hex_flags = ''.join(buffer)
        self.hex_flags = bytes.fromhex(str(self.hex_flags[2:])) # 2 bytes
        #print(self.hex_flags)

        self.header = b''.join([self.transaction_id,self.hex_flags, self.QDCOUNT,self.ANCOUNT,self.NSCOUNT,self.ARCOUNT])








