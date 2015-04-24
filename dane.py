import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
from scipy import exp
from os import listdir
from os.path import isfile, join


class dane(object):

	
	sciezka=''
	x=0
	y=0
	lewy=0
	srodkowy=0
	prawy=0
	max1=0
	max2=0
	popt=0
	pcov=0
	popt=0
	poptR=0
	poptL=0
	#fig, ax = plt.subplots(1, 1)
	obraz = plt.figure()
	
	def wczytajDane(self,sciezka):
		self.sciezka = sciezka
		f = open(sciezka,'r')
		data= np.loadtxt(sciezka,skiprows=10)
		x=data[:,0]
		y=data[:,1]
		self.x =x
		self.y=self.y+y
	
	def __init__(self):
		pass

	def pojedynczyPlik(sciezka):
		self.sciezka = sciezka
		self.wczytajDane(self.sciezka)

	def gaus(self,x,a,x0,sigma):
		return a*exp(-(x-x0)**2/(2*sigma**2))
		
	def gaus2(self,x,a1,x01,sigma1,a2,x02,sigma2):
		p1=a1*exp(-(x-x01)**2/(2*sigma1**2))
		p2=a2*exp(-(x-x02)**2/(2*sigma2**2))
		return p1+ p2
	
	def dopasuj(self,l,s,p,m1,m2):
		self.lewy=l
		self.srodkowy=s
		self.prawy=p
		self.max1=m1
		self.max2=m2
		#a=self.gaus([1,2,3, 4, 5],30,4,1)
		#print a
		#print self.x,self.y[2000],self.lewy,self.prawy
		self.popt,cov1 = curve_fit(self.gaus2,self.x[range(self.lewy,self.prawy)],self.y[range(self.lewy,self.prawy)],p0=[314,1700,1,600,1800,1])# ok ale trzeba jeszcze brac x i y z kliknietego maxa
		self.poptL,cov2 = curve_fit(self.gaus,self.x[range(self.lewy,self.srodkowy)],self.y[range(self.lewy,self.srodkowy)],p0=[314,1700,1])
		self.poptR,cov3 = curve_fit(self.gaus,self.x[range(self.srodkowy,self.prawy)],self.y[range(self.srodkowy,self.prawy)],p0=[500,1800,1])# drugi gaus
		#print poptL
		#print poptR
		#plt.plot(self.x,self.gaus2(self.x,*popt),'ro',label='fit')
		#plt.plot(self.x,self.gaus(self.x,poptL[0],poptL[1],poptL[2]),'r--')
		#plt.plot(self.x,self.gaus(self.x,poptR[0],poptR[1],poptR[2]),'r--')
		#return popt,poptL,poptR


