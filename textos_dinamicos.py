import os, pickle
import pandas as pd

data=pd.read_csv('astronomical_data.csv')
#Data from binary stellar systems have been cleaned.
data=data.drop(data.loc[data['pl_cbflag']==1].index)

#en base a los archivos en la carpeta de texto variable, actualiza los textos correspondientes.
def update():
	for t in os.listdir('textos_variables'):
		with open(f'textos_variables/{t}', 'rb') as f:
			texto_mapa = pickle.load(f)
		texto_calculos = eval(texto_mapa['constantes'])
		with open(f'textos/{t.replace("pickle", "txt")}', "w", encoding = "utf-8") as f:
			f.write(texto_mapa['titulo']+'\n')
			f.write(texto_mapa['contenido'].format(*eval(texto_mapa['variables'].format(*[f'texto_calculos[{i}]' for i, u in enumerate(texto_calculos)]))))