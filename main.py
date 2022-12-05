from requests import Session
from urllib import parse
from GUI import Ui_mainWindow 
from PyQt5.QtWebEngineWidgets import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.uic import loadUi
from PyQt5.QtCore import *
from PyQt5 import *
import socket
import sys
import re

class Browser(QMainWindow):
    regex = re.compile('((https:\/\/|http:\/\/)?(www\.)?[\w]{2,20}(\.[a-z]{2,4}){1,3})')
    prevMousePos = QPointF()

    def __init__(self): 
        super().__init__()
        self.ui = Ui_mainWindow()
        self.ui.setupUi(self)
        self.ui.displayWgt.cookies.deleteAllCookies()
        self.__init_UI__()

    def __init_UI__(self): 
        self.prevGeo = self.geometry()   
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.CustomizeWindowHint | Qt.WindowStaysOnTopHint)
        # self.setAttribute(Qt.WA_TranslucentBackground, True)

        self.ui.head.installEventFilter(self)

        qtRectangle = self.frameGeometry()
        centerPoint = QDesktopWidget().availableGeometry().center()
        qtRectangle.moveCenter(centerPoint)
        self.move(qtRectangle.topLeft())

        self.ui.displayWgt.goto('https://google.com')
        self.setWindowOpacity(0.9)
        self.ui.opacityLab.setText(f'Opacity: {self.ui.opacitySld.value()}%')

        self.ui.srchBtn.clicked.connect(self.search)
        self.ui.srchLine.returnPressed.connect(self.search)
        self.ui.displayWgt.urlChanged.connect(lambda: self.ui.srchLine.setText(self.ui.displayWgt.url().toString()))
        self.ui.displayWgt.urlChanged.connect(lambda: self.ui.srchLine.setCursorPosition(0))
        self.ui.opacitySld.valueChanged.connect(lambda: self.setWindowOpacity(float(self.ui.opacitySld.value()/100)))
        self.ui.opacitySld.valueChanged.connect(lambda: self.ui.opacityLab.setText(f'Opacity: {self.ui.opacitySld.value()}%'))
        self.ui.backwardBtn.pressed.connect(self.ui.displayWgt.back)
        self.ui.forwardBtn.pressed.connect(self.ui.displayWgt.forward)
        self.ui.refreshBtn.pressed.connect(self.ui.displayWgt.reload)
        self.ui.sizeAdjustBtn.clicked.connect(lambda: self.setWindowState(self.windowState() ^ Qt.WindowState.WindowMaximized))
        self.ui.closeBtn.clicked.connect(self.close)

        self.show()

    def search(self):
        text = self.ui.srchLine.text()
        if self.regex.match(text):
            if not re.match('https://|http://', text): text = 'https://' + text
            url = text
        else:
            url = f'https://www.google.com/search?' + parse.urlencode({'q':text})
        self.ui.srchLine.setText(url)
        self.ui.displayWgt.goto(url)

    def eventFilter(self, obj: QObject, event: QEvent):
        if obj.objectName() == 'head':
            if not self.ui.closeBtn.underMouse() or self.ui.sizeAdjustBtn.underMouse():
                if event.type() == QEvent.MouseButtonDblClick: # Change between fullscreen and normal size with double click
                    self.setWindowState(self.windowState() ^ Qt.WindowState.WindowMaximized)
                    return True

                if event.type() == QEvent.MouseButtonRelease: # Detect if drop the window in the top of the screen to maximize 
                    if event.globalPos().y() < 10 and self.moved:
                        # self.prevGeo = self.geometry()
                        self.showMaximized()
                        return True

                if event.type() == QEvent.MouseButtonPress:
                    if event.button() == Qt.MouseButton.LeftButton:
                        self.prevMousePos = event.globalPos()
                    if event.button() == Qt.MouseButton.BackButton:
                        self.ui.displayWgt.back()
                
                if event.type() == QEvent.MouseMove:
                    if self.windowState() == Qt.WindowFullScreen or self.windowState() == Qt.WindowMaximized:
                        self.showNormal()
                        # self.prevMousePos = QPointF(self.prevGeo.width()*.7,5)
                    if  event.buttons() == Qt.MouseButton.LeftButton:
                        delta = QPointF(event.globalPos() - self.prevMousePos)

                        self.move(int(self.x() + delta.x()), int(self.y() + delta.y()))
                        self.prevMousePos = event.globalPos()
                        self.moved = True

        return super().eventFilter(obj, event)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = Browser()
    app.exec()