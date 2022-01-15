SRVs=[]
class SRV_record:
    def __init__(self,name_service, protocol, domain_name, ttl, priority, weigth, port, target):
        self.name_service=name_service
        self.protocol=protocol  #mereu e UDP
        self.domain_name=domain_name #numele de domeniu unde aceasta intrare este valida
        self.ttl=ttl   #time to alive
        self.priority=priority  #prioritatea gazdei tinta
        self.weight=weigth  #o valoare relativa pentru intrarile cu aceeasi greutate
        self.port=port      #portul TCP unde va fi gasit serviciul
        self.target=target #numele de gazda al dispozitivului ce pune la dispozitie acel serviciu
        SRVs.append(self)

    def print(self):
        return str(self.name_service+" "+self.priority+" "+self.domain_name+" "+self.ttl+" "+self.weight+" "+self.port+" "+self.target)

    def get_dates(self):
        list=[]
        list.append(self.name_service)
        list.append(self.priority)
        list.append(self.domain_name)
        list.append(self.ttl)
        list.append(self.weight)
        list.append(self.port)
        list.append(self.target)
        return list



