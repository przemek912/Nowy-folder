path = "C:\Users\Przemek\Desktop\Nowy folder\_dane\W132X2s3_01.dat"
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
from scipy import exp
from os import listdir
from os.path import isfile, join,basename
#pliki = [ f for f in listdir("/home/przemek/Pulpit/_dane/") if isfile(join("/home/przemek/Pulpit/_dane/",f)) ]
#print pliki
print path
f = open(path,'r')
print  basename(path).partition("_")[0]

data= np.loadtxt(path,skiprows=10)
x=data[:,0]
y=data[:,1]
def przygotujDane(sciezka):
	f = open(path,'r')
	data= np.loadtxt(path,skiprows=10)
	x=data[:,0]
	y=data[:,1]
	return x+y
plt.plot(x,y,'go')

#l=33
#r=117
l=1550
sr=1750
r=2000
n = len(x[range(l,r)])                          
m = sum(x[range(l,r)]*y[range(l,r)])/n                
sigma = np.sqrt(sum(y[range(l,r)]*(x[range(l,r)]-m)**2)/n)     
 
def wybierzMaxPunkt(x,y,granicaLewa,granicaPrawa):
	maxy = max(y[granicaLewa:granicaPrawa])
	indexX = granicaLewa + np.where(y[granicaLewa:granicaPrawa] == maxy)[0][0]
	return maxy,indexX
def gaus(x,a,x0,sigma):
    return a*exp(-(x-x0)**2/(2*sigma**2))
def gaus2(x,a1,x01,sigma1,a2,x02,sigma2):
 	p1=a1*exp(-(x-x01)**2/(2*sigma1**2))
	p2=a2*exp(-(x-x02)**2/(2*sigma2**2))
	#print a2
   	return (p1+p2)

print wybierzMaxPunkt(x,y,l,sr)
print wybierzMaxPunkt(x,y,sr,r)
popt,pcov = curve_fit(gaus2,x[range(l,r)],y[range(l,r)],p0=[314,1700,1,600,1800,1])# ok 
poptL,pcovL = curve_fit(gaus,x[range(l,sr)],y[range(l,sr)],p0=[314,1700,1])
poptR,pcovR = curve_fit(gaus,x[range(sr,r)],y[range(sr,r)],p0=[500,1800,1])# drugi gaus
print poptL
print poptR
plt.plot(x,gaus2(x,*popt),'r',label='fit', linewidth=3.0)
plt.plot(x,gaus(x,poptL[0],poptL[1],poptL[2]),'r--')
plt.plot(x,gaus(x,poptR[0],poptR[1],poptR[2]),'r--')

#print  popt
#print popt1
b=gaus(x,poptL[0],poptL[1],poptL[2])+gaus(x,poptR[0],poptR[1],poptR[2]) #jak sie dodaje te co zwrocily gaus2 jest dobrze, ale wtedy wychodza zle dane wyjsciowe
#plt.plot(x,b)

plt.show()


#for f1, f2 in zip(x, gaus2(x,*popt)):
	#print f1, f2

