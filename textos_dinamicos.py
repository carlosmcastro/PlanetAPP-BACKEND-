#encoding: utf-8

#Directorios de textos y tabla de datos astronomicos.
from container_constantes import TXT_STATIC, TXT_DINAMIC, ASTRO_DATA
import os, pickle


#en base a los archivos en la carpeta de texto variable, actualiza los textos correspondientes.
def update():
	import pandas as pd

	data=pd.read_csv(ASTRO_DATA)
	#Data from binary stellar systems have been cleaned.
	data=data.drop(data.loc[data['pl_cbflag']==1].index)
	txt_pickle = [i for i in os.listdir(TXT_DINAMIC) if '.pickle' in i]

	for t in txt_pickle:
		with open(f'{TXT_DINAMIC}/{t}', 'rb') as f:
			texto_mapa = pickle.load(f)
		texto_calculos = eval(texto_mapa['constantes'])
		with open(f'{TXT_STATIC}/{t.replace("pickle", "txt")}', "w", encoding = "utf-8") as f:
			f.write(texto_mapa['titulo']+'\n')
			f.write(texto_mapa['contenido'].format(*eval(texto_mapa['variables'].format(*[f'texto_calculos[{i}]' for i, u in enumerate(texto_calculos)]))))
			
#comprueba si los archivos estan disponibles y si no estan corruptos.
def calidad(legi, direc):
	import hashlib 
	from urllib.request import urlopen
	from urllib.error import HTTPError, URLError
	
	raw = "https://github.com/carlosmcastro/PlanetAPP-BACKEND-/blob/master/{}?raw=true"
	legi = f"{direc}/{legi}"
	
	#lectura de hashes.
	try:
		with urlopen(raw.format(legi)) as response:
			hashes = pickle.loads(response.read())
	except HTTPError as H:
		return {'Error': H}
	except URLError as U:
		return {'Error': U}
		
	def escribir_(d_arch):
		try:
			with urlopen(raw.format(d_arch)) as response:
				with open(d_arch, "wb") as f:
					f.write(response.read())
		except HTTPError as H:
			return {'Error': H}
		except URLError as U:
			return {'Error': U}
				
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
	txt_stc_error = calidad('legitimidad_textos.dat', TXT_STATIC)
	txt_din_error = calidad('legitimidad_textos_variables.dat', TXT_DINAMIC)
	
	#si alguno retorna un valor distinto de None, retorna el error.
	if txt_stc_error:
		return "Ha fallado la verificación de textos estaticos.", txt_stc_error
	if txt_din_error:
		return "Ha fallado la verificación de textos dinamicos.", txt_din_error