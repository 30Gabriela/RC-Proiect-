from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QMessageBox
from SRV_record import SRVs
devices= []
UDP_server=None

class Ui_MainWindow(object):
    UDP_local = None

    def set_UDP(self, udp):
        global UDP_server
        # global UDP_local
        self.UDP_local = udp
        UDP_server=udp

    def setupUi(self, MainWindow):
        self.height=462
        self.weight=635
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(self.height,self.weight);
        MainWindow.setMinimumSize(QtCore.QSize(462, 635))
        MainWindow.setMaximumSize(QtCore.QSize(462, 635))
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.MainFrame = QtWidgets.QFrame(self.centralwidget)
        self.MainFrame.setGeometry(QtCore.QRect(-140, -80, 811, 941))
        self.MainFrame.setStyleSheet("background-color: rgb(216, 238, 240);")
        self.MainFrame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.MainFrame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.MainFrame.setObjectName("MainFrame")
        self.EcranReadOnly = QtWidgets.QTextEdit(self.MainFrame)
        self.EcranReadOnly.setGeometry(QtCore.QRect(150, 100, 441, 421))
        self.EcranReadOnly.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.EcranReadOnly.setReadOnly(True)
        self.EcranReadOnly.setObjectName("EcranReadOnly")
        self.RefreshButton = QtWidgets.QPushButton(self.MainFrame)
        self.RefreshButton.setGeometry(QtCore.QRect(150, 530, 101, 21))
        self.RefreshButton.setStyleSheet("background-color: rgb(230, 230, 230);")
        self.RefreshButton.setObjectName("RefreshButton")
        self.Nume_echip_label = QtWidgets.QLabel(self.MainFrame)
        self.Nume_echip_label.setGeometry(QtCore.QRect(160, 570, 171, 41))
        self.Nume_echip_label.setObjectName("Nume_echip_label")
        self.Tip_echip_label = QtWidgets.QLabel(self.MainFrame)
        self.Tip_echip_label.setGeometry(QtCore.QRect(420, 560, 171, 41))
        self.Tip_echip_label.setObjectName("Tip_echip_label")
        self.WriteNumeEchip = QtWidgets.QLineEdit(self.MainFrame)
        self.WriteNumeEchip.setGeometry(QtCore.QRect(150, 610, 201, 31))
        self.WriteNumeEchip.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.WriteNumeEchip.setObjectName("WriteNumeEchip")
        self.WriteTipEchip = QtWidgets.QLineEdit(self.MainFrame)
        self.WriteTipEchip.setGeometry(QtCore.QRect(380, 610, 201, 31))
        self.WriteTipEchip.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.WriteTipEchip.setObjectName("WriteTipEchip")
        self.ACLOGO = QtWidgets.QLabel(self.MainFrame)
        self.ACLOGO.setGeometry(QtCore.QRect(540, 650, 51, 51))
        self.ACLOGO.setText("")
        self.ACLOGO.setPixmap(QtGui.QPixmap("cropped-logo_ac_iasi.qrc.png"))
        self.ACLOGO.setScaledContents(True)
        self.ACLOGO.setObjectName("ACLOGO")
        self.ACLOGO_2 = QtWidgets.QLabel(self.MainFrame)
        self.ACLOGO_2.setGeometry(QtCore.QRect(150, 650, 51, 51))
        self.ACLOGO_2.setText("")
        self.ACLOGO_2.setPixmap(QtGui.QPixmap("cropped-logo_ac_iasi.qrc.png"))
        self.ACLOGO_2.setScaledContents(True)
        self.ACLOGO_2.setObjectName("ACLOGO_2")
        self.comboBoxDevice= QtWidgets.QComboBox(self.MainFrame)
        self.comboBoxDevice.setGeometry(QtCore.QRect(430, 530, 101, 21))
        self.comboBoxDevice.setObjectName("comboBoxDevice")
        self.popupSRV = QtWidgets.QPushButton(self.MainFrame)
        self.popupSRV.setGeometry(QtCore.QRect(540, 529, 50, 21))
        self.popupSRV.setStyleSheet("background-color: rgb(230, 230, 230);")
        self.popupSRV.setObjectName("popupSRV")
        MainWindow.setCentralWidget(self.centralwidget)

        self.popupSRV.clicked.connect(self.SRVshowButton)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

        self.RefreshButton.clicked.connect(self.displayDevices)
    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Resolver"))
        self.RefreshButton.setText(_translate("MainWindow", "Refresh"))
        self.popupSRV.setText(_translate("MainWindow", "Show"))
        self.Nume_echip_label.setText(_translate("MainWindow", "<html><head/><body><p><span style=\" font-size:14pt;\">Nume echipament</span></p><p><br/></p></body></html>"))
        self.Tip_echip_label.setText(_translate("MainWindow", "<html><head/><body><p><span style=\" font-size:14pt;\">Tip echipament</span></p></body></html>"))

    def displayDevices(self):
        self.comboBoxDevice.clear()
        for x in range(len(devices)):
            self.comboBoxDevice.addItem(str(x+1))
        try:
            filterNume=self.WriteNumeEchip.text()
            filterServiciu = self.WriteTipEchip.text()
            if (filterNume=='' and filterServiciu==''):
                self.EcranReadOnly.clear()
                for device in devices:
                    self.EcranReadOnly.insertPlainText(str(devices.index(device)+1)+")\t "+device[0]+"\t "+device[1] + '\n')

            elif(filterServiciu==''):
                self.EcranReadOnly.clear()
                for device in devices:
                    if device[0].find(filterNume)!=-1:
                        self.EcranReadOnly.insertPlainText(str(devices.index(device)+1)+")\t "+device[0]+"\t "+device[1] + '\n')
            elif(filterNume==''):
                self.EcranReadOnly.clear()
                for device in devices:
                    for srv in SRVs:
                        if device[0]==srv.target:
                            if srv.name_service.find(filterServiciu)!=-1:
                                self.EcranReadOnly.insertPlainText(
                                    str(devices.index(device) + 1) + ")\t " + device[0] + "\t " + device[1] + '\n')
            else:
                self.EcranReadOnly.clear()
                for device in devices:
                    for srv in SRVs:
                        if device[0] == srv.target:
                            if (srv.domain_name.find(filterServiciu) != -1 and device[0].find(filterNume)!=-1):
                                self.EcranReadOnly.insertPlainText(
                                    str(devices.index(device) + 1) + ")\t " + device[0] + "\t " + device[1] + '\n')



        except Exception as e:
            print(str(e))


    def SRVshowButton(self):
        id=self.comboBoxDevice.currentText()

        try:
            msg = QMessageBox()
            msg.setWindowTitle("SRV")
            msg.setText("Lista SRV uri pentru device ul cu numele:   {} ".format(str(devices[int(id)-1][0])))
            string=""
            for x in SRVs:
                if x.target==str(devices[int(id)-1][0]):
                    string+=x.print()+"\n"
            msg.setDetailedText(string)
            x = msg.exec_()
        except Exception as e:
            print(e)


