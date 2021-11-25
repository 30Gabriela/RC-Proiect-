from random import randrange
from Device import Device
class Local:
    def __init__(self):
        self.devices=[] #o lista cu dispozitivele din retea
        self.IP_used=[]

    #zero-config

    def register_device(self,new_device):
        #setare adresa IP
        limita_superioara=256
        limita_inferioara=0
        Ip1 = 192
        Ip2 = 168
        Ip3=0
        Ip4=0
        new_Ip=''
        if len(self.IP_used) == 0:
            Ip4=1
            new_Ip=str(Ip1)+'.'+str(Ip2)+'.'+str(Ip3)+'.'+str(Ip4)
        else:
            last_address=self.IP_used.pop(len(self.IP_used)-1)
            self.IP_used.append(last_address)
            ip1,ip2,ip3,ip4=last_address.split('.')
            ip4+=1
            if ip4==limita_superioara:
                ip4=limita_inferioara+1 #am voie sa ocup adresa de retea? sau care va fi masca retelei?
                ip3=ip3+1
            new_Ip=str(ip1)+'.'+str(ip2)+'.'+str(ip3)+'.'+str(ip4)
        #Ip_address_4=randrange(1,253,1) ?????
        check_Ip=self.verify_IP(new_Ip)
        if check_Ip==1:
            new_device.set_router_address(new_Ip)
            self.IP_used.append(new_Ip)
        self.devices.append(new_device)

    def verify_IP(self,IP):
        for i in self.IP_used:
            if i ==IP:
                return 0
        return 1