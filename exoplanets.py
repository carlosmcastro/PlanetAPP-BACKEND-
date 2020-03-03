#encoding: utf-8
#!/usr/bin/env python
#Más información: https://exoplanetarchive.ipac.caltech.edu/docs/program_interfaces.html
#Uso de la API NASA Exoplanet Archive; para optimizar la visualización de datos para Planetas Confirmados.
#No incluye el filtrado de fechas, ni el uso de comodines.

#Uso: exoplanets.get(tabla_de_datos, tupla_de_numeros_de_columnas, columna1,...,columnaN)
#Ejemplo: exoplanets.get('exoplanets', (0,1), ['pl_hostname', 'pl_letter'], ['pl_name', 'pl_mnum'])

#Renueva la elección de datos. Genera un archivo serializado para proximas actualizaciones.
#Uso: exoplanets.update([tabla_de_datos, tupla_de_numeros_de_columnas, columna1,...,columnaN])
#Ejemplo: exoplanets.update(['exoplanets', (0,1), ['pl_hostname', 'pl_letter'], ['pl_name', 'pl_mnum']])

#Uso: exoplanets.update() #Actualiza la base de datos basandose en el archivo serializado.

#El script tiene un corrector de errores, que aproxima al nombre de la tabla y las columnas para buscar.
#Es menos aproximado para los datos corregidos, cuando la palabra incorrecta es corta, como poner "dic" en lugar de "dec".

#Solo se puede acceder a un conjunto de datos por conjunto de columnas, esto sucede intencionalmente, para forzar la búsqueda de datos precisos.

#El script devuelve un diccionario con datos Json.

#Link de la api con los datos de exoplanetas, tabla de datos astronomicos, archivo pickle con los valores a descargar.
from container_constantes import API_EXOPLANETAS, TABLAS_EXOPLANETAS, ASTRO_DATA, TABLAS_REF
from urllib.request import urlopen
from urllib.error import HTTPError, URLError
import pickle, json

#Verifica los datos de busqueda reales, más cercanos.
def concor(nombre, nombres_t):
	if nombre in nombres_t:
		return nombre

	#nombre con mayor cantidad de caracteres en comun.
	co_nombre = set(nombre)
	similar = [(len(co_nombre&set(i)) ,i) for i in nombres_t]
	maximos = max(similar, key=lambda x: x[0])
	
	#Se filtran los valores maximos.
	primer_sel = [*filter(lambda x: x[0]==maximos[0], similar)]
	
	#Si no es único, compara si por cada caracter en comun posee la misma cantidad de coincidencias.
	if len(primer_sel)-1:
		sumada = [sum([1 for i in co_nombre if v.count(i) == nombre.count(i)]) for u, v in primer_sel]
		segunda_sel = primer_sel[sumada.index(max(sumada))][1]
	else:
		segunda_sel = maximos[1]
	return segunda_sel

	
#Para evitar la costosa importación de pandas para unicamente una conversión.
def json_csv(json_arch):
	with open(ASTRO_DATA, "w") as f:
		#Encabezado.
		f.write(",".join(json_arch[0].keys())+"\n")
		#Datos linea a linea.
		for i in json_arch:
			aux_str = lambda x: str(x) if x!=None else "" #Para imprimir datos vacíos.
			f.write(",".join(map(aux_str, i.values()))+"\n")

		
#Llamada a la API
def get(tabla, num, *args):
	tabla=concor(tabla, TABLAS_EXOPLANETAS)

#Comprueba las columnas.
	columna = [concor(dato, TABLAS_EXOPLANETAS[tabla][indice])
					for indice, col in zip(num, args)
						for dato in col]

#Descarga los datos o informa un error.
	try:
		with urlopen(API_EXOPLANETAS+'table='+tabla+'&select='+",".join(columna)+'&order=dec&format=json') as response:
			if response.status == 200:
				return json.loads(response.read()) #Datos en formato JSON.
			else:
				return [{'Error': response.status}]
	except HTTPError as H:
		return [{'Error': H}]
	except URLError as U:
		return [{'Error': U}]


#datexo es una Lista
#Sevicio de actualización de base de datos.		
def update(datexo=None):
	#deserializa la lista con pickle por defecto si existe. En caso contrario lo serializa.
	if datexo:
		with open(TABLAS_REF, 'wb') as file_reference_data:
			pickle.dump(datexo, file_reference_data)
	else:
		with open(TABLAS_REF, 'rb') as file_reference_data:
			datexo=pickle.load(file_reference_data)
	
	#descarga los datos exigidos.
	json_data=get(datexo[0], datexo[1], *datexo[2:])
	json_csv(json_data)