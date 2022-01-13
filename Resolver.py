from PyQt5 import QtCore, QtGui, QtWidgets


devices= []
class Ui_MainWindow(object):
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
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

        self.RefreshButton.clicked.connect(self.displayDevices)
    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Resolver"))
        self.RefreshButton.setText(_translate("MainWindow", "Refresh"))
        self.Nume_echip_label.setText(_translate("MainWindow", "<html><head/><body><p><span style=\" font-size:14pt;\">Nume echipament</span></p><p><br/></p></body></html>"))
        self.Tip_echip_label.setText(_translate("MainWindow", "<html><head/><body><p><span style=\" font-size:14pt;\">Tip echipament</span></p></body></html>"))

    def displayDevices(self):
        try:
            filterNume=self.WriteNumeEchip.text()
            if (filterNume==''):
                self.EcranReadOnly.clear()
                for device in devices:
                    self.EcranReadOnly.insertPlainText(device[0]+"  "+device[1] + '\n')
            else:
                self.EcranReadOnly.clear()
                for device in devices:
                    if device[0].find(filterNume)!=-1:
                        self.EcranReadOnly.insertPlainText(device[0] + "  " + device[1] + '\n')
        except Exception as e:
            print(str(e))


def addDevices(deviceName):
    devices.append(deviceName)

def renameDevice(old,new):
    for x in devices:

        if x[0]==old:
            x[0]=new

def checkDevicesDuplicate(deviceName):
    for x in devices:
        if x[0]==deviceName:
            return False

    return True






