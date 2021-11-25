#zero config se bazeaza pe TCP/IP
import TCP
import Local_network

if __name__=='__main__':
    MainServer=TCP.Server()
    MainServer.start()
    local_network=Local_network.Local(MainServer)
    MainServer.set_local_network(local_network)