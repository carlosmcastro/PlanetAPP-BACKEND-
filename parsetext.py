#encoding: utf-8

from container_constantes import ASTRO_DATA
import pandas as pd

data=pd.read_csv(ASTRO_DATA)
#Data from binary stellar systems have been cleaned.
data=data.drop(data.loc[data['pl_cbflag']==1].index)

#Busca los planetas que cumplen la condición exacta.
#Ejemplo: whopl_equal(clasificacion_estrella='K2 IV')
def whopl_equal(**kargs):
	filt_data=data.copy() #copia

	equivalencia = {'clasificacion_estrella': 'st_spstr', 'instalacion_descubrimiento_planeta': 'pl_facility',
			  'lugar_descubrimiento_planeta': 'pl_locale', 'telescopio_descubrimiento_planeta': 'pl_telescope', 
			  'intrumento_descubrimiento_planeta': 'pl_instrument'}
	
	for i in kargs:
		filt_data=filt_data[filt_data[equivalencia[i]]==kargs[i]]
	
	return filt_data.pl_name.to_list()
	
#Busca los planetas que cumplen la condición dentro de un intervalo.
#Ejemplo 1: whopl_inequal(edad_estrella=(1,2), distancia_estrella=(2, 25))
#Ejemplo 2: whopl_inequal(distancia_estrella=(7000, float('inf')))
#Se debe usar float('-inf') ó float('inf') para establecer una cota superior o inferior.
def whopl_inequal(**kargs):
	filt_data = data.copy()
	
	equivalencia = {'distancia_estrella': 'st_dist', 'edad_estrella': 'st_age',
			  'numero_planetas_estrella': 'pl_pnum', 'numero_lunas_planeta': 'pl_mnum',
			  'año_descubrimiento_planeta': 'pl_disc', 'masa_planeta': 'pl_bmassj', 
			  'radio_planeta': 'pl_rade', 'densidad_planeta': 'pl_dens'}

	for i in kargs:
		filt_data=filt_data[(filt_data[equivalencia[i]]>kargs[i][0]) & (filt_data[equivalencia[i]]<kargs[i][1])]
	
	return filt_data.pl_name.to_list()
	
	
	