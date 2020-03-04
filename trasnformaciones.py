#encoding: utf-8

from container_constantes import MORGAN_KENNAN, EQUIVALENCIAS

#Convierte la codificación de la clasificación Morgan-Kennan para estrellas,
#en lenguaje común.
# coloquial_mk('sdBV')	#Subdwarf star Blue-white Main-Sequence
# coloquial_mk('K0/1 V + G (III)') #Yellow Orange Main-Sequence regular-giant
def coloquial_mk(morgank):		
	letras_Mk = [MORGAN_KENNAN['letras'][i] for i in set(morgank).intersection(MORGAN_KENNAN['letras'])]
	num_romanos = [MORGAN_KENNAN['numeros'][u] for u in ''.join([i if i in 'IV' else " " for i in morgank]).split()]
	return [morgank, " ".join(letras_Mk+num_romanos)] #[Notación_formal, En_lenguaje_común]
			

			


				