from requests import Session
from urllib import parse
from GUI import Ui_mainWindow 
from PyQt5.QtWebEngineWidgets import *
from PyQt5.QtWidgets import *
from PyQt5.uic import loadUi
from PyQt5.QtCore import *
from PyQt5 import *
import socket
import sys
import re

class Browser(QMainWindow):
    regex = re.compile('((https:\/\/|http:\/\/)?(www\.)?[\w]{2,20}(\.[a-z]{2,4}){1,3})')

    def __init__(self): 
        super().__init__()
        self.ui = Ui_mainWindow()
        self.ui.setupUi(self)
        self.s = Session()
        self.s.headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:71.0) Gecko/20100101 Firefox/71.0'}

        self.ui.srchBtn.clicked.connect(self.search)
        self.ui.srchLine.returnPressed.connect(self.search)
        self.ui.displayWgt.urlChanged.connect(lambda: self.ui.srchLine.setText(self.ui.displayWgt.url().toString()))
        self.ui.displayWgt.urlChanged.connect(lambda: self.ui.srchLine.setCursorPosition(0))
        self.ui.backwardBtn.pressed.connect(self.ui.displayWgt.back)
        self.ui.forwardBtn.pressed.connect(self.ui.displayWgt.forward)
        self.ui.refreshBtn.pressed.connect(self.ui.displayWgt.reload)
        self.setWindowOpacity(0.85)
        self.ui.displayWgt.goto('https://google.com')

        self.setWindowFlags(Qt.Window | Qt.CustomizeWindowHint | Qt.WindowCloseButtonHint | Qt.WindowStaysOnTopHint)

        self.show()

    def search(self):
        text = self.ui.srchLine.text()
        if self.regex.match(text):
            if not re.match('https://|http://', text): text = 'https://' + text
            # ans = self.s.get(url=text)
            url = text
        else:
            url = f'https://www.google.com/search?' + parse.urlencode({'q':text})
        self.ui.srchLine.setText(url)
        self.ui.displayWgt.goto(url)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = Browser()
    app.exec()