from SRV_record import SRV_record
from PyQt5 import QtCore, QtGui, QtWidgets
from Resolver import Ui_MainWindow
from Server import UDP
import sys
from Resolver import checkDevicesDuplicate,addDevices,renameDevice
srvList=[]
class Ui_ShowSRV(object):
    def setupUi(self, Form1):
        Form1.setObjectName("Form")
        Form1.resize(260,238)
        self.frame = QtWidgets.QFrame(Form1)
        self.frame.setGeometry(QtCore.QRect(-161, -21, 1241, 921))
        self.frame.setStyleSheet("background-color: rgb(216, 238, 240);")
        self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setObjectName("frame")
        self.WriteSRVEntries = QtWidgets.QTextEdit(self.frame)
        self.WriteSRVEntries.setGeometry(QtCore.QRect(160, 20, 1011, 881))
        self.WriteSRVEntries.setReadOnly(True)
        self.WriteSRVEntries.setObjectName("WriteSRVEntries")

        self.retranslateUi(Form1)
        QtCore.QMetaObject.connectSlotsByName(Form1)

    def retranslateUi(self, Form1):
        _translate = QtCore.QCoreApplication.translate
        Form1.setWindowTitle(_translate("Form", "SRV Entries"))


class Ui_SRV(object):
    listaSRV=[]
    listaClienti=[]

    def setupUi(self, Form,main):
        self.mainWindows=main
        Form.setObjectName("Form")
        Form.resize(1180, 159)
        Form.setMinimumSize(QtCore.QSize(1180, 159))
        Form.setMaximumSize(QtCore.QSize(1180, 159))
        Form.setStyleSheet("background-color: rgb(216, 238, 240);")
        self.MainFrame = QtWidgets.QFrame(Form)
        self.MainFrame.setGeometry(QtCore.QRect(20, 20, 1141, 121))
        self.MainFrame.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.MainFrame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.MainFrame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.MainFrame.setObjectName("MainFrame")
        self.Address_label = QtWidgets.QLabel(self.MainFrame)
        self.Address_label.setGeometry(QtCore.QRect(70, 20, 61, 16))
        self.Address_label.setObjectName("Address_label")
        self.TTL_label = QtWidgets.QLabel(self.MainFrame)
        self.TTL_label.setGeometry(QtCore.QRect(260, 20, 61, 16))
        self.TTL_label.setObjectName("TTL_label")
        self.Port_label = QtWidgets.QLabel(self.MainFrame)
        self.Port_label.setGeometry(QtCore.QRect(640, 20, 61, 16))
        self.Port_label.setObjectName("Port_label")
        self.Priority_label = QtWidgets.QLabel(self.MainFrame)
        self.Priority_label.setGeometry(QtCore.QRect(380, 20, 61, 16))
        self.Priority_label.setObjectName("Priority_label")
        self.Weight_label = QtWidgets.QLabel(self.MainFrame)
        self.Weight_label.setGeometry(QtCore.QRect(500, 20, 61, 16))
        self.Weight_label.setObjectName("Weight_label")
        self.WriteAddress = QtWidgets.QLineEdit(self.MainFrame)
        self.WriteAddress.setGeometry(QtCore.QRect(10, 50, 181, 31))
        self.WriteAddress.setObjectName("WriteAddress")
        self.WriteTTL = QtWidgets.QLineEdit(self.MainFrame)
        self.WriteTTL.setGeometry(QtCore.QRect(220, 50, 101, 31))
        self.WriteTTL.setObjectName("WriteTTL")
        self.WritePriority = QtWidgets.QLineEdit(self.MainFrame)
        self.WritePriority.setGeometry(QtCore.QRect(350, 50, 101, 31))
        self.WritePriority.setObjectName("WritePriority")
        self.WriteWeight = QtWidgets.QLineEdit(self.MainFrame)
        self.WriteWeight.setGeometry(QtCore.QRect(480, 50, 101, 31))
        self.WriteWeight.setObjectName("WriteWeight")
        self.WritePort = QtWidgets.QLineEdit(self.MainFrame)
        self.WritePort.setGeometry(QtCore.QRect(610, 50, 101, 31))
        self.WritePort.setObjectName("WritePort")
        self.WriteHost = QtWidgets.QLineEdit(self.MainFrame)
        self.WriteHost.setGeometry(QtCore.QRect(740, 50, 201, 31))
        self.WriteHost.setObjectName("WriteHost")
        self.Host_label = QtWidgets.QLabel(self.MainFrame)
        self.Host_label.setGeometry(QtCore.QRect(820, 20, 61, 16))
        self.Host_label.setObjectName("Host_label")
        self.AddButton_2 = QtWidgets.QPushButton(self.MainFrame)
        self.AddButton_2.setGeometry(QtCore.QRect(980, 42, 111, 41))
        self.AddButton_2.setStyleSheet("background-color: rgb(230, 230, 230);")
        self.AddButton_2.setObjectName("AddButton_2")
        self.AddButton_2.clicked.connect(self.getSRVDates)
        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Setari SRV"))
        self.Address_label.setText(_translate("Form", "<html><head/><body><p><span style=\" font-size:12pt;\">Address</span></p></body></html>"))
        self.TTL_label.setText(_translate("Form", "<html><head/><body><p><span style=\" font-size:12pt;\">TTL</span></p><p><br/></p></body></html>"))
        self.Port_label.setText(_translate("Form", "<html><head/><body><p><span style=\" font-size:12pt;\">Port</span></p><p><br/></p></body></html>"))
        self.Priority_label.setText(_translate("Form", "<html><head/><body><p><span style=\" font-size:12pt;\">Priority</span></p><p><br/></p></body></html>"))
        self.Weight_label.setText(_translate("Form", "<html><head/><body><p><span style=\" font-size:12pt;\">Weight</span></p><p><br/></p></body></html>"))
        self.Host_label.setText(_translate("Form", "<html><head/><body><p><span style=\" font-size:12pt;\">Host</span></p></body></html>"))
        self.AddButton_2.setText(_translate("Form", "Add"))


    def getSRVDates(self):
        global srvList
        address = self.WriteAddress.text()
        ttl = self.WriteTTL.text()
        priority = self.WritePriority.text()
        weight = self.WriteWeight.text();
        port = self.WritePort.text()
        host = self.WriteHost.text()
        host+='.local'
        if(not checkDevicesDuplicate(host)):
            a = SRV_record("defaultName", "UDP", address, ttl, priority, weight, port, host)
            self.mainWindows.closeSrv()
            self.listaSRV.append(a)
            srvList.append(a)

        else:
            error_dialog = QtWidgets.QErrorMessage()
            error_dialog.showMessage('Dispozitivul ales pentru srv nu exista.')
            error_dialog.exec_()

    def getLista(self):
        return self.listaSRV
    def deleteLista(self):
        self.listaSRV.clear()


