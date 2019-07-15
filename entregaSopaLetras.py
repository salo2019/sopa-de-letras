import PySimpleGUI as sg
from pattern.web import Wiktionary
import random
import string
import json
import sys


BOX_SIZE=25


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

def repetido(palabra,dicio):
	#palabra es un objeto
	#si "sePuede" es verdadero, la palabra se podrá agregar
	
	sePuede = True
	tipo = ''
	
	#chequea en todo el diccionario si la palabra ya se encuentra agregada
	for clave, valor in dicio.items():
		lista = []
		lista=list(map(lambda x: x.getPalabra(),dicio[clave]))
		if palabra.getPalabra() in lista:
			sePuede = False
			tipo = clave
	
	# Devuelve una tupla, donde el primer elemento ("sePuede"), si es "True", indica si se puede agregar la palabra. Caso conrario, 
	# el segundo devuelve el tipo al que pertenece la palabra que no puede ser agregada
	
	return (sePuede, tipo)

class Palabra:
	def reporte(self,p,quien):
		archivoAbrir= open("reporte.txt","r")
		datos= json.load(archivoAbrir)
		datos[quien].append(p)
		archivoAbrir.close()
		archivoGuardar= open("reporte.txt","w")
		json.dump(datos,archivoGuardar)
		archivoGuardar.close()
	def verificar(self,p):
			wiki= self.verificar_wiktionary(p)
			pattern=self.verificar_pattern(p)
			#print(wiki)
			#print(pattern)
			if (wiki[1]==True and pattern[1]==True):
				if wiki[0]!=pattern[0]:
					#print("#se genera un reporte")
					self.reporte(p,"pattern")
				#print("uso la clasificacion de Wiki",wiki[0])
				return wiki[0],wiki[2]
			elif wiki[1]==False and pattern[1]==True:
				#print("# se genera un reporte de mano de wiki")
				self.reporte(p,"wikidictionary")
				diseñoo=[
						[sg.Text("Ingrese una definición"),sg.InputText(key="definicion")],
						[sg.Text("Tipo"),sg.Radio('Sustantivo','tipo',key="sustantivo", default=True),sg.Radio('Adjetivo','tipo',key="adjetivo"),sg.Radio('Verbo','tipo',key="verbo")],
						[sg.Submit("Agregar"), sg.Submit("Cancelar")]
						]
				window=sg.Window("Definición y Tipo").Layout(diseñoo)		
				while True:
					boton,valores= window.Read()
					if boton is None:
						tipo = "sinTipo"
						valores["definicion"] = "sinDefinicion"
						break
					if boton == "Agregar":
		
						if valores["sustantivo"]:
							tipo="sustantivo"
						elif valores["adjetivo"]:
							tipo="adjetivo"
						elif valores["verbo"]:
							tipo="verbo"
						break
						
					if boton == "Cancelar":
						tipo = "sinTipo"
						valores["definicion"] = "sinDefinicion"
						break
						
				#se cierra la ventana. Si presiona "Cancelar", la ventana se cierra y los valores son iguales a None
				window.Close()
				
				return tipo,valores["definicion"]
			else:
				diseñoo=[
						[sg.Text("Ingrese una definición de ",str(p)),sg.InputText(key="definicion")],
						[sg.Text("Tipo"),sg.Radio('Sustantivo','tipo',key="sustantivo", default=True),sg.Radio('Adjetivo','tipo',key="adjetivo"),sg.Radio('Verbo','tipo',key="verbo")],
						[sg.Submit("Agregar"), sg.Submit("Cancelar")]
						]
				window=sg.Window("Definición y Tipo").Layout(diseñoo)		
				while True:
					boton,valores= window.Read()
					if boton is None:
						tipo = "sinTipo"
						valores["definicion"] = "sinDefinicion"
						break
					if boton == "Agregar":
		
						if valores["sustantivo"]:
							tipo="sustantivo"
						elif valores["adjetivo"]:
							tipo="adjetivo"
						elif valores["verbo"]:
							tipo="verbo"
						break
						
					if boton == "Cancelar":
						tipo = "sinTipo"
						valores["definicion"] = "sinDefinicion"
						break
						
				#se cierra ventana. Si presiona "Cancelar", la ventana se cierra y los valores son iguales a None
				window.Close()
				
				return tipo,valores["definicion"]			

	def verificar_wiktionary(self,palabra):
		w = Wiktionary(language="es")
		article = w.search(palabra)
		# si la palabra no la encuentra article = None
		#print(article)
		esClasificado=False
		if not article is None:
			for section in article.sections:
				if 'ustantiv' in section.title:
					cadena = 'sustantivo'
					esClasificado=True
					break #el break va para que informe solo el primero y luego salga
				elif 'djetiv' in section.title:
					cadena = 'adjetivo'
					esClasificado=True
					break #idem anterior
				elif 'erb' in section.title:
					cadena = 'verbo'
					esClasificado=True
					break #idem anterior
		else: cadena="problema_wik"		
		defini=""	
		if esClasificado:
			# ******* A CONTINUACIÓN EN EL "TRY" *******
			# a[0].content es un string que contiene el título de Etimología + un espacio en blanco + definición de la palabra
			# Convierto en lista el string anterior para filtrar, en una nueva lista, el título de Etimología + el espacio en blanco
			# La lista "lis" contendrá sólo la definición de la palabra 
			
			try:
				b = list(filter(lambda x: x.title == "Español",article.sections))			
				#print(b[0].children)
				a = list(filter(lambda x: x.title in "Etimología",b[0].children))
				#defini=a[0].content
				listaDefinicion = []
				listaDefinicion = (a[0].content).split('\n')
				li = list(filter(lambda x: x != '' and "Etimología" not in x, listaDefinicion))
				defini = '\n'.join(li)
			except IndexError:
				#Carga sólo definicion, si tiene clasificacion de wiki, pero sin el Popup, sino con una ventana
				diseñoo=[
						[sg.Text("Ingrese una definición"),sg.InputText(key="definicion")],
						[sg.Submit("Agregar"), sg.Submit("Cancelar")]
						]
				window=sg.Window("Agregar Definición").Layout(diseñoo)		
				while True:
					boton,valores= window.Read()
					if boton is None:
						valores["definicion"] = "sinDefinicion"
						break
					if boton == "Cancelar":
						valores["definicion"] = "sinDefinicion"
						break
					if boton == "Agregar":
						defini = valores["definicion"]
						break
				
				defini = valores["definicion"]
						
				#se cierra ventana. Si presiona "Cancelar", la ventana se cierra y los valores son iguales a None
				window.Close()		
		return [cadena,esClasificado,defini]
		
	def verificar_pattern(self,palabra):
		from pattern.es import tag
		tipo= tag(palabra)[0][1]
		clasificacion=True
		if tipo=="VB":
			pTipo="verbo"
		elif tipo=="NN":
			pTipo="sustantivo"
		elif tipo=="JJ":
			pTipo="adjetivo"
		else:
			clasificacion=False
			pTipo="problema_pattern"
		return [pTipo,clasificacion]
	def __init__(self,p):
		self.tipo,self.definicion= self.verificar(p)
		self.palabra=p
	
			
	def esTipo(self):
		return self.tipo
	def getPalabra(self):
		return self.palabra	
	def getDefinicion(self):
		return self.definicion	

