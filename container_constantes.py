#encoding: utf-8
#Constantes de las variables.

API_EXOPLANETAS="https://exoplanetarchive.ipac.caltech.edu/cgi-bin/nstedAPI/nph-nstedAPI?" #Parametro obligatorio.
ASTRO_DATA = "astronomical_data.csv"
TABLAS_REF = "data.pickle"

TXT_STATIC = 'textos'
TXT_DINAMIC = 'textos_variables'

EQUIVALENCIAS = {'clasificacion_estrella': 'st_spstr', 'instalacion_descubrimiento_planeta': 'pl_facility',
		  'lugar_descubrimiento_planeta': 'pl_locale', 'telescopio_descubrimiento_planeta': 'pl_telescope', 
		  'intrumento_descubrimiento_planeta': 'pl_instrument', 'distancia_estrella': 'st_dist', 
		  'edad_estrella': 'st_age', 'numero_planetas_estrella': 'pl_pnum', 
		  'numero_lunas_planeta': 'pl_mnum', 'año_descubrimiento_planeta': 'pl_disc',
		  'masa_planeta': 'pl_bmassj', 'radio_planeta': 'pl_rade', 
		  'densidad_planeta': 'pl_dens', 'nombre_planeta': 'pl_name',
		  'nombre_estrella': 'pl_hostname'}