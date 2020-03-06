from container_constantes import ASTRO_DATA, EQUIVALENCIAS
import pandas as pd
from math import pi
from decimal import Decimal as D

data=pd.read_csv(ASTRO_DATA)
#Data from binary stellar systems have been cleaned.
data.drop(data[data['pl_cbflag']==1].index, inplace = True)

#masas de jupiter
data['pl_bmassj'].min()
data['pl_bmassj'].max()

#masas solares
data['st_mass'].min()
data['st_mass'].max()

#gr/cm**3
data['pl_dens'].min()
data['pl_dens'].max()

data['st_dens'].min()
data['st_dens'].max()


sunmass=1.989*10**30 #Solar mass in kg
sunrad = 6.957*10**8 #metros
#3*8 => 24
#10**6 /por/ 30-24
def dens(a, b):
	d = 1.989/6.957**3
	g = 10**6 #kg/m**3
	h = 10**3	#gr/cm**3
	c = (3/4)*(1/pi)
	f =  a*c*d*b**-3
	return [f*g, f*h]
	
def den(a, b):
	d = D('1.989')/D('6.957')**3
	g = D(10)**6 #kg/m**3
	h = D(10)**3	#gr/cm**3
	c = D(3/4)*D(1)/D(str(pi))
	f =  D(str(a))*c*d*D(str(b))**-3
	return [f*g, f*h]
	
junmass =1.898 * 10**27 #kg
ter_rad = 6.371 * 10**6 #metros
def dens_pl(a, b):
	d = 1.898/6.371**3
	g = 10**9 #kg/m**3
	h = 10**6	#gr/cm**3
	c = (3/4)*(1/pi)
	f =  a*c*d*b**-3
	return [f*g, f*h]
	
#masa estrella en masas solares.
def mass(a, b):
	c = (4/3)*pi
	d = 6.957**3/1.989  
	g=10**-3
	f = a*c*d*g*b**3
	return f
	
def mass_pl(a, b):
	c = (4/3)*pi
	d = 6.371**3/1.898
	g = 10**-6
	f = a*c*d*g*b**3
	return f
	

	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	