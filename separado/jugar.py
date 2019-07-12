import palabras as pal
import configuracion as confg
import jugarSopa as sopa
def calcularCantidadIngresadas(cXtipo,pXtipo):
	#lo que hace es hace un for de las palabrasXtipo,como la clave es "sustantivo" "adjetivo", "verbo" puedo acceder a la cantidadXtipo  con eso saco "cant" 
	# en linea if cant > si es mayor lo pedido y no tengo esa cantidad agarro todos los que tengo
	#si es menor elijo uno al azar pregunto si no esta en la lista lo agrego
	import random
	lista=[]
	for i in list(pXtipo.items()):
		cant= cXtipo[i[0]]
		if cant >= len(i[1]):
			for j in i[1]:
				lista.append(j)
		elif cant< len(i[1]):
			l=i[1]
			n=0
			while n< cant:
				palabra= random.choice(l)
				if not palabra in lista:
					lista.append(palabra)
					n=n+1		
	return lista	
def comenzar():
	palabrasXtipo,cantidadXtipo,orientacion,ayuda,mayusMinu,colores,colorSop=confg.configurarYa()		
	lista=calcularCantidadIngresadas(cantidadXtipo,palabrasXtipo)
	#igual que antes pero paso ademas al modulo "palabrasXtipo" (diccionario con clave "tipo" y valor "lista" de todas las palabras) para poder reiniciar las palabras manteniendo el ajuste
	sopa.juego_nuevo(lista,orientacion,ayuda,colores,mayusMinu,cantidadXtipo,colorSop, palabrasXtipo)


comenzar()
