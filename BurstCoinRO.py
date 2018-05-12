from decimal import Decimal
import time
import datetime
import requests
import sys
import os.path
import webbrowser
import configparser
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QLabel, QLineEdit, QGridLayout, QComboBox, QDesktopWidget
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import pyqtSlot, QTimer, Qt

class App (QWidget):
    
    def __init__(self):
        super().__init__()
        self.title = 'BurstCoin.RO Pending Notifier'
        self.width = 360
        self.height = 100
        self.initUI()

    def closeEvent(self, event):
        saveSettings(self)
        event.accept()
        sys.exit(0)
    
    def initUI(self):
        self.setWindowTitle(self.title)
        self.setWindowIcon(QIcon('RO.jpg'))

        self.poolSelect = QComboBox(self)
        self.poolSelect.addItem("pool.burstcoin.ro")
        self.poolSelect.addItem("0-100pool.burstcoin.ro")
        
        self.textbox = QLineEdit(self)
        self.textbox.setPlaceholderText("Enter Burst Address or Numeric ID")

        self.donate = QPushButton('Donate', self)
        self.donate.setToolTip('If you like this app and want to thank the dev')
        self.donate.clicked.connect(self.on_click)
        
        self.pendingLabel = QLabel('Pending:')
        self.pendingAmount = QLabel('')

        self.refreshTime = QLineEdit(self)
        self.refreshTime.setPlaceholderText('Refresh Time (Minutes)')

        self.balLabel = QLabel('Wallet Balance:')
        self.bal = QLabel('')

        file = 'settings.ini'
        if os.path.isfile(file):
            loadSettings(self)
               
        grid = QGridLayout()
        self.setLayout(grid)
        grid.addWidget(self.textbox, 0,0)
        grid.addWidget(self.donate, 0, 1)
        grid.addWidget(self.pendingLabel,1,0) 
        grid.addWidget(self.pendingAmount,1,1)
        grid.addWidget(self.poolSelect, 2, 0)
        grid.addWidget(self.refreshTime, 2, 1)
        grid.addWidget(self.balLabel, 3, 0)
        grid.addWidget(self.bal, 3, 1)

        self.center()
        self.show()
        self.update()

    def center(self):
        frameGm = self.frameGeometry()
        screen = QApplication.desktop().screenNumber(QApplication.desktop().cursor().pos())
        centerPoint = QApplication.desktop().screenGeometry(screen).center()
        frameGm.moveCenter(centerPoint)
        self.move(frameGm.topLeft())

    @pyqtSlot()
    def on_click(self):
        webbrowser.open('https://github.com/thothloki/BurstCoinROPendingNotifier/blob/master/README.md')
        
    def update(self):
        self.delay = 10000
        try:
            addy = (self.textbox.text())
            if addy == '':
                self.pendingAmount.setText('0')
                self.delay = 5000
            else:
                addy = convert(addy)
                addy2 = str(addy)

                if self.poolSelect.currentText() == 'pool.burstcoin.ro':
                    URL = ("https://pool.burstcoin.ro/static/pending.json")
                elif self.poolSelect.currentText() == '0-100pool.burstcoin.ro':
                    URL = ("https://0-100pool.burstcoin.ro/static/pending.json")
                r = requests.get(url = URL)
                self.data = r.json()

                self.bar = ((self.data[addy]))
                #print (self.bar)

                self.balance = getBal(addy)
                
                self.pendingAmount.setText(str(self.bar) + ' Burst')
                self.bal.setText(str(self.balance) + ' BURST')                

                self.timeD = (self.refreshTime.text())
                if self.timeD != '' and self.timeD.isdigit():
                    customerDelayTime = delayTime(self.timeD)
                    self.delay = customerDelayTime
                else:
                    self.delay = 360000
        except:
            QTimer.singleShot(self.delay, self.update)
            print('error')
        finally:
            QTimer.singleShot(self.delay, self.update)

        
def convert(addy):
    burst = addy
    try:
        URL = ("https://wallet1.burstnation.com:8125/burst?requestType=rsConvert&account=" + burst)
        r = requests.get(url = URL)
        data = r.json()
        numeric = data['account']
        return numeric
    except:
        numeric = ''
        return numeric

def getBal(addy):
    burst = addy
    try:
        URL = ("https://explore.burst.cryptoguru.org/api/v1/account/" + burst)
        r = requests.get(url = URL)
        data = r.json()
        bar = ((data['data'])['balance'])
        bal = (int(bar)/100000000)
        #print (bal)
        return bal
    except:
        bal = ''
        return bal


def delayTime(minutes):
    timeA = str(minutes)
    timeB = int(timeA)
    seconds = (timeB*60)
    raw = (seconds * 1000)
    return raw

def saveSettings(self):
    address = self.textbox.text()
    pool = self.poolSelect.currentText()
    refreshTime = self.refreshTime.text()
    settingsFile = 'settings.ini'
    config = configparser.ConfigParser()
    config['settings'] = {'address': address, 'pool': pool, 'refresh-time': refreshTime}
    with open(settingsFile, 'w') as configfile:
        config.write(configfile)

def loadSettings(self):
    config = configparser.ConfigParser()
    config.read('settings.ini')
    address = config['settings']['address']
    pool = config['settings']['pool']
    refreshTime = config['settings']['refresh-time']
    self.textbox.setText(str(address))
    index = self.poolSelect.findText(str(pool), Qt.MatchFixedString)
    if index >= 0:
        self.poolSelect.setCurrentIndex(index)
    self.refreshTime.setText(refreshTime)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())
