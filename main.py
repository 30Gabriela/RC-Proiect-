import Local_network
import Server
import Responder

if __name__=='__main__':
    Responder.startInterface()
    MainServer = Server.UDP()
    # se creeaza reteaua locala
    local_network = Local_network.Local(MainServer)
    # setam in server reteaua locala
    MainServer.set_local_network(local_network)
    MainServer.start()