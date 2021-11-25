from random import randrange
from Device import Device
class Local:
    def __init__(self):
        self.devices=[] #o lista cu dispozitivele din retea
        self.IP_used=[]
    #zero-config
    def register_device(self,new_device):
        Ip_address_1=192
        Ip_address_2=168
        Ip_address_3=0
        Ip_address_4=randrange(1,253,1)
        check_Ip=self.verify_IP(Ip_address_4)
        if check_Ip==1:
            new_device.set_router_address(str(Ip_address_1)+'.'+str(Ip_address_2)+'.'+str(Ip_address_3)+'.'+str(Ip_address_4g))
        self.devices.append(new_device)

    def verify_IP(self,IP_address_4):
        for i in self.IP_used:
            if i ==IP_address_4:
                return 0
        return 1