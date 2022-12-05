# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'main.ui'
#
# Created by: PyQt5 UI code generator 5.15.4
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_mainWindow(object):
    def setupUi(self, mainWindow):
        mainWindow.setObjectName("mainWindow")
        mainWindow.resize(1075, 767)
        mainWindow.setToolButtonStyle(QtCore.Qt.ToolButtonTextOnly)
        self.widget = QtWidgets.QWidget(mainWindow)
        self.widget.setObjectName("widget")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.widget)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.navGrid = QtWidgets.QVBoxLayout()
        self.navGrid.setObjectName("navGrid")
        self.gridLayout = QtWidgets.QGridLayout()
        self.gridLayout.setObjectName("gridLayout")
        self.srchBtn = QtWidgets.QPushButton(self.widget)
        self.srchBtn.setText("")
        self.srchBtn.setObjectName("srchBtn")
        self.gridLayout.addWidget(self.srchBtn, 0, 4, 1, 1)
        self.backwardBtn = QtWidgets.QPushButton(self.widget)
        self.backwardBtn.setText("")
        self.backwardBtn.setObjectName("backwardBtn")
        self.gridLayout.addWidget(self.backwardBtn, 0, 0, 1, 1)
        self.srchLine = QtWidgets.QLineEdit(self.widget)
        self.srchLine.setObjectName("srchLine")
        self.gridLayout.addWidget(self.srchLine, 0, 3, 1, 1)
        self.forwardBtn = QtWidgets.QPushButton(self.widget)
        self.forwardBtn.setText("")
        self.forwardBtn.setObjectName("forwardBtn")
        self.gridLayout.addWidget(self.forwardBtn, 0, 1, 1, 1)
        self.refreshBtn = QtWidgets.QPushButton(self.widget)
        self.refreshBtn.setText("")
        self.refreshBtn.setObjectName("refreshBtn")
        self.gridLayout.addWidget(self.refreshBtn, 0, 2, 1, 1)
        self.navGrid.addLayout(self.gridLayout)
        self.gridLayout_2.addLayout(self.navGrid, 0, 0, 1, 1)
        self.displayWgt = WebView(self.widget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.displayWgt.sizePolicy().hasHeightForWidth())
        self.displayWgt.setSizePolicy(sizePolicy)
        self.displayWgt.setObjectName("displayWgt")
        self.gridLayout_2.addWidget(self.displayWgt, 1, 0, 1, 1)
        mainWindow.setCentralWidget(self.widget)

        self.retranslateUi(mainWindow)
        QtCore.QMetaObject.connectSlotsByName(mainWindow)

    def retranslateUi(self, mainWindow):
        _translate = QtCore.QCoreApplication.translate
        mainWindow.setWindowTitle(_translate("mainWindow", "MainWindow"))
from utils import WebView
