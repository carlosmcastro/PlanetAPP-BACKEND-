from container_constantes import ASTRO_DATA, EQUIVALENCIAS
from math import pi
from decimal import Decimal as D
import pandas as pd

data=pd.read_csv(ASTRO_DATA)
#Data from binary stellar systems have been cleaned.
data.drop(data[data['pl_cbflag']==1].index, inplace = True)



c = D(3/4)/D(str(pi))
d = {i: (c*(D(u)/D(v)**3), w) for i, u, v, w in [('Estrella', '1.989', '6.957', 3), ('Planeta', '1.898', '6.371', 6)]}

#gr/cm**3
def dens(t, a, b):
	f =  D(str(a))*D(str(b))**-3*d[t][0]
	return f.scaleb(d[t][1])
	
#masa planeta en jupiter.
#densidad
#radio
def mass(t, a, b):
	f = (D(str(a))*D(str(b))**3)/d[t][0]
	return f.scaleb(-d[t][1])
	
#a:masa
#b:densidad
def radio(t, a,b):
	f = (D(str(a))*d[t][0])/D(str(b))**(D(1)/D(3))
	return f.scaleb(d[t][1]//3)


	
	
	
	
	
	
	
	
	
	
	
