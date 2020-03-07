#encoding: utf-8

from container_constantes import ASTRO_DATA, EQUIVALENCIAS, TYP_DATOS
from transformaciones import dens as densidad, mass as masa, radio, lum_calc as luminosidad
#from math import pi
#from decimal import Decimal as D
import pandas as pd

data=pd.read_csv(ASTRO_DATA)
#Data from binary stellar systems have been cleaned.
#data.drop(data[data['pl_cbflag']==1].index, inplace = True)

#Completa los datos físicos (densidad, masa y radio) faltantes.
#Sobreescribe la base original.
def rellenar_phy_nan():
	#estrella o planeta.
	for typ in TYP_DATOS:
		prop_phy = EQUIVALENCIAS['densidad_'+typ], EQUIVALENCIAS['masa_'+typ], EQUIVALENCIAS['radio_'+typ]
		#Datos no nulos de cada propiedad física.
		boolean_nan = (data[prop_phy[0]].notna(), 
					   data[prop_phy[1]].notna(), 
					   data[prop_phy[2]].notna())

		#DataFrames booleanos con 1 dato nan y 2 datos completos.					   
		index_nan = (data[~boolean_nan[(0+i)%3]&
						boolean_nan[(1+i)%3]&
							boolean_nan[(2+i)%3]].index 
								for i in range(3))

		# u, o, v = (Serie_indices_nan, propiedad_física_compleatar, rotacion_prop_hy)
		for u, o, v in zip(index_nan, (densidad, masa, radio), range(3)):
			for i in u:
				data.at[i ,prop_phy[(v+0)%3]] = round(
					o(typ, data.at[i , prop_phy[(v+1)%3]], 
						data.at[i , prop_phy[(v+2)%3]]),6).normalize()
			#redondea a 6 digitos decimales, y normaliza, para eliminar los ceros de exceso.

	#Completamos los datos de luminosidad estelar.
	lumen, t, r =EQUIVALENCIAS['luminosidad_estrella'], EQUIVALENCIAS['temperatura_estrella'] ,EQUIVALENCIAS['radio_estrella']
	for l in data[data[lumen].isnull()&data[t].notna()&data[r].notna()].index:
		data.at[l, lumen] = round(luminosidad(data.at[l, t], data.at[l, r]).log10(), 6).normalize()

	data.to_csv(ASTRO_DATA, index=False)	#Se guarda sin indices.
	
	



	
	
	
	
	
	
	
	
	
	
	
