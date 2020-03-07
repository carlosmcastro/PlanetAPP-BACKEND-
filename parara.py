#encoding: utf-8

from container_constantes import ASTRO_DATA, LIMITES_PL_REALISTA, EQUIVALENCIAS as EQV, TYP_DATOS
from transformaciones import dens as densidad, mass as masa, radio, lum_calc as luminosidad
import pickle
import pandas as pd

data=pd.read_csv(ASTRO_DATA)
#Data from binary stellar systems have been cleaned.
#data.drop(data[data['pl_cbflag']==1].index, inplace = True)

#Completa los datos físicos (densidad, masa y radio) faltantes.
#Sobreescribe la base original.
def rellenar_phy_nan():
	#Creamos una copia para no alterar la tabla [data original] importada.
	data_ = data.copy()

	#estrella o planeta.
	for typ in TYP_DATOS:
		prop_phy = EQV['densidad_'+typ], EQV['masa_'+typ], EQV['radio_'+typ]
		#Datos no nulos de cada propiedad física.
		boolean_nan = (data_[prop_phy[0]].notna(), 
					   data_[prop_phy[1]].notna(), 
					   data_[prop_phy[2]].notna())

		#DataFrames booleanos con 1 dato nan y 2 datos completos.					   
		index_nan = (data_[~boolean_nan[(0+i)%3]&
						boolean_nan[(1+i)%3]&
							boolean_nan[(2+i)%3]].index 
								for i in range(3))

		# u, o, v = (Serie_indices_nan, propiedad_física_compleatar, rotacion_prop_hy)
		for u, o, v in zip(index_nan, (densidad, masa, radio), range(3)):
			for i in u:
				data_.at[i ,prop_phy[(v+0)%3]] = round(
					o(typ, data_.at[i , prop_phy[(v+1)%3]], 
						data_.at[i , prop_phy[(v+2)%3]]),6).normalize()
			#redondea a 6 digitos decimales, y normaliza, para eliminar los ceros de exceso.

	#Completamos los datos de luminosidad estelar.
	lumen, t, r =EQV['luminosidad_estrella'], EQV['temperatura_estrella'] ,EQV['radio_estrella']
	for l in data_[data_[lumen].isnull()&data_[t].notna()&data_[r].notna()].index:
		data_.at[l, lumen] = round(luminosidad(data_.at[l, t], data_.at[l, r]).log10(), 6).normalize()

	data_.to_csv(ASTRO_DATA, index=False)	#Se guarda sin indices.
	
#Busca los datos necesarios para evaluar los intervalos limitantes de masa y radio.
#La proporcional_masa, se fundamenta en el cociente minimo y maximo de cada planeta con su estrella.
def limites():
		c_st_pl = data[EQV['masa_planeta']]/ data[EQV['masa_estrella']]
		
		lim_st_pl = {'estrella': 
						{'densidad': (data[EQV['densidad_estrella']].min(), data[EQV['densidad_estrella']].max()),
						 'masa': (data[EQV['masa_estrella']].min(), data[EQV['masa_estrella']].max()),
						 'radio': (data[EQV['radio_estrella']].min(), data[EQV['radio_estrella']].max())}, 
					 'planeta':
								{'densidad': (data[EQV['densidad_planeta']].min(), data[EQV['densidad_planeta']].max()),
								 'masa': (data[EQV['masa_planeta']].min(), data[EQV['masa_planeta']].max()),
								 'proporcional_masa': (c_st_pl.min(), c_st_pl.max()),
								 'radio': (data[EQV['radio_planeta']].min(), data[EQV['radio_planeta']].max())}
								 }

		with open(LIMITES_PL_REALISTA, 'wb') as f:
			pickle.dump(lim_st_pl, f)

		

	
	
	
	
	
	
	
	
	
	
	
