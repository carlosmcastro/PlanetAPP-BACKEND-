#encoding: utf-8

from container_constantes import D, ASTRO_DATA, LIMITES_PL_REALISTA, MORGAN_KENNAN, EQUIVALENCIAS, TEMPERATURA_SOLAR, TYP_DATOS, CONST_DMR
import pickle

#Convierte la codificación de la clasificación Morgan-Kennan para estrellas,
#en lenguaje común.
# coloquial_mk('sdBV')	#Subdwarf star Blue-white Main-Sequence
# coloquial_mk('K0/1 V + G (III)') #Yellow Orange Main-Sequence regular-giant
def coloquial_mk(morgank):		
	letras_Mk = [MORGAN_KENNAN['letras'][i] for i in set(morgank).intersection(MORGAN_KENNAN['letras'])]
	num_romanos = [MORGAN_KENNAN['numeros'][u] for u in ''.join([i if i in 'IV' else " " for i in morgank]).split()]
	return [morgank, " ".join(letras_Mk+num_romanos)] #[Notación_formal, En_lenguaje_común]
	
#Operaciones extraídas de: https://exoplanetarchive.ipac.caltech.edu/docs/poet_calculations.html
#Calculo de luminosidad con la temperatura efectiva (Kelvin), y el radio (radios solares) de la estrella.
def lum_calc(teff, strad):
	tsun=D(TEMPERATURA_SOLAR)
	teff, strad = D(str(teff)), D(str(strad))
	return strad**2*(teff/tsun)**4 #luminosidad de estrella en Luminosidad Solar. [Type: decimal.Decimal]

#Conversion de log10(lsun) a lsun.
#Recordar que los datos de la tabla astronomica estan por defecto en log(lsun).
def lum10(lsunlog):
	return 10**D(str(lsunlog))
	
#Calculo de zona habitable.
#Limite inferior, limite superior y ancho.
def chz(stlum):
	K_lum = D(str(stlum)).sqrt()
	limite_interno = K_lum*D('0.75')	#UA
	limite_externo = K_lum*D('1.77')	#UA
	return [limite_interno, limite_externo, limite_externo-limite_interno]

#####################################################################################################
#####################################################################################################
#####################################################################################################
	
#t: 'Estrella' o 'Planeta'
		
#a:masa
#b:radio
def dens(t, a, b):
	f =  D(str(a))*D(str(b))**-3*CONST_DMR[t][0]
	return f.scaleb(CONST_DMR[t][1])	#gr/cm**3
	
#a:densidad
#b:radio
def mass(t, a, b):
	f = (D(str(a))*D(str(b))**3)/CONST_DMR[t][0]
	return f.scaleb(-CONST_DMR[t][1])	#masa en masas solares/de jupiter.
	

#a:densidad
#b:masa
def radio(t, a, b):
	f = ((D(str(b))*CONST_DMR[t][0])/D(str(a)))**(D(1)/D(3))
	return f.scaleb(CONST_DMR[t][1]//3)	#radio en radios solares/terrestres.	

#####################################################################################################
#####################################################################################################
#####################################################################################################


def interval(t, masa=[], aux_mass=[]):
	with open(LIMITES_PL_REALISTA, 'rb') as f:
		nel = pickle.load(f)
	if aux_mass:
		tmass_min = nel[t]['proporcional_masa'][0]*aux_mass
		tmass_max = nel[t]['proporcional_masa'][1]*aux_mass
		return max(nel[t]['masa'][0], tmass_min), min(nel[t]['masa'][1], tmass_max)
	if masa:
		trad_min = radio(t, nel[t]['densidad'][1], masa)
		trad_max = radio(t, nel[t]['densidad'][0], masa)
		return max(nel[t]['radio'][0], trad_min), min(nel[t]['radio'][1], trad_max)
	else:
		return nel[t]['masa']
	
		
	













	

			


				