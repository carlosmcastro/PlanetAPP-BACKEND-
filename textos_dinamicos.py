#encoding: utf-8
import os, pickle

#Directorios con los textos.
txt_static = 'textos'
txt_dinamic = 'textos_variables'

#en base a los archivos en la carpeta de texto variable, actualiza los textos correspondientes.
def update():
	import pandas as pd

	data=pd.read_csv('astronomical_data.csv')
	#Data from binary stellar systems have been cleaned.
	data=data.drop(data.loc[data['pl_cbflag']==1].index)
	txt_pickle = [i for i in os.listdir(txt_dinamic) if '.pickle' in i]

	for t in txt_pickle:
		with open(f'{txt_dinamic}/{t}', 'rb') as f:
			texto_mapa = pickle.load(f)
		texto_calculos = eval(texto_mapa['constantes'])
		with open(f'{txt_static}/{t.replace("pickle", "txt")}', "w", encoding = "utf-8") as f:
			f.write(texto_mapa['titulo']+'\n')
			f.write(texto_mapa['contenido'].format(*eval(texto_mapa['variables'].format(*[f'texto_calculos[{i}]' for i, u in enumerate(texto_calculos)]))))
			
#comprueba si los archivos estan disponibles y si no estan corruptos.
def calidad(legi, direc):
	import hashlib 
	from urllib.request import urlopen
	
	raw = "https://github.com/carlosmcastro/PlanetAPP-BACKEND-/blob/master/{}?raw=true"
	legi = f"{direc}/{legi}"
	
	with urlopen(raw.format(legi)) as response:
		hashes = pickle.loads(response.read())
		
	def escribir_(d_arch):
		with urlopen(raw.format(d_arch)) as response:
			with open(d_arch, "wb") as f:
				f.write(response.read())
				
	def hash_comp(d_arch):
		m=hashlib.md5()
		with open(d_arch, "rb") as f:
			m.update(f.read())		
		return m.hexdigest()
		
	for arch, hex_md5 in hashes.items():
		d_arch = f"{direc}/{arch}"
		if arch in os.listdir('textos'):
			if hash_comp(d_arch) != hex_md5:
				escribir_(d_arch)
		else:
			escribir_(d_arch)
	
#legitimidad de los archivos internos.
def legitimidad():
	calidad('legitimidad_textos.dat', txt_static)
	calidad('legitimidad_textos_variables.dat', txt_dinamic)