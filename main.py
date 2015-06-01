# -*- coding: utf-8 -*-
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
from os.path import isfile, join,basename
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
	osx = [0,0]
	osy= [0,0]
	nrwykresu=[0] #lista przekazywana przez referencje / int przez wartosc https://sites.google.com/site/usfcomputerscience/functions-and-parameters
	def __init__(self, parent=None):

		QtGui.QWidget.__init__(self,parent)
		self.ui = Ui_MainWindow()
		self.ui.setupUi(self)
		self.ui.widget.canvas.mpl_connect('button_press_event',self.klikniety)
		info = self.ui.menubar.addMenu(' O programie')
		info.addAction('Instrukcja',self.wyswietlInstrukcje)
		info.addAction('o Autorze', self.wyswietlAutor)
		
		QtCore.QObject.connect(self.ui.pushButton, QtCore.SIGNAL('clicked()'),lambda: self.PlotFunc())
		QtCore.QObject.connect(self.ui.pushButton1, QtCore.SIGNAL('clicked()'),lambda: self.OtworzPliki())
		QtCore.QObject.connect(self.ui.pushButton2, QtCore.SIGNAL('clicked()'),lambda: self.EksportujDane())
		QtCore.QObject.connect(self.ui.pushButton3, QtCore.SIGNAL('clicked()'),lambda: self.resetujWartosci())
		
		self.ui.lewyTekst.mousePressEvent = self.lewyTekstonClick
		self.ui.srodekTekst.mousePressEvent = self.srodekTekstonClick
		self.ui.prawyTekst.mousePressEvent = self.prawyTekstonClick
		self.ui.maxlewyTekst.mousePressEvent = self.lewymaxTekstonClick

	
	
	def wyswietlInstrukcje(self):
		t= u"Instrukcja obsługi programu. \n  Aby załadować pliki należy nacisnać przycisk otwórz, wybrać pliki, oraz zatwierdzić wybór. W celu porównania kilku widm  \
istnieje możliwość wczytania kolejnych plików. Po wybraniu plików należy przystąpić do zaznaczenia miejsca do którego zostaną dopasowane krzywe. Aby tego dokonać  \
należy nacisnąć lewy CTRL i kliknięciami LPM wskazać kolejno lewy, środkowy oraz prawy punkt krzywej. Następnie należy wcisnać CTRL i PPM wskazać lewe oraz prawe maksima krzywej. \
W razie pomyłki istnieje możliwość zmiany punktów poprzez klikniecie napisu parametru który chcemy zmienić oraz wskazanie nowego punktu. Gdy parametry są juz dopasowane należy nacisnąć \
przycisk dopasuj. Po dopasowaniu istnieje możliwość eksportowania danych do pliku .dat. Krzywa zostaje dopasowywana do ostatnio otwartego pliku z danymi."
		 
		QtGui.QMessageBox.information(self, 'Instrukcja',
			t, QtGui.QMessageBox.Ok, 
			 QtGui.QMessageBox.Ok)
	
	def wyswietlAutor(self):
		t=u"Autor: Przemysław Lewandowski, kontakt  przemek1648@wp.pl" 
		QtGui.QMessageBox.information(self, 'Instrukcja',
			t, QtGui.QMessageBox.Ok, 
			 QtGui.QMessageBox.Ok)
			 
	def lewyTekstonClick(self,licznik):
		self.licznik = 0

			
	def srodekTekstonClick(self,licznik):
		self.licznik=1

		
	def prawyTekstonClick(self,licznik):
		self.licznik=2	

		
	def lewymaxTekstonClick(self,licznik):
		self.licznik2=0
		
	def PlotFunc(self):
		
		if (type(self.linie[0]) == int or type(self.linie[1]) == int or type(self.linie[2]) == int or type(self.m1) == int or type(self.m2) == int):
			QtGui.QMessageBox.critical(self, u'Błąd dopasowania !',
			u"Punkty dopasowania nie zostaly ustawione prawidlowo. Do dopasowania potrzeba 3 linii, oraz 2 maksimow", QtGui.QMessageBox.Ok, 
			 QtGui.QMessageBox.Ok)
		else:
			if self.m1==[0,0]:
				self.m1 =  self.dane.wybierzMaxPunkt(int(self.linie[0].get_xdata()[0]),int(self.linie[1].get_xdata()[0]))
				self.ui.maxlewyTekst.setText("lewe max: " + str (self.m1))
			if self.m2 == [0,0]:
				self.m2 = self.dane.wybierzMaxPunkt(int(self.linie[1].get_xdata()[0]),int(self.linie[2].get_xdata()[0]))
				self.ui.maxprawyTekst.setText("prawe max: "+str(self.m2))
			self.osx = self.ui.widget.canvas.ax.get_xlim()
			self.osy = self.ui.widget.canvas.ax.get_ylim()

			self.dane.popt = 0
			self.dane.poptL = 0
			self.dane.poptR = 0
			try:
				self.dane.dopasuj(self.linie[0].get_xdata()[0],self.linie[1].get_xdata()[0],self.linie[2].get_xdata()[0],self.m1,self.m2)	
				self.ui.widget.canvas.ax.clear()
				self.ui.widget.canvas.ax.plot(self.dane.y,'go')
				self.ui.widget.canvas.ax.plot(self.dane.x,self.dane.gaus2(self.dane.x,self.dane.popt[0],self.dane.popt[1],self.dane.popt[2],self.dane.popt[3],self.dane.popt[4],self.dane.popt[5]),'r',label='fit', linewidth=3.0)
				self.ui.widget.canvas.ax.plot(self.dane.x,self.dane.gaus(self.dane.x,self.dane.poptL[0],self.dane.poptL[1],self.dane.poptL[2]),'r--')
				self.ui.widget.canvas.ax.plot(self.dane.x,self.dane.gaus(self.dane.x,self.dane.poptR[0],self.dane.poptR[1],self.dane.poptR[2]),'r--')
				self.ui.widget.canvas.ax.set_xlim(self.osx)

				self.ui.widget.canvas.ax.set_ylim(self.osy)
				self.ui.widget.canvas.ax.set_xlabel(u'numer kanału')
				self.ui.widget.canvas.ax.set_ylabel(u'liczba wystapien')
				self.ui.widget.canvas.draw()
				self.ui.parametryPraweTekst.setText("Par. Prawe: w {0:.2f}, sr {1:.2f}, sz {2:.2f}".format(self.dane.poptR[0],self.dane.poptR[1],self.dane.poptR[2]))
				self.ui.parametryLeweTekst.setText("Par. Lewe: w {0:.2f}, sr {1:.2f}, sz {2:.2f}".format(self.dane.poptL[0],self.dane.poptL[1],self.dane.poptL[2]))
			except RuntimeError:
				QtGui.QMessageBox.critical(self, u'Błąd dopasowania !',
			u"Nie można dopasować krzywej do podanego obszaru. Upewnij się, że zaznaczony obszar ma charakter podwójnej krzywej Gaussa.", QtGui.QMessageBox.Ok, 
			 QtGui.QMessageBox.Ok)
			
			if type(self.dane.poptL) != int:
				tekst = "                      lewy       | prawy \n wysokosc:  {0:.2f}  | {1:.2f}  \n poz. srodka: {2:.2f} | {3:.2f} \n szerokosc: {4:.2f}       | {5:.2f}".format(self.dane.poptL[0], self.dane.poptR[0],self.dane.poptL[1], self.dane.poptR[1],self.dane.poptL[2], self.dane.poptR[2] )
				QtGui.QMessageBox.information(self, 'Dopasowano ! !',
			tekst, QtGui.QMessageBox.Ok, 
			 QtGui.QMessageBox.Ok)

			self.m1=[0,0]
			self.m2=[0,0]
			self.linie = [0,0,0]
			self.licznik=0
			self.licznik2=0
			self.punkty = [0,0]
	def klikniety(self,event):

		klawisz = QtGui.QApplication.keyboardModifiers()
		if klawisz == QtCore.Qt.ControlModifier: #ctrl
			if   len(self.listaDanych) ==0:
				QtGui.QMessageBox.critical(self, u'Błąd dopasowania !',
			u"Zaznaczanie wartosci jest mozliwe dopiero po otwarciu plików. Naciśnij przycisk otwórz i wybierz pliki.", QtGui.QMessageBox.Ok, 
			 QtGui.QMessageBox.Ok)
			else:
				if event.button==1: #lpm
					if self.licznik <=2:#2
						if (type(self.linie[self.licznik]) != int) :
							self.linie[self.licznik].remove
							self.linie[self.licznik].remove()
							self.ui.widget.canvas.draw()
							
						self.linie[self.licznik]=self.ui.widget.canvas.ax.axvline(int (event.xdata), color='r', linestyle='solid')
						if self.licznik==0:
							self.ui.lewyTekst.setText( "lewy punkt: "+( str(int(self.linie[0].get_xdata()[0]))))
							
						elif self.licznik==1:
							self.ui.srodekTekst.setText(u'środkowy punkt: '+ str(int(self.linie[1].get_xdata()[0])))
							
						else:
							self.ui.prawyTekst.setText('prawy punkt: '+ str(int(self.linie[2].get_xdata()[0])))	
							
						
						if self.licznik <2 and (type(self.linie[self.licznik+1])) ==int:
							self.licznik=self.licznik+1
						
					if (self.licznik ==3 and type(self.linie[2]) != int):#2
						
						self.linie[2].remove
						self.linie[2].remove()
						self.linie[2]=self.ui.widget.canvas.ax.axvline(int (event.xdata), color='k', linestyle='solid')
						self.ui.widget.canvas.draw()
						
				elif event.button==3: #ppm
					if self.licznik2<=1:
						if (type(self.punkty[self.licznik2]) != int):
							self.punkty[self.licznik2].remove
							self.punkty[self.licznik2].remove()
							self.ui.widget.canvas.draw()
						self.punkty[self.licznik2] = plt.Circle((event.xdata,event.ydata),50,color='r')
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
			QtGui.QMessageBox.critical(self, u'Błąd eksportowania !',
			u"Aby eksportować dane do pliku krzywe muszą zostać dopasowane. Zaznacz punkty i dopasuj krzywe", QtGui.QMessageBox.Ok, 
			 QtGui.QMessageBox.Ok)
		else:
			
			plik = QtGui.QFileDialog.getSaveFileName(self, 'Dialog Title', selectedFilter='*.dat')
			if plik:
				self.dane.zapiszDane(plik)
			
	def OtworzPliki(self): 

		if type(self.dane.popt)!=int:
			self.resetujWartosci()
			self.ui.widget.canvas.ax.clear()
			
		self.pliki =[]
		self.dane = dane()
		for path in QtGui.QFileDialog.getOpenFileNames(self, 'Open File',".","(*.dat)"):
			self.pliki.append(str(path))
		if len(self.pliki)>0:
			self.ui.widget.canvas.ax.clear()
			self.dane.ustalNazwe(self.pliki,self.nrwykresu)
			for path in self.pliki:
				self.dane.wczytajDane(str(path))

			self.listaDanych.append(self.dane)

			for i  in self.listaDanych:		
				self.ui.widget.canvas.ax.plot(i.y,'o',label = i.nazwa)
				self.ui.widget.canvas.draw()
			self.ui.widget.canvas.ax.legend(loc = 'upper right')
			self.ui.widget.canvas.ax.set_xlabel(u'numer kanału')
			self.ui.widget.canvas.ax.set_ylabel(u'liczba wystapien')
			self.ui.widget.canvas.draw()
			self.linie = [0,0,0]
			self.licznik=0
			self.ui.lewyTekst.setText( "lewy punkt: ")
			self.ui.prawyTekst.setText( "prawy punkt: ")
			self.ui.srodekTekst.setText( u"środkowy punkt: ")
			self.ui.maxlewyTekst.setText("lewe max: ")
			self.ui.maxprawyTekst.setText("prawe max: ")


	def closeEvent(self, event):
		sound_file = "Windows Exclamation.wav"
		QtGui.QSound.play(sound_file)       
		odp = QtGui.QMessageBox.question(self, 'Uwaga !',
			u"Czy na pewno zamknąć?", QtGui.QMessageBox.Yes | 
			QtGui.QMessageBox.No, QtGui.QMessageBox.No)
		
		if odp == QtGui.QMessageBox.Yes:
			QtGui.QApplication.quit()
			event.accept()
			sys.exit(app.exec_())
			
			
		else:
			event.ignore()  

	def resetujWartosci(self):
		self.m1=[0,0]
		self.m2=[0,0]
		self.licznik=0
		self.licznik2=0
		self.listaDanych =[]
		self.pliki = []
		self.dane =dane()
		self.linie = [0,0,0]
		self.punkty =[0,0]
		self.ui.widget.canvas.ax.clear()
		self.ui.widget.canvas.draw()
		self.ui.lewyTekst.setText( "lewy punkt: ")
		self.ui.prawyTekst.setText( "prawy punkt: ")
		self.ui.srodekTekst.setText( u"środkowy punkt: ")
		self.ui.maxlewyTekst.setText("lewe max: ")
		self.ui.maxprawyTekst.setText("prawe max: ")
		self.ui.parametryLeweTekst.setText("Parametry Lewe:")
		self.ui.parametryPraweTekst.setText("Parametry Prawe:")		
if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    myapp = GUIForm()
    myapp.show()
    sys.exit(app.exec_())
