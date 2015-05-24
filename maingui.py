# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'untitled.ui'
#
# Created: Thu Mar 12 11:00:37 2015
#      by: PyQt4 UI code generator 4.11.3
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui
from matplotlib.backend_bases import *
try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName(_fromUtf8("MainWindow"))
        MainWindow.resize(1280, 700)
        self.centralwidget = QtGui.QWidget(MainWindow)
        #self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
        self.widget = matplotlibWidget(self.centralwidget)
        self.widget.setGeometry(QtCore.QRect(0, 0, 1011, 661))
        self.widget.setObjectName(_fromUtf8("widget"))
        
        self.pushButton = QtGui.QPushButton(self.centralwidget)
        self.pushButton.setGeometry(QtCore.QRect(1040, 10, 75, 23))
        self.pushButton.setObjectName(_fromUtf8("pushButton"))
        
        self.pushButton1 = QtGui.QPushButton(self.centralwidget)
        self.pushButton1.setGeometry(QtCore.QRect(1040, 50, 75, 23))
        self.pushButton1.setObjectName(_fromUtf8("otworzButtton"))
        
        self.pushButton2 = QtGui.QPushButton(self.centralwidget)
        self.pushButton2.setGeometry(QtCore.QRect(1040, 90, 75, 23))
        self.pushButton2.setObjectName(_fromUtf8("eksportujButton"))
        
        self.lewyTekst = QtGui.QLabel('lewy punkt: ----------',self.centralwidget)
        self.lewyTekst.move(1040, 120)
        self.lewyTekst.setObjectName(_fromUtf8("lewyTekst"))
        
        self.srodekTekst = QtGui.QLabel(u'środkowy punkt: ----------',self.centralwidget)
        self.srodekTekst.move(1040, 150)
        self.srodekTekst.setObjectName(_fromUtf8("srodekTekst"))
        
        self.prawyTekst = QtGui.QLabel('prawy punkt: ----------',self.centralwidget)
        self.prawyTekst.move(1040, 180)
        self.prawyTekst.setObjectName(_fromUtf8("prawyTekst"))
        
        self.maxlewyTekst = QtGui.QLabel('lewe max: -------------------------------',self.centralwidget)
        self.maxlewyTekst.move(1040, 210)
        self.maxlewyTekst.setObjectName(_fromUtf8("lewyTekst"))
        
        self.maxprawyTekst = QtGui.QLabel('prawe maxt: -----------------------------',self.centralwidget)
        self.maxprawyTekst.move(1040, 240)
        self.maxprawyTekst.setObjectName(_fromUtf8("prawyTekst"))
        
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtGui.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1166, 21))
        self.menubar.setObjectName(_fromUtf8("menubar"))
        
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtGui.QStatusBar(MainWindow)
        self.statusbar.setObjectName(_fromUtf8("statusbar"))
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow", None))
        self.pushButton.setText(_translate("MainWindow", "dopasuj", None))
        self.pushButton1.setText(_translate("MainWindow", "otworz", None))
        self.pushButton2.setText(_translate("MainWindow", "eksportuj", None))

from matplotlibwidgetFile import matplotlibWidget