def addDevices(deviceName):
    devices.append(deviceName)


def renameDevice(old,new):
    try:
        UDP_server.query_name(old)
    except Exception as err:
        print(err)
    for x in devices:

        if x[0]==old:
            x[0]=new
            UDP_server.send_DNS_answer(x[1],new)
            print("x:..........",x)

def checkDevicesDuplicate(deviceName):
    for x in devices:
        if x[0]==deviceName:
            return False

    return True

def get_address_of_host(deviceName):
    for x in devices:
        if x[0]==deviceName:
            return x[1]

    return '0.0.0.0'

"""
Interfata pentru SRV in forma de tabela daca este timp :)
class Ui_Form(object):
    def setupUi(self, Form):
        if not Form.objectName():
            Form.setObjectName(u"Form")
        Form.resize(575, 455)
        Form.setMinimumSize(QSize(575, 455))
        Form.setMaximumSize(QSize(575, 455))
        self.MainFrame = QFrame(Form)
        self.MainFrame.setObjectName(u"MainFrame")
        self.MainFrame.setGeometry(QRect(-51, -91, 1581, 1021))
        self.MainFrame.setFrameShape(QFrame.StyledPanel)
        self.MainFrame.setFrameShadow(QFrame.Raised)
        self.tableWidget = QTableWidget(self.MainFrame)
        if (self.tableWidget.columnCount() < 7):
            self.tableWidget.setColumnCount(7)
        font = QFont()
        font.setPointSize(10)
        __qtablewidgetitem = QTableWidgetItem()
        __qtablewidgetitem.setFont(font);
        self.tableWidget.setHorizontalHeaderItem(0, __qtablewidgetitem)
        __qtablewidgetitem1 = QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(1, __qtablewidgetitem1)
        __qtablewidgetitem2 = QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(2, __qtablewidgetitem2)
        __qtablewidgetitem3 = QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(3, __qtablewidgetitem3)
        __qtablewidgetitem4 = QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(4, __qtablewidgetitem4)
        __qtablewidgetitem5 = QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(5, __qtablewidgetitem5)
        __qtablewidgetitem6 = QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(6, __qtablewidgetitem6)
        self.tableWidget.setObjectName(u"tableWidget")
        self.tableWidget.setGeometry(QRect(45, 91, 581, 461))

        self.retranslateUi(Form)

        QMetaObject.connectSlotsByName(Form)
    # setupUi

    def retranslateUi(self, Form):
        Form.setWindowTitle(QCoreApplication.translate("Form", u"SRV", None))
        ___qtablewidgetitem = self.tableWidget.horizontalHeaderItem(0)
        ___qtablewidgetitem.setText(QCoreApplication.translate("Form", u"Name", None));
        ___qtablewidgetitem1 = self.tableWidget.horizontalHeaderItem(1)
        ___qtablewidgetitem1.setText(QCoreApplication.translate("Form", u"Protocol", None));
        ___qtablewidgetitem2 = self.tableWidget.horizontalHeaderItem(2)
        ___qtablewidgetitem2.setText(QCoreApplication.translate("Form", u"Domain", None));
        ___qtablewidgetitem3 = self.tableWidget.horizontalHeaderItem(3)
        ___qtablewidgetitem3.setText(QCoreApplication.translate("Form", u"TTL", None));
        ___qtablewidgetitem4 = self.tableWidget.horizontalHeaderItem(4)
        ___qtablewidgetitem4.setText(QCoreApplication.translate("Form", u"Priority", None));
        ___qtablewidgetitem5 = self.tableWidget.horizontalHeaderItem(5)
        ___qtablewidgetitem5.setText(QCoreApplication.translate("Form", u"Weight", None));
        ___qtablewidgetitem6 = self.tableWidget.horizontalHeaderItem(6)
        ___qtablewidgetitem6.setText(QCoreApplication.translate("Form", u"Port", None));
    # retranslateUi

"""


