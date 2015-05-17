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
	obraz = plt.figure()
	
	def wczytajDane(self,sciezka):
		self.sciezka = sciezka
		f = open(sciezka,'r')
		data= np.loadtxt(sciezka,skiprows=10)
		x=data[:,0]
		y=data[:,1]
		self.x =x
		self.y=self.y+y
		
	def zapiszDane(self,sciezka):
		with open(sciezka, 'w') as f:
			for f1, f2 in zip(self.x, self.gaus2(self.x,*self.popt)):
				print >> f, f1, f2
	
	def __init__(self):
		self.x=0
		self.y=0
		self.popt=0
		self.pcov=0
		self.popt=0
		self.poptR=0
		self.poptL=0

	def pojedynczyPlik(sciezka):
		self.sciezka = sciezka
		self.wczytajDane(self.sciezka)

	def gaus(self,x,a,x0,sigma):
		return a*exp(-(x-x0)**2/(2*sigma**2))
		
	def gaus2(self,x,a1,x01,sigma1,a2,x02,sigma2):
		p1=a1*exp(-(x-x01)**2/(2*sigma1**2))
		p2=a2*exp(-(x-x02)**2/(2*sigma2**2))
		return (p1+ p2)
	
	def dopasuj(self,l,s,p,m1,m2):
		self.popt,self.pcov = curve_fit(self.gaus2,self.x[range(l,p)],self.y[range(l,p)],p0=[m1[1],m1[0],1,m2[1],m2[0],1])
		self.poptL,cov2 = curve_fit(self.gaus,self.x[range(l,s)],self.y[range(l,s)],p0=[m1[1],m1[0],1])
		self.poptR,cov3 = curve_fit(self.gaus,self.x[range(s,p)],self.y[range(s,p)],p0=[(m2[1],m2[0],1)])



