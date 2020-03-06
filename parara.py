#encoding: utf-8

from container_constantes import D, ASTRO_DATA, CONST_DMR
#from math import pi
#from decimal import Decimal as D
import pandas as pd

data=pd.read_csv(ASTRO_DATA)
#Data from binary stellar systems have been cleaned.
data.drop(data[data['pl_cbflag']==1].index, inplace = True)

#t: 'Estrella' o 'Planeta'
		
#a:masa
#b:radio
def dens(t, a, b):
	f =  D(str(a))*D(str(b))**-3*CONST_DMR[t][0]
	return f.scaleb(CONST_DMR[t][1])	#gr/cm**3
	
#a:densidad
#b:radio
def mass(t, a, b):
	f = (D(str(a))*D(str(b))**3)/CONST_DMR[t][0]
	return f.scaleb(-CONST_DMR[t][1])	#masa en masas solares/de jupiter.
	

#a:densidad
#b:masa
def radio(t, a, b):
	f = ((D(str(b))*CONST_DMR[t][0])/D(str(a)))**(D(1)/D(3))
	return f.scaleb(CONST_DMR[t][1]//3)	#radio en radios solares/terrestres.


	
	
	
	
	
	
	
	
	
	
	