def getSRVtoResolver():
    return srvList

class Ui_Responder(object):

    UDP_local=None

    def set_UDP(self,udp):
        #global UDP_local
        self.UDP_local=udp

    def setupUi(self, MainWindow):
        self.height = 462
        self.weight = 635
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(self.height,self.weight)
        MainWindow.setMinimumSize(QtCore.QSize(462, 635))
        MainWindow.setMaximumSize(QtCore.QSize(462, 635))
        MainWindow.setStyleSheet("\n"
"background-color: rgb(255, 255, 255);")

        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.MainFrame = QtWidgets.QFrame(self.centralwidget)
        self.MainFrame.setGeometry(QtCore.QRect(-10, -30, 511, 881))
        self.MainFrame.setStyleSheet("background-color: rgb(216, 238, 240);")
        self.MainFrame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.MainFrame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.MainFrame.setObjectName("MainFrame")
        self.ACLOGO = QtWidgets.QLabel(self.MainFrame)
        self.ACLOGO.setGeometry(QtCore.QRect(410, 600, 51, 51))
        self.ACLOGO.setText("")
        self.ACLOGO.setPixmap(QtGui.QPixmap("cropped-logo_ac_iasi.qrc.png"))
        self.ACLOGO.setScaledContents(True)
        self.ACLOGO.setObjectName("ACLOGO")
        self.ACLOGO_2 = QtWidgets.QLabel(self.MainFrame)
        self.ACLOGO_2.setGeometry(QtCore.QRect(20, 600, 51, 51))
        self.ACLOGO_2.setText("")
        self.ACLOGO_2.setPixmap(QtGui.QPixmap("cropped-logo_ac_iasi.qrc.png"))
        self.ACLOGO_2.setScaledContents(True)
        self.ACLOGO_2.setObjectName("ACLOGO_2")
        self.AddServiceFrame = QtWidgets.QFrame(self.MainFrame)
        self.AddServiceFrame.setGeometry(QtCore.QRect(30, 50, 421, 161))
        self.AddServiceFrame.setStyleSheet("background-color: rgb(163, 163, 163);\n"
"background-color: rgb(255, 255, 255);")
        self.AddServiceFrame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.AddServiceFrame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.AddServiceFrame.setObjectName("AddServiceFrame")
        self.Add_device_label = QtWidgets.QLabel(self.AddServiceFrame)
        self.Add_device_label.setGeometry(QtCore.QRect(10, 0, 111, 41))
        self.Add_device_label.setObjectName("Add_device_label")
        self.Domain_name_label = QtWidgets.QLabel(self.AddServiceFrame)
        self.Domain_name_label.setGeometry(QtCore.QRect(10, 60, 111, 16))
        self.Domain_name_label.setObjectName("Domain_name_label")
        self.WriteDomainName = QtWidgets.QLineEdit(self.AddServiceFrame)
        self.WriteDomainName.setGeometry(QtCore.QRect(130, 60, 261, 31))
        self.WriteDomainName.setObjectName("WriteDomainName")
        self.AddButton = QtWidgets.QPushButton(self.AddServiceFrame)
        self.AddButton.setGeometry(QtCore.QRect(160, 120, 91, 23))
        self.AddButton.setStyleSheet("background-color: rgb(230, 230, 230);")
        self.AddButton.setObjectName("AddButton")
        self.AddButton.clicked.connect(self.getDomainName)
        self.Rename_domain_frame = QtWidgets.QFrame(self.MainFrame)
        self.Rename_domain_frame.setGeometry(QtCore.QRect(30, 230, 421, 171))
        self.Rename_domain_frame.setStyleSheet("background-color: rgb(163, 163, 163);\n"
"background-color: rgb(255, 255, 255);")
        self.Rename_domain_frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.Rename_domain_frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.Rename_domain_frame.setObjectName("Rename_domain_frame")
        self.Rename_domain_label = QtWidgets.QLabel(self.Rename_domain_frame)
        self.Rename_domain_label.setGeometry(QtCore.QRect(10, 10, 241, 41))
        self.Rename_domain_label.setObjectName("Rename_domain_label")
        self.Old_name_label = QtWidgets.QLabel(self.Rename_domain_frame)
        self.Old_name_label.setGeometry(QtCore.QRect(20, 50, 111, 16))
        self.Old_name_label.setObjectName("Old_name_label")
        self.New_name_label = QtWidgets.QLabel(self.Rename_domain_frame)
        self.New_name_label.setGeometry(QtCore.QRect(20, 90, 111, 16))
        self.New_name_label.setObjectName("New_name_label")
        self.WriteOldName = QtWidgets.QLineEdit(self.Rename_domain_frame)
        self.WriteOldName.setGeometry(QtCore.QRect(140, 40, 261, 31))
        self.WriteOldName.setObjectName("WriteOldName")
        self.WriteNewName = QtWidgets.QLineEdit(self.Rename_domain_frame)
        self.WriteNewName.setGeometry(QtCore.QRect(140, 90, 261, 31))
        self.WriteNewName.setObjectName("WriteNewName")
        self.RenameButton = QtWidgets.QPushButton(self.Rename_domain_frame)
        self.RenameButton.setGeometry(QtCore.QRect(160, 130, 91, 23))
        self.RenameButton.setStyleSheet("background-color: rgb(230, 230, 230);")
        self.RenameButton.setObjectName("RenameButton")
        self.SRV = QtWidgets.QFrame(self.MainFrame)
        self.SRV.setGeometry(QtCore.QRect(30, 430, 421, 161))
        self.SRV.setStyleSheet("background-color: rgb(163, 163, 163);\n"
"background-color: rgb(255, 255, 255);")
        self.SRV.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.SRV.setFrameShadow(QtWidgets.QFrame.Raised)
        self.SRV.setObjectName("SRV")
        self.SRV_label = QtWidgets.QLabel(self.SRV)
        self.SRV_label.setGeometry(QtCore.QRect(10, 0, 111, 41))
        self.SRV_label.setObjectName("SRV_label")
        self.ShowButton = QtWidgets.QPushButton(self.SRV)
        self.ShowButton.setGeometry(QtCore.QRect(160, 110, 91, 23))
        self.ShowButton.setStyleSheet("background-color: rgb(230, 230, 230);")
        self.ShowButton.setObjectName("ShowButton")
        self.ShowButton.clicked.connect(self.showSRVEntries)
        self.CreateButton = QtWidgets.QPushButton(self.SRV)
        self.CreateButton.setGeometry(QtCore.QRect(20, 60, 91, 23))
        self.CreateButton.setStyleSheet("background-color: rgb(230, 230, 230);")
        self.CreateButton.setObjectName("CreateButton")
        self.CreateButton.clicked.connect(self.showSRV)
        self.DeleteButton = QtWidgets.QPushButton(self.SRV)
        self.DeleteButton.setGeometry(QtCore.QRect(310, 60, 91, 23))
        self.DeleteButton.setStyleSheet("background-color: rgb(230, 230, 230);")
        self.DeleteButton.setObjectName("DeleteButton")
        self.DeleteButton.clicked.connect(lambda: self.uiSRV.deleteLista())
        self.layoutWidget = QtWidgets.QWidget(self.centralwidget)
        self.layoutWidget.setGeometry(QtCore.QRect(0, 0, 2, 2))
        self.layoutWidget.setObjectName("layoutWidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.layoutWidget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        ##REFERINTA CATRE POPOP UL DE SRV. DACA NU L-AS PUNE AICI, APLICATIA AR LUA CRASH DACA AS DA SHOW INAINTE DE CREATE
        self.uiSRV = Ui_SRV()
        MainWindow.setCentralWidget(self.centralwidget)
        self.RenameButton.clicked.connect(self.changeName)
        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def showSRV(self):
        self.Form = QtWidgets.QWidget()
        self.uiSRV.setupUi(self.Form, self)
        self.Form.show()

    def showSRVEntries(self):
        self.uiShowSRV = Ui_ShowSRV()
        self.Form1 = QtWidgets.QWidget()
        self.Form1.setGeometry(237, 591, 200,200)
        self.uiShowSRV.setupUi(self.Form1)
        self.Form1.show()
        entries=self.uiSRV.getLista()
        for entry in entries:
            self.uiShowSRV.WriteSRVEntries.insertPlainText(entry.print()+"\n")

    def closeSrv(self):
        self.Form.close();

    def getDomainName(self):
        name=self.WriteDomainName.text()
        name+='.local'
        self.WriteDomainName.clear()
        #print(name)
        boolv =checkDevicesDuplicate(name)
        if(boolv):
            try:
                UDP.registerDevice(self.UDP_local,name)
            except BaseException as err:
                print("Eroare la inregistrarea unui device..."+err)
                raise
        else:
            error_dialog = QtWidgets.QErrorMessage()
            error_dialog.showMessage('Deja exista un device cu acest nume.')
            error_dialog.exec_()
    def changeName(self):
        old=self.WriteOldName.text()
        old+='.local'
        new=self.WriteNewName.text()
        new+='.local'

        if(not checkDevicesDuplicate(old)):
            try:
                renameDevice(old,new)
            except Exception as e:
                print(str(e))
        else:
            error_dialog = QtWidgets.QErrorMessage()
            error_dialog.showMessage('Numele pe care doriti sa-l schimbati nu exista.')
            error_dialog.exec_()


    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Responder"))
        self.Add_device_label.setText(_translate("MainWindow", "<html><head/><body><p><span style=\" font-size:14pt; font-weight:600;\">Add device</span></p></body></html>"))
        self.Domain_name_label.setText(_translate("MainWindow", "<html><head/><body><p><span style=\" font-size:12pt;\">Domain name:</span></p><p><span style=\" font-size:12pt;\"><br/></span></p></body></html>"))
        self.AddButton.setText(_translate("MainWindow", "Add"))
        self.Rename_domain_label.setText(_translate("MainWindow", "<html><head/><body><p><span style=\" font-size:14pt; font-weight:600;\">Rename domain name</span></p><p><br/></p></body></html>"))
        self.Old_name_label.setText(_translate("MainWindow", "<html><head/><body><p><span style=\" font-size:12pt;\">Old name:</span></p><p><br/></p></body></html>"))
        self.New_name_label.setText(_translate("MainWindow", "<html><head/><body><p><span style=\" font-size:12pt;\">New name:</span></p><p><br/></p></body></html>"))
        self.RenameButton.setText(_translate("MainWindow", "Rename"))
        self.SRV_label.setText(_translate("MainWindow", "<html><head/><body><p><span style=\" font-size:14pt; font-weight:600;\">SRV</span></p></body></html>"))
        self.ShowButton.setText(_translate("MainWindow", "Show"))
        self.CreateButton.setText(_translate("MainWindow", "Create"))
        self.DeleteButton.setText(_translate("MainWindow", "Delete"))




def startInterface(udp):
    app = QtWidgets.QApplication(sys.argv)
    ResolverWindow = QtWidgets.QMainWindow()
    uiResolver = Ui_MainWindow()
    uiResolver.setupUi(ResolverWindow)
    ResolverWindow.setGeometry(961, 194, uiResolver.height, uiResolver.weight)
    ResolverWindow.show()

    ResponderWindow = QtWidgets.QMainWindow()
    uiResponder = Ui_Responder()
    Ui_Responder.set_UDP(uiResponder,udp)
    uiResponder.setupUi(ResponderWindow)
    ResponderWindow.setGeometry(498, 194, uiResolver.height, uiResolver.weight)
    ResponderWindow.show()
    sys.exit(app.exec_())
