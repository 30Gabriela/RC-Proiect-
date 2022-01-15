from random import randrange
import logging
logging.basicConfig(filename='LOGS.log',format='%(asctime)s----%(message)s', datefmt='%d/%m/%Y %I:%M:%S %p', level=logging.DEBUG)
class Local:
    def __init__(self,server):
        self.devices=[] #o lista cu dispozitivele din retea
        self.IP_used=[]
        self.initial_port_for_client=20000
        self.server=server
    #zero-config

    def register_device(self,new_device):
        #setare adresa IP
        #de pus valori pt adrese din reteaua locala utilizata
        limita_superioara=256
        limita_inferioara=0
        Ip1 = 192
        Ip2 = 168
        Ip3=75
        Ip4=1
        new_Ip=''
        if len(self.IP_used) == 0:
            Ip4=1
            new_Ip=str(Ip1)+'.'+str(Ip2)+'.'+str(Ip3)+'.'+str(Ip4)
        else:
            last_address=self.IP_used.pop(len(self.IP_used)-1)
            self.IP_used.append(last_address)
            ip1,ip2,ip3,ip4=last_address.split('.')
            ip4=int(ip4)+1
            if ip4==limita_superioara:
                ip4=limita_inferioara+1 #am voie sa ocup adresa de retea? sau care va fi masca retelei?
                ip3=int(ip3)+1
            new_Ip=str(ip1)+'.'+str(ip2)+'.'+str(ip3)+'.'+str(ip4)

        check_Ip=self.verify_IP(new_Ip)
        if check_Ip==1:
            new_device.set_router_address(new_Ip)
            logging.info('S-a setat adresa ip: {}'.format(new_Ip))
            #print(f"S-a setat adresa IP: {new_Ip}")
            self.IP_used.append(new_Ip)

        self.initial_port_for_client+=1
        new_device.set_port(self.initial_port_for_client)

        self.devices.append(new_device)

    def verify_IP(self,IP):
        for i in self.IP_used:
            if i ==IP:
                return 0
        return 1