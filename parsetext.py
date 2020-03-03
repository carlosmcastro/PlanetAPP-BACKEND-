#encoding: utf-8

from container_constantes import ASTRO_DATA, EQUIVALENCIAS
from exoplanets import concor
import pandas as pd

data=pd.read_csv(ASTRO_DATA)
#Data from binary stellar systems have been cleaned.
data=data.drop(data.loc[data['pl_cbflag']==1].index)

#Busquedador principal.
def whopl(who_type, elec, elec_filt):
	filt_data=data.copy() #copia
	elec = [concor(i, EQUIVALENCIAS) for i in elec] #si se a cometido un error se corrige.
	elecciones = {EQUIVALENCIAS[i] : i for i in elec}
	
	if who_type=='equal':
		for i in elec_filt:
			filt_data=filt_data[filt_data[EQUIVALENCIAS[concor(i, EQUIVALENCIAS)]]==elec_filt[i]]
	else:
		for i in elec_filt:
			filt_data=filt_data[(filt_data[EQUIVALENCIAS[concor(i, EQUIVALENCIAS)]]>elec_filt[i][0]) & 
								(filt_data[EQUIVALENCIAS[concor(i, EQUIVALENCIAS)]]<elec_filt[i][1])]

	return filt_data[elecciones.keys()].drop_duplicates().rename(columns=elecciones).to_dict('list')

#Busca los planetas que cumplen la condición exacta.
#Ejemplo: whopl_equal('nombre_planeta', 'edad_estrella', edad_estrella=1.60)
def whopl_equal(*args ,**kargs):
	return whopl('equal', args, kargs)
	
#Busca los planetas que cumplen la condición dentro de un intervalo.
#Ejemplo 1: whopl_inequal('nombre_planeta', 'distancia_estrella', edad_estrella=(1,2), distancia_estrella=(2, 25))
#Ejemplo 2: whopl_inequal('nombre_planeta', 'distancia_estrella', distancia_estrella=(7000, float('inf')))
#Se debe usar float('-inf') ó float('inf') para establecer una cota superior o inferior.
def whopl_inequal(*args, **kargs):
	return whopl('inequal', args, kargs)