#FIN DEL OBJETO		
# BOX_SIZE va ser el tamaño que va tener el rectangulo que se va dibujar en el grafico
BOX_SIZE=25
#//////////////////////////////////////////////////////////////////////////////////////////////
#-----Determina el color de la sopa de letras dependiendo del promedio que tenga la oficina elegida

def calcularColorSopa(promedio):
	if promedio <=15:
		return "blue"
	elif promedio>=15 and promedio <=20:
		return "orange"
	return "red"
#----Calcula el promedio de la oficina elegida	
#----Como registro es una lista con diccionarios y estos tiene como claves "temp""hum""fecha" se hace un for, de la lista, i seria el diccionario 
#----

def calcularPromedio(registro):
	promedio=0
	for i in registro:
		promedio=promedio+i["temp"]
	return promedio//len(registro)
#/////////////////fin//////////////////////
#pXtipo.items retorna una lista de tuplas donde tiene ("sustantivo",[*palabras*])... asi con adjetivo y verbo entonces i= ("sustantivo",[*palabras*])
#cant es la cantidad que ingreso el docente para que se muestre por eso se hace cXtipo[i[0]] >>>> i[0] es la clave (sustantivo , adjetivo , verbo)





		
def configurarYa():
	#calcula las oficinas a mostrar
	archivo=open("oficinas.txt","r")	
	datos=json.load(archivo)
	#genero una lista que va tener radios de las oficinas , utilizo un for ya que levantando el archivo no se cuantas oficinas tengo que poner en listaOfi entonces las creo
	listaOfi=[sg.Text("Oficina: ")]
	for i in list(datos.keys()):
		listaOfi.append(sg.Radio(i,'oficina',key=i, default=True))
	#listaOfi es una lista con los radios 

	
	palabrasXtipo={"sustantivo":[],"adjetivo":[],"verbo":[]}
	cantidadXtipo={"sustantivo":0,"adjetivo":0,"verbo":0}
	orientacion=True
	ayuda=""
	mayusMinu=True
	colores={"sustantivo":0,"adjetivo":0,"verbo":0}
	
	columna_1 =[[sg.Text('Sustantivos')],
				[sg.Multiline(do_not_clear=True, disabled=False, key='sustantivo')]
				]
	columna_2 = [[sg.Text('Adjetivos')],
				[sg.Multiline(do_not_clear=True, disabled=False, key='adjetivo')]
				]
	columna_3 = [[sg.Text('Verbos')],
				[sg.Multiline(do_not_clear=True, disabled=False, key='verbo')]
				]
			
	#Armo para la eleccion de colores
	frame_layout = [	  
					[sg.T('Color Verbos: '), sg.In(change_submits=True, size=(10,1), do_not_clear=True, key='ColVer'), sg.ColorChooserButton('Elegir', target=(sg.ThisRow, -1))],
					[sg.T('Color Adjetivos: '), sg.In(change_submits=True, size=(10,1), do_not_clear=True, key='ColAdj'), sg.ColorChooserButton('Elegir', target=(sg.ThisRow, -1))],
					[sg.T('Color Sustantivos: '), sg.In(change_submits=True, size=(10,1), do_not_clear=True, key='ColSust'), sg.ColorChooserButton('Elegir', target=(sg.ThisRow, -1))]
				]	  

	#Armo el diseño de la interface
	diseño = [  [sg.Frame('Seleccion de colores', frame_layout)],
				[sg.Text('Ingreso de palabra'), sg.InputText(key="palabra")],
				[sg.Text("",size=(60,1),key="out1",text_color="red")],
				[sg.Submit('Aceptar')],				
				[sg.Column(columna_1), sg.Column(columna_2), sg.Column(columna_3)],
				#cantidad a mostrar
				[sg.Text("Cantidad de sustantivos",size=(18,1)),sg.InputText(key="sustantivo1",size=(5,1))],
				[sg.Text("",text_color="red",key="sus",size=(20,1))],
				[sg.Text("Cantidad de adjetivos",size=(18,1)),sg.InputText(key="adjetivo1",size=(5,1))],
				[sg.Text("",text_color="red",key="adj",size=(20,1))],
				[sg.Text("Cantidad de verbos",size=(18,1)),sg.InputText(key="verbo1",size=(5,1))],
				[sg.Text("",text_color="red",key="ver",size=(20,1))],
				#fin
				[sg.Text('Orientacion: '), sg.Radio('Horizontal', 'orientacion',default=True,key="h"),  sg.Radio('Vertical', 'orientacion',key="v")],
				[sg.Text('Tipo de Ayuda: '), sg.Radio('Sin ayuda', 'ayuda',default=True,key="SA"),  sg.Radio('Ayuda mínima', 'ayuda',key="AMin"), sg.Radio('Ayuda máxima', 'ayuda',key="AM")],
				[sg.Text('¿Letras en mayúscula ó minúscula?'), sg.Radio('Letra mayúscula', 'tipo_letra',key="mayus"),  sg.Radio('Letra minúscula', 'tipo_letra',default=True,key="min")],
				 listaOfi,
				[sg.Submit('Terminar')]		
			]

	window = sg.Window('Ajustes', resizable=True).Layout(diseño)
	while True:
		boton,valores=window.Read()
		if boton is None:
			break
		if boton =="Aceptar":
			window.FindElement("out1").Update("")
			if valores["palabra"] !="":
				palabra=valores["palabra"]
				if not palabra.isalpha():
					window.FindElement("out1").Update("{} no es una palabra".format(str(palabra)))
				else:
					#en la siguiente línea, todos los caracteres son convertidos en minúsculas y se crea el objeto Palabra
					p = Palabra(palabra.lower())
					#tener en cuenta si no tiene clasificacion 
					#como uso multiline me debo fijar como agregar esta palabra
					
					#chequea si se cancelaron los ingresos manuales de tipo y definición de la palabra
					if p.getDefinicion() == "sinDefinicion":
						window.FindElement("out1").Update("El ingreso de la palabra '{}' fue cancelado".format(str(palabra)))
						
					else:
						tuplaVerificacion = repetido(p, palabrasXtipo)
						if tuplaVerificacion[0]:
							palabrasXtipo[p.esTipo()].append(p)
							window.FindElement(p.esTipo()).Update(value=str(p.getPalabra()+" "),append=True)
						else:
							window.FindElement("out1").Update("La palabra '{}' fue agregada anteriormente como {}".format(str(palabra.lower()), tuplaVerificacion[1]))	
					
			else: window.FindElement("out1").Update("Ingrese una palabra")
		if boton=="Terminar":
			if valores["sustantivo1"].isdigit():
				cantidadXtipo["sustantivo"]= int(valores["sustantivo1"])
			else:
				window.FindElement("sus").Update('<INGRESE UN NUMERO>')
			if valores["adjetivo1"].isdigit():
				cantidadXtipo["adjetivo"]= int(valores["adjetivo1"])
			else:
				window.FindElement("adj").Update('<INGRESE UN NUMERO>')	
				
			if valores["verbo1"].isdigit():
				cantidadXtipo["verbo"]= int(valores["verbo1"])
			else:
				window.FindElement("ver").Update('<INGRESE UN NUMERO>')
				continue
				
			#chequea que los colores no estén repetidos
			if valores['ColSust'] == valores['ColAdj']:
				sg.Popup('ERROR', 'Los colores para sustantivos y adjetivos deben ser distintos. Vuelva a elegirlos')
				window.FindElement("ColSust").Update('')
				window.FindElement("ColAdj").Update('')
				continue
			elif valores['ColSust'] == valores['ColVer']:
				sg.Popup('ERROR', 'Los colores para sustantivos y verbos deben ser distintos. Vuelva a elegirlos')
				window.FindElement("ColSust").Update('')
				window.FindElement("ColVer").Update('')
				continue
			elif valores['ColAdj'] == valores['ColVer']:
				sg.Popup('ERROR', 'Los colores para adjetivos y verbos deben ser distintos. Vuelva a elegirlos')
				window.FindElement("ColAdj").Update('')
				window.FindElement("ColVer").Update('')
				continue
				
			break		
	
	
	colores['sustantivo']=valores['ColSust']
	colores['adjetivo']=valores['ColAdj']
	colores['verbo']=valores['ColVer']
	
			
	if valores["h"] == True:
		orientacion=True
	elif valores["v"] == True:
		orientacion=False
	if valores["SA"] == True:
		ayuda='Sin ayuda'
	elif valores["AMin"] == True:
		ayuda='Ayuda mínima'
	elif valores["AM"] == True:
		ayuda='Ayuda máxima'
	if valores["mayus"] == True:
		mayusMinu=False
	elif valores["min"] == True:
		mayusMinu=True

	#busca la clave de la oficina 	
	for i in list(datos.keys()):
		if valores[i]==True:
			oficina=i
			break
	#oficina es la oficina que selecciono el docente		
	listaDeOficina= datos[oficina]
	#calculo el promedio de temperaturas
	promedio= calcularPromedio(listaDeOficina)
	#calculo el color que va tener la sopa
	color= calcularColorSopa(promedio)
	#print("LA OFICINA ",oficina,"tiene un color ",color)	
	window.Close()	

	
	return palabrasXtipo,cantidadXtipo,orientacion,ayuda,mayusMinu,colores,color	

#/////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
#/////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
#COMIENZA LAS FUNCIONES DEL JUEGO	
def calcularCantidad(dictio):
	cant=0
	for i in dictio:
		cant= cant+ len(dictio[i])
	return cant 


def chequearSiPisa(tipo,coordenada,dictio):
	for i in dictio:
		if i != tipo:
			if coordenada in dictio[i]:
				dictio[i].remove(coordenada)

def mostrar(matrix,nxn,grph):
	for row in range(nxn):
		for col in range(nxn):
			grph.DrawRectangle((col * BOX_SIZE , row * BOX_SIZE ), (col * BOX_SIZE + BOX_SIZE  , row * BOX_SIZE + BOX_SIZE  ), line_color='black')
			#print((col * BOX_SIZE , row * BOX_SIZE ),(col * BOX_SIZE + BOX_SIZE  , row * BOX_SIZE + BOX_SIZE  ))
			grph.DrawText(str(matrix[row][col]),(col*BOX_SIZE+18,row*BOX_SIZE+14),font='Courier 25')

def completar_matriz(mtx,n,m):
	for i in range(n):
		for e in range(n):
			if mtx[i][e] == "":
				mtx[i][e] = random.choice(string.ascii_lowercase) if m  else random.choice(string.ascii_uppercase)
	return mtx

def crear_matriz(nxn):
	matriz=[]
	for i in range(nxn):
		matriz.append([])
		for e in range(nxn):
			matriz[i].append("")
	return matriz
	
def valores_posicion(matriz,nxn,orient,pos):
	valores=[]
	espacios=0
	for i in range(nxn):
		if orient:
			if matriz[pos][i] !="":
				valores.append(espacios)
				valores.append(matriz[pos][i])
			else:
				espacios=espacios+1
		else:
			if matriz[i][pos] !="":
				valores.append(espacios)
				valores.append(matriz[i][pos])
				espacios=0
			else:
				espacios=espacios+1
	if espacios == nxn:
		valores.append(espacios)
		valores.append("0")
	return valores
	
def colocar_palabra(matrix,palabra,tipo,esfila,pos,inicio,dictio):
	lista=[]
	for x in range(inicio, inicio+len(palabra) ) :
		if esfila:
			matrix[pos][x] = palabra[x-inicio]
			lista.append((x,pos))
		else:
			matrix[x][pos] = palabra[x-inicio]
			lista.append((pos,x))		
	dictio[tipo][palabra]=lista	
	
	return matrix

def procesar_palabras(matriz,nxn,palabras,orient,dictio,m):
	posiciones=[]
	#cambiar direccion , m (AMBOS TIENEN QUE SER BOOLEANOS))
	for i in range(len(palabras)):
		posicion_inicial= random.randint(0,nxn-1)
		posicion= posicion_inicial
		#direccion= orient
		colocada=False
		while(not colocada):
			valores_en_posicion = valores_posicion(matriz, nxn,orient,posicion)
			for e in range(len(valores_en_posicion)//2):
				if((valores_en_posicion[e*2]) >= len(palabras[i].getPalabra())):
					margen= int(valores_en_posicion[e*2] - len(palabras[i].getPalabra()))
					if margen > 0:
						inicio= random.randint(0,margen)		
						matriz = colocar_palabra(matriz, palabras[i].getPalabra().lower() if m else palabras[i].getPalabra().upper(),palabras[i].esTipo(), orient, posicion, inicio, dictio)
					else:
						matriz = colocar_palabra(matriz,palabras[i].getPalabra().lower() if m else palabras[i].getPalabra().upper(),palabras[i].esTipo(), orient, posicion, margen, dictio)
					colocada=True	
					break
			if not colocada:
				if posicion < nxn-1: posicion += 1
				else: posicion = 0
	 
	return matriz


def resultado(errores,lista,orientacion,ayuda,colores,mayusMinu,diccionario,colorSop, diccioTodasPalabras, ok):
	cadena = ''
	#Linea Nueva. Esta lista es para cuando quiera volver a hacer la eleccion de palabras aleatorias. Ver linea 474	
	lnue=[]
	
	#Parte borrada, no necesaria
#	if len(errores) > 0:
#		cadena = '\n \n'.join(errores)
#	elif len(errores) == 0:
#		cadena = 'FELICITACIONES. GANASTE EL JUEGO'
	if (ok==False):
		cadena = '\n \n'.join(errores)
	if (ok==True):
		cadena = 'FELICITACIONES. GANASTE EL JUEGO' 
	
	diseño=[
		
		[sg.Text('Observaciones')],
		[sg.Multiline(cadena, size=(50,20))],
		[sg.Submit("Reiniciar Juego con las mismas palabras")],
		[sg.Submit("Reiniciar con otras palabras Manteniendo el Ajuste")],
		[sg.Submit("Volver a Ajustes")],
		[sg.Submit("No quiero jugar mas")]
		
		
		]
	
	
	window = sg.Window("grafico", resizable=True).Layout(diseño)
#	window.Finalize()
	
	while True:
		button,values=window.Read()
		if button is None:
			break
		if button == "No quiero jugar mas":
			window.Close()
			sys.exit(0)
		#permito reiniciar el juego con el mismo ajuste y las mismas palabras
		if button=="Reiniciar Juego con las mismas palabras":
			window.Close()
			juego_nuevo(lista,orientacion,ayuda,colores,mayusMinu,diccionario,colorSop, diccioTodasPalabras)
		#permito reiniciar el juego con el mismo ajuste y otras palabras aleatorias
		if button=="Reiniciar con otras palabras Manteniendo el Ajuste":
			window.Close()
			lnue = calcularCantidadIngresadas(diccionario, diccioTodasPalabras)
			juego_nuevo(lnue, orientacion, ayuda, colores, mayusMinu, diccionario, colorSop, diccioTodasPalabras)
		#permito reiniciar desde cero	
		if button=="Volver a Ajustes":
			window.Close()
			comenzar()	
	

def completarAyuda(cantLista,cantSust,cantAdj,cantVerbo,lisNue,ayuda):
	diseño= [	[sg.T('Total de palabras:'),sg.T(cantLista)],  
				[sg.T('Cantidad verbos:'), sg.T(cantVerbo)],
				[sg.T('Cantidad adjetivos:'), sg.T(cantAdj)],
				[sg.T('Cantidad sustantivos:'), sg.T(cantSust)]
			]
	if ayuda=='Ayuda máxima':
		diseño.append([sg.T('Lista de palabras: '), sg.T(lisNue)])
	elif ayuda =='Ayuda mínima':
		diseño.append([sg.Button('Definiciones')])
	return diseño


def juego_nuevo(lista,orientacion,ayuda,colores,mayusMinu,diccionario,colorSop, diccioTodasPalabras):
	encontradas = []
	
	dictioDeClicksDePalabras={"sustantivo":[],"adjetivo":[],"verbo":[]}
	
	dictioPalabrasAbuscar={"sustantivo":{},"adjetivo":{},"verbo":{}}
	maximo=0

	#diccionario de las definiciones en el cual la clave es la palabra y el valor la deficinicion.
	diccioDef={}
	for p in lista:
		cadena = ''
		cadena = p.getDefinicion()
		diccioDef[p.getPalabra()] = cadena #completo el diccionario de definiciones para la Ayuda Minima 
		if len(p.getPalabra()) > maximo:
			maximo=len(p.getPalabra())
	
	# Realizo una lista de definiciones, de manera tal de poder volcarlas a una variable de tipo string "definiciones"
	# La variable "definiciones", será enviada al multiline si el usuario elige opción "Ayuda Mínima"
	# La variable "CadenaArmada", también de tipo string, sólo se usa para darle un formato de presentación a cada definición
	# Cada definicón confeccionada con la variable "cadenaArmada" es agregada a la lista "lista_defini"
	# Una vez configurada la lista "lista_defini", se hace la conversión a string en la variable "definiciones"
		
	listaDef = []
	
	for clave, valor in diccioDef.items():
		listaDef.append(valor)
		
	definiciones = ''
	
	lista_defini = []
	
	num = 1
	for i in listaDef:
		cadenaArmada = ''
		cadenaArmada = '- - - - DEFINICIÓN  ' + str(num) + ' - - - -'
		cadenaArmada = cadenaArmada + '\n' + '\n'
		cadenaArmada = cadenaArmada + i
		cadenaArmada = cadenaArmada + '\n'
		lista_defini.append(cadenaArmada)
		num = num + 1
	
	definiciones = '\n \n'.join(lista_defini)
		
	nxn=(len(lista))+maximo
	matriz_control = crear_matriz(nxn)
	matriz=crear_matriz(nxn)
	matriz= procesar_palabras(matriz,nxn,lista,orientacion,dictioPalabrasAbuscar,mayusMinu)
	
	#Creo lista de las palabras buscadas para la "AYUDA"
	lisNue=[]
	for valor in dictioPalabrasAbuscar.values():
		for clave, valor2 in valor.items():
			lisNue.append(clave)
	#fin de tratamiento de las palabras. Se usa en "AYUDA"
	#*******MIRAR DONDE INFLUYE****
	#****DICCI= dictioPalabrasAbuscar y matriz es matriz
	#dicci=dic['dictio']
	#matriz= dic['matriz']
		
	matriz = completar_matriz(matriz, nxn, mayusMinu)
	largo= BOX_SIZE*nxn
	
	co = [ 
		[sg.ReadButton("Sustantivo",button_color=('white',colores["sustantivo"]),key="Sustantivo"),sg.ReadButton("Adjetivo",button_color=("white",colores["adjetivo"]),key="Adjetivo"),sg.ReadButton("Verbo",button_color=("white",colores["verbo"]),key="Verbo")] 
		 ]

	#Se soluciono un error que habia en la linea siguiente. El adjetivo siempre marcaba 0. Habia solo un error de nombre de diccionario en parametro 3 
	palabras=completarAyuda(len(lista),len(dictioPalabrasAbuscar["sustantivo"]),len(dictioPalabrasAbuscar["adjetivo"]),len(dictioPalabrasAbuscar["verbo"]),lisNue,ayuda)
	diseño=[
		[sg.Frame('PALABRAS A BUSCAR', palabras),(sg.Column(co))],
		[sg.Graph(canvas_size=(400,400),graph_bottom_left=(0,largo),graph_top_right=(largo,0),background_color=colorSop, key='graph',change_submits=True, drag_submits=False)],
		[sg.ReadButton("Listo")]
		]

	window = sg.Window("grafico", resizable=True).Layout(diseño)
	window.Finalize()
	grafico= window.FindElement('graph')
	mostrar(matriz,nxn,grafico)
	color_predeterminado=colorSop
	color=color_predeterminado

	#UTILIZO LA VARIABLE "QUE_SOY" PARA QUE CUANDO ESTA LA INTERFAZ DE LA SOPA NO PINTE NI HAGA NADA , UNA VEZ QUE PRESIONO LOS BOTONES "SUSTANTIVO","ADJETIVO" , "VERBO" AHI PUEDE ARRANCAR A BUSCAR
	que_soy=""
	
	#Linea Nueva. Si el OK se mantiene en TRUE sera que el juego fue ganado sin errores
	ok = True
	
	#loop
	while True:
		button,values = window.Read()
		if button is None:
			break
		mouse = values['graph']
		mouse= values['graph']
		# ESTOS 3 IF HACEN QUE CUANDO CAMBIE DE BOTON EL QUE SOY SE MODIFIQUE Y EL COLOR TAMBIEN
		if button=="Sustantivo":
			que_soy=button 
			color=colores["sustantivo"]
		if button=="Adjetivo":
			que_soy=button 
			color=colores["adjetivo"]
		if button=="Verbo":
			que_soy=button 
			color=colores["verbo"]
		if button=="Definiciones":
			nuevo=[[sg.Multiline(definiciones,size=(30,20))]]	
			w=sg.Window("Definiciones").Layout(nuevo)
			w.Read()
		if button == 'graph':
			if mouse == (None, None):
					continue
			# SI QUE_SOY ES IGUAL A "" NO PUEDE COMENZAR A JUGAR 		
			if que_soy !="":
				box_x = mouse[0]//BOX_SIZE
				box_y = mouse[1]//BOX_SIZE
				# LA FUNCION "CHEQUEARSIPISA" LO QUE HACE ES SI UNA POSICION DE LA SOPA ESTA PINTADA DE ROJO(SUSTANTIVO)Y HAGO CLICK EN LA MISMA CON EL COLOR CAMBIADO ELIMINO EN SUSTANTIVO LA COORDENADA. 
				#EJEMPLO LA POSICION (2,2) ESTA EN LA LISTA DE SUSTANTIVO Y ESTOY CON EL COLOR VERDE (VERBO) Y HAGO CLICK EN LA POSICION (2,2) LO QUE HACE CHEQUEAR ELIMINA EN LA LISTA DE SUSTANTIVO (2,2)
				#UTILIZO LA VARIBLE QUE_SOY PARA HACER USO DE LOS DICCIONARIOS 
				#QUE_SOY.LOWER() SE PUEDE CAMBIAR YA QUE PUSE EL BOTON COMO "Sustantivo" Y EN EL DICCIONARIO ESTA COMO "sustantivo" (no es de mucha importancia)
				chequearSiPisa(que_soy.lower(),(box_x,box_y),dictioDeClicksDePalabras)
				#probando
				if (box_x,box_y)in dictioDeClicksDePalabras[que_soy.lower()]:
					grafico.DrawRectangle((box_x*BOX_SIZE,box_y*BOX_SIZE),(box_x * BOX_SIZE + BOX_SIZE  , box_y * BOX_SIZE + BOX_SIZE),fill_color=color_predeterminado)
					dictioDeClicksDePalabras[que_soy.lower()].remove((box_x,box_y))
					matriz_control[box_x][box_y] = color_predeterminado
					# arregar
					grafico.DrawText(str(matriz[box_y][box_x]).lower() if mayusMinu else str(matriz[box_y][box_x]).upper(),(box_x*BOX_SIZE+18,box_y*BOX_SIZE+14),font='Courier 25')
					
				else:
					dictioDeClicksDePalabras[que_soy.lower()].append((box_x,box_y))
					grafico.DrawRectangle((box_x*BOX_SIZE,box_y*BOX_SIZE),(box_x * BOX_SIZE + BOX_SIZE  , box_y * BOX_SIZE + BOX_SIZE),fill_color=color)
					matriz_control[box_x][box_y] = color
					grafico.DrawText(str(matriz[box_y][box_x]).lower() if mayusMinu else str(matriz[box_y][box_x]).upper(),(box_x*BOX_SIZE+18,box_y*BOX_SIZE+14),font='Courier 25')
		
		
					
		if button is 'Listo':
			window.Close()
			errores = []
			no_encontradas = []
			
			for clave in dictioPalabrasAbuscar.keys():
				for nombre_palabra, elemento in dictioPalabrasAbuscar[clave].items():
					cantidad = 0
					cant_coloridos = 0
					col = ''
					t = ''
					for punto in elemento:
						if punto in dictioDeClicksDePalabras[clave]:
							cantidad = cantidad + 1
						if matriz_control[punto[0]][punto[1]] == colores[clave]:
							cant_coloridos = cant_coloridos + 1
						else:
							 col = matriz_control[punto[0]][punto[1]]
					if (cantidad == len(elemento) and cantidad == cant_coloridos):
						encontradas.append(nombre_palabra)
					if cant_coloridos == 0:
						for tipo, color_sombreado in colores.items():
							if col == color_sombreado:
								t = tipo
						if (t != ''):
							errores.append('La palabra ' + nombre_palabra + ' es ' + clave + '. Erróneamente fue sombreada como ' + t)
							#Linea Nueva, el OK se pondra en False porque el juego estuvo incompleto o mal echo
							ok=False
							#Linea nueva, por mas que le erre al tipo, la palabra fue encontrada, por lo tanto la agrego igual a la lista de encontradas
							encontradas.append(nombre_palabra)
			
			if len(encontradas) < len(lista):
				for i in lista:
					ok = False
					for j in encontradas:
						if i.getPalabra() == j:
							ok = True
					if ok == False:
						no_encontradas.append(i)
			
			if len(no_encontradas) > 0:
				#Linea Nueva, el ok se pone en FALSE dado que falton paralabras
				ok=False
				texto = 'Faltaron encontrar palabras. La lista total de palabras que debias encontrar son: '
				texto = texto + ' - '.join(lisNue)
				errores.append(texto)
			else: #Linea nueva, indica que las palabras se encontraron todas, acertando o no el tipo. Se vera si en le acerto al tipo indicado en las "Observaciones"
				texto = 'Has encontrado todas las palabras en la sopa'
				errores.append(texto)
						
			#Linea Nueva, se envia el OK al modulo resultado para la devolucion. Ok=True (Juego Ganado sin Problemas), OK=False (Juego con observaciones)
			resultado(errores,lista,orientacion,ayuda,colores,mayusMinu,diccionario,colorSop, diccioTodasPalabras, ok)
			
			#Esto lo saco dado que errores nunca va a ser 0. Porque para el caso que se encuentren todas las palabras, la funcion "errores" va a contener eso la 
#			if len(errores) == 0:
#				break
					
			
			
		
def comenzar():
	palabrasXtipo,cantidadXtipo,orientacion,ayuda,mayusMinu,colores,colorSop=configurarYa()		
	lista=calcularCantidadIngresadas(cantidadXtipo,palabrasXtipo)
	#igual que antes pero paso ademas al modulo "palabrasXtipo" (diccionario con clave "tipo" y valor "lista" de todas las palabras) para poder reiniciar las palabras manteniendo el ajuste
	juego_nuevo(lista,orientacion,ayuda,colores,mayusMinu,cantidadXtipo,colorSop, palabrasXtipo)


comenzar()
