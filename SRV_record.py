class SRV_record:
    def __init__(self,name_service, protocol, domain_name, ttl, priority, weigth, port, target):
        self.name_service=name_service
        self.protocol=protocol  #mereu e TCP/IP
        self.domain_name=domain_name #numele de domeniu unde aceasta intrare este valida
        self.ttl=ttl   #time to alive
        self.priority=priority  #prioritatea gazdei tinta
        self.weight=weigth  #o valoare relativa pentru intrarile cu aceeasi greutate
        self.port=port      #portul TCP unde va fi gasit serviciul
        self.target=target #numele de gazda al dispozitivului ce pune la dispozitie acel serviciu

    def print(self):
        print(self.name_service)
        print(self.priority)
        print(self.domain_name)
        print(self.ttl)
        print(self.weight)
        print(self.port)
        print(self.target)


