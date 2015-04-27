import sys
from maingui import *
from dane import *
import random
from matplotlib.backend_bases import *
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
from scipy import exp
from os import listdir
from os.path import isfile, join
from PyQt4 import QtGui,QtCore
from matplotlib.backends.backend_qt4agg import NavigationToolbar2QT as NavigationToolbar2

class GUIForm(QtGui.QMainWindow):
	lewy=0
	srodek=0
	prawy = 0
	m1=0
	m2=0
	licznik=0
	pliki = []
	dane =dane()
	linie = [0,0,0]
	def __init__(self, parent=None):

		QtGui.QWidget.__init__(self,parent)
		self.ui = Ui_MainWindow()
		self.ui.setupUi(self)
		self.ui.widget.canvas.mpl_connect('button_press_event',self.klikniety)
		QtCore.QObject.connect(self.ui.pushButton, QtCore.SIGNAL('clicked()'),lambda: self.PlotFunc(d))
		QtCore.QObject.connect(self.ui.pushButton1, QtCore.SIGNAL('clicked()'),lambda: self.OtworzPliki())
		
		self.ui.lewyTekst.mousePressEvent = self.lewyTekstonClick
		self.ui.srodekTekst.mousePressEvent = self.srodekTekstonClick
		self.ui.prawyTekst.mousePressEvent = self.prawyTekstonClick
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
		
	def PlotFunc(self,a):
		#a = dane("C:\Users\Przemek\Desktop\Nowy folder\_dane\W132X2s3_01.dat",1550,1750,2000,314,500)
		a.dopasuj()	
		#randomNumbers = random.sample(range(0, 10), 10)
		self.ui.widget.canvas.ax.clear()
		self.ui.widget.canvas.ax.plot(a.y,'go')
		self.ui.widget.canvas.ax.plot(a.x,a.gaus2(a.x,a.popt[0],a.popt[1],a.popt[2],a.popt[3],a.popt[4],a.popt[5]),'r',label='fit', linewidth=3.0)
		self.ui.widget.canvas.ax.plot(a.x,a.gaus(a.x,a.poptL[0],a.poptL[1],a.poptL[2]),'r--')
		self.ui.widget.canvas.ax.plot(a.x,a.gaus(a.x,a.poptR[0],a.poptR[1],a.poptR[2]),'r--')
		self.ui.widget.canvas.draw()
    
	def klikniety(self,event):
		#GUIForm.licznik=GUIForm.licznik+1
		klawisz = QtGui.QApplication.keyboardModifiers()
		if klawisz == QtCore.Qt.ControlModifier: #ctrl
			if event.button==1: #lpm
				if self.licznik <=2:#2
					if (type(self.linie[self.licznik]) != int) :
						self.linie[self.licznik].remove
						self.linie[self.licznik].remove()
						self.ui.widget.canvas.draw()
						
					self.linie[self.licznik]=self.ui.widget.canvas.ax.axvline(event.xdata, color='r', linestyle='solid')#pionowa kreska na wykresie
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
					self.linie[2]=self.ui.widget.canvas.ax.axvline(event.xdata, color='k', linestyle='solid')
					self.ui.widget.canvas.draw()
					print self.licznik
					
			elif event.button==3: #ppm
				circle1= plt.Circle((event.xdata,event.ydata),.1,color='r')
				fig = self.ui.widget.canvas.ax.add_artist(circle1)
				#kropka - do wierzcholkow
		self.ui.widget.canvas.draw()
	def OtworzPliki(self):
		self.pliki =[]
		self.dane = dane()
		for path in QtGui.QFileDialog.getOpenFileNames(self, 'Open File',".","(*.dat)"):
			self.pliki.append(str(path))

		for path in self.pliki:
			self.dane.wczytajDane(str(path))
			
		self.ui.widget.canvas.ax.clear()
		self.ui.widget.canvas.ax.plot(self.dane.y,'go')	
		self.ui.widget.canvas.draw()
		self.linie = [0,0,0]
		self.licznik=0
		self.ui.lewyTekst.setText( "lewy punkt: ")
		self.ui.prawyTekst.setText( "prawy punkt: ")
		self.ui.srodekTekst.setText( "srodkowy punkt: ")

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
