import sys
from maingui import *
from dane import *
import random
from matplotlib.backend_bases import *
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
from scipy import exp
from os import listdir
from os.path import isfile, join
from PyQt4 import QtGui,QtCore
from matplotlib.backends.backend_qt4agg import NavigationToolbar2QT as NavigationToolbar2

class GUIForm(QtGui.QMainWindow):

	m1=[0,0]
	m2=[0,0]
	licznik=0
	licznik2=0
	listaDanych =[]
	pliki = []
	dane =dane()
	linie = [0,0,0]
	punkty =[0,0]
	def __init__(self, parent=None):
		#QtGui.QColorDialog.getColor()
		QtGui.QWidget.__init__(self,parent)
		self.ui = Ui_MainWindow()
		self.ui.setupUi(self)
		self.ui.widget.canvas.mpl_connect('button_press_event',self.klikniety)
		QtCore.QObject.connect(self.ui.pushButton, QtCore.SIGNAL('clicked()'),lambda: self.PlotFunc())
		QtCore.QObject.connect(self.ui.pushButton1, QtCore.SIGNAL('clicked()'),lambda: self.OtworzPliki())
		QtCore.QObject.connect(self.ui.pushButton2, QtCore.SIGNAL('clicked()'),lambda: self.EksportujDane())
		
		self.ui.lewyTekst.mousePressEvent = self.lewyTekstonClick
		self.ui.srodekTekst.mousePressEvent = self.srodekTekstonClick
		self.ui.prawyTekst.mousePressEvent = self.prawyTekstonClick
		self.ui.maxlewyTekst.mousePressEvent = self.lewymaxTekstonClick
		#print self.licznik
		
		
	def lewyTekstonClick(self,licznik):
		self.licznik = 0
		print self.licznik
			
	def srodekTekstonClick(self,licznik):
		self.licznik=1
		print self.licznik
		
	def prawyTekstonClick(self,licznik):
		self.licznik=2	
		print self.licznik
		
	def lewymaxTekstonClick(self,licznik):
		self.licznik2=0
		
	def PlotFunc(self):
		if (type(self.linie[0]) == int or type(self.linie[1]) == int or type(self.linie[2]) == int or type(self.m1) == int or type(self.m2) == int):
			QtGui.QMessageBox.question(self, 'Blad dopasowania !',
			"Punkty dopasowania nie zostaly ustawione prawidlowo. Do dopasowania potrzeba 3 linii, oraz 2 maksimow", QtGui.QMessageBox.Ok, 
			 QtGui.QMessageBox.Ok)
		else:
			self.dane.dopasuj(self.linie[0].get_xdata()[0],self.linie[1].get_xdata()[0],self.linie[2].get_xdata()[0],self.m1,self.m2)	
			self.ui.widget.canvas.ax.clear()
			self.ui.widget.canvas.ax.plot(self.dane.y,'go')
			self.ui.widget.canvas.ax.plot(self.dane.x,self.dane.gaus2(self.dane.x,self.dane.popt[0],self.dane.popt[1],self.dane.popt[2],self.dane.popt[3],self.dane.popt[4],self.dane.popt[5]),'r',label='fit', linewidth=3.0)
			self.ui.widget.canvas.ax.plot(self.dane.x,self.dane.gaus(self.dane.x,self.dane.poptL[0],self.dane.poptL[1],self.dane.poptL[2]),'r--')
			self.ui.widget.canvas.ax.plot(self.dane.x,self.dane.gaus(self.dane.x,self.dane.poptR[0],self.dane.poptR[1],self.dane.poptR[2]),'r--')
			self.ui.widget.canvas.draw()
			self.m1=[0,0]
			self.m2=[0,0]
			self.linie = [0,0,0]
			self.licznik=0
			self.licznik2=0
			self.punkty = [0,0]
	def klikniety(self,event):

		klawisz = QtGui.QApplication.keyboardModifiers()
		if klawisz == QtCore.Qt.ControlModifier: #ctrl
			if len(self.pliki) == 0:
				QtGui.QMessageBox.question(self, 'Blad dopasowania !',
			"Zaznaczanie wartosci jest mozliwe dopiero po otwarciu plikow. Nacisnij przycisk otworz i wybierz pliki.", QtGui.QMessageBox.Ok, 
			 QtGui.QMessageBox.Ok)
			else:
				if event.button==1: #lpm
					if self.licznik <=2:#2
						if (type(self.linie[self.licznik]) != int) :
							self.linie[self.licznik].remove
							self.linie[self.licznik].remove()
							self.ui.widget.canvas.draw()
							
						self.linie[self.licznik]=self.ui.widget.canvas.ax.axvline(int (event.xdata), color='r', linestyle='solid')#pionowa kreska na wykresie
						if self.licznik==0:
							self.ui.lewyTekst.setText( "lewy punkt: "+( str(int(self.linie[0].get_xdata()[0]))))
							
						elif self.licznik==1:
							self.ui.srodekTekst.setText('srodkowy punkt: '+ str(int(self.linie[1].get_xdata()[0])))
							
						else:
							self.ui.prawyTekst.setText('prawy punkt: '+ str(int(self.linie[2].get_xdata()[0])))	
							
						
						if self.licznik <2 and (type(self.linie[self.licznik+1])) ==int:
							self.licznik=self.licznik+1
						
					if (self.licznik ==3 and type(self.linie[2]) != int):#2
						
						self.linie[2].remove
						self.linie[2].remove()
						self.linie[2]=self.ui.widget.canvas.ax.axvline(int (event.xdata), color='k', linestyle='solid')
						self.ui.widget.canvas.draw()
						#print self.licznik
						
				elif event.button==3: #ppm
					if self.licznik2<=1:
						#print self.punkty
						if (type(self.punkty[self.licznik2]) != int):
							self.punkty[self.licznik2].remove
							self.punkty[self.licznik2].remove()
							self.ui.widget.canvas.draw()
						self.punkty[self.licznik2] = plt.Circle((event.xdata,event.ydata),50,color='r')
						#print dir(self.punkty[1])
						if self.licznik2 ==0:
							self.m1=int(event.xdata),int(event.ydata)
							self.ui.maxlewyTekst.setText("lewe max: " + str (self.m1))
							self.ui.widget.canvas.ax.add_artist(self.punkty[self.licznik2])
							
							if type(self.punkty[1]) == int:
								self.licznik2=self.licznik2+1
							
						else:
							self.m2=int(event.xdata),int(event.ydata)
							self.ui.maxprawyTekst.setText("prawe max: "+str(self.m2))
							self.punkty[self.licznik2] = plt.Circle((event.xdata,event.ydata),50,color='r')
							
							self.ui.widget.canvas.ax.add_artist(self.punkty[1])
							
						if self.licznik ==1 and type(self.punkty[1] != int):
							self.punkty[1].remove
							self.punkty[1].remove()
							self.punkty[1] = plt.Circle((event.xdata,event.ydata),50,color='r')
							self.m2=event.xdata,event.ydata
							self.ui.widget.canvas.ax.add_artist(self.punkty[1])
							self.ui.widget.canvas.draw()
			self.ui.widget.canvas.draw()
		
		
	def EksportujDane(self):
		if type(self.dane.pcov) ==int:
			QtGui.QMessageBox.question(self, 'Blad eksportowania !',
			"Aby eksportowac dane do pliku krzywe musza zostac dopasowane. Zaznacz punkty i dopasuj krzywe", QtGui.QMessageBox.Ok, 
			 QtGui.QMessageBox.Ok)
		else:
			
			plik = QtGui.QFileDialog.getSaveFileName(self, 'Dialog Title', selectedFilter='*.dat')
			if plik:
				self.dane.zapiszDane(plik)
			
	def OtworzPliki(self):
		self.pliki =[]
		self.dane = dane()
		for path in QtGui.QFileDialog.getOpenFileNames(self, 'Open File',".","(*.dat)"):
			self.pliki.append(str(path))
			print str(path)
		if len(self.pliki)>0:
			for path in self.pliki:
				self.dane.wczytajDane(str(path))

			self.listaDanych.append(self.dane)
			
			for i  in self.listaDanych:		
				self.ui.widget.canvas.ax.plot(self.dane.y,'o')	
				self.ui.widget.canvas.draw()

			self.linie = [0,0,0]
			self.licznik=0
			self.ui.lewyTekst.setText( "lewy punkt: ")
			self.ui.prawyTekst.setText( "prawy punkt: ")
			self.ui.srodekTekst.setText( "srodkowy punkt: ")
			self.ui.maxlewyTekst.setText("lewe max: ")
			self.ui.maxprawyTekst.setText("prawe max: ")

	def closeEvent(self, event):
		sound_file = "Windows Exclamation.wav"
		QtGui.QSound.play(sound_file)       
		odp = QtGui.QMessageBox.question(self, 'Uwaga !',
			"Czy na pewno zamknac?", QtGui.QMessageBox.Yes | 
			QtGui.QMessageBox.No, QtGui.QMessageBox.No)
		
		if odp == QtGui.QMessageBox.Yes:
			QtGui.QApplication.quit()
			event.accept()
			sys.exit(app.exec_())
			
			
		else:
			event.ignore()  


if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    myapp = GUIForm()
    myapp.show()
    sys.exit(app.exec_())
