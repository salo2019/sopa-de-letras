###### SEGUIR EN CONFIGURARYA######
#COMIENZA LA CREACION DEL OBJETO

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
	lista=list(map(lambda x: x.getPalabra(),dicio[palabra.esTipo()]))
	if palabra.getPalabra() in lista:
		return False
	else: return True

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
						[sg.Text("Ingrese una Definicion "),sg.InputText(key="definicion")],
						[sg.Text("Tipo"),sg.Radio('Sustantivo','tipo',key="sustantivo"),sg.Radio('Adjetivo','tipo',key="adjetivo"),sg.Radio('Verbo','tipo',key="verbo")],
						[sg.Submit("Agregar")]
						]
				window=sg.Window("Definicion").Layout(diseñoo)		
				while True:
					boton,valores= window.Read()
					if boton is None:
						break
					if boton == "Agregar":
		
						if valores["sustantivo"]:
							tipo="sustantivo"
						elif valores["adjetivo"]:
							tipo="adjetivo"
						elif valores["verbo"]:
							tipo="verbo"	
						break
				
				
				return tipo,valores["definicion"]
			else:
				diseñoo=[
						[sg.Text("Ingrese una Definicion de ",str(p)),sg.InputText(key="definicion")],
						[sg.Text("Tipo"),sg.Radio('Sustantivo','tipo',key="sustantivo"),sg.Radio('Adjetivo','tipo',key="adjetivo"),sg.Radio('Verbo','tipo',key="verbo")],
						[sg.Submit("Agregar")]
						]
				window=sg.Window("Definicion").Layout(diseñoo)		
				while True:
					boton,valores= window.Read()
					if boton is None:
						break
					if boton == "Agregar":
		
						if valores["sustantivo"]:
							tipo="sustantivo"
						elif valores["adjetivo"]:
							tipo="adjetivo"
						elif valores["verbo"]:
							tipo="verbo"	
						break
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
			try:
				b = list(filter(lambda x: x.title == "Español",article.sections))			
				#print(b[0].children)
				a = list(filter(lambda x: x.title in "Etimología",b[0].children))
				defini=a[0].content
			except IndexError:
				defini = sg.PopupGetText('Ingrese definicion:', 'No existe definicion de la palabra')
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
				[sg.Text("",size=(30,1),key="out1",text_color="red")],
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
					p= Palabra(palabra)
					#tener en cuenta si no tiene clasificacion 
					#como uso multiline me debo fijar como agregar esta palabra
					if repetido(p,palabrasXtipo):
						palabrasXtipo[p.esTipo()].append(p)
						window.FindElement(p.esTipo()).Update(value=str(p.getPalabra()+" "),append=True)
					else:
						window.FindElement("out1").Update("{} ya esta en la lista de {}".format(str(palabra),str(p.esTipo())))	
					
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
				if m == 'Minúscula':
					mtx[i][e] = random.choice(string.ascii_lowercase)
				else:
					if m == 'Mayúscula':
						mtx[i][e] = random.choice(string.ascii_uppercase)
				
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
	print ('cacho',dictio)	
	diccionario_resultado = {}
	diccionario_resultado['matriz'] = matrix
	diccionario_resultado['dictio'] = dictio
	return diccionario_resultado

def procesar_palabras(matriz,nxn,palabras,orient,dictio,m):
	posiciones=[]
	for i in range(len(palabras)):
		posicion_inicial= random.randint(0,nxn-1)
		posicion= posicion_inicial
		direccion=orient
		colocada=False
		while(not colocada):
			valores_en_posicion = valores_posicion(matriz, nxn,direccion,posicion)
			for e in range(len(valores_en_posicion)//2):
				if((valores_en_posicion[e*2]) >= len(palabras[i].getPalabra())):
					margen= int(valores_en_posicion[e*2] - len(palabras[i].getPalabra()))
					if margen > 0:
						inicio= random.randint(0,margen)
						if m == 'Minúscula':
							dic = colocar_palabra(matriz, palabras[i].getPalabra().lower(),palabras[i].esTipo(), direccion, posicion, inicio, dictio)
						if m == 'Mayúscula':
							dic = colocar_palabra(matriz, palabras[i].getPalabra().upper(),palabras[i].esTipo(), direccion, posicion, inicio, dictio)
					else:
						if m == 'Minúscula':
							dic = colocar_palabra(matriz, palabras[i].getPalabra().lower(),palabras[i].esTipo(), direccion, posicion, margen, dictio)
						if m == 'Mayúscula':
							dic = colocar_palabra(matriz, palabras[i].getPalabra().upper(),palabras[i].esTipo(), direccion, posicion, margen, dictio)
					colocada=True	
					break
			if not colocada:
				if posicion < nxn-1: posicion += 1
				else: posicion = 0
	 
	return dic					


def resultado(ori, ayuda, m, errores):
	cadena = ''
	if len(errores) > 0:
		cadena = '\n \n'.join(errores)
	elif len(errores) == 0:
		cadena = 'FELICITACIONES. GANASTE EL JUEGO'
	
	
	diseño=[
		
		[sg.Text('Observaciones')],
		[sg.Multiline(cadena, size=(50,20))],
		[sg.Text('La orientacion es:'), sg.Text(ori)],
		[sg.Text('Tipo de ayuda:'), sg.Text(ayuda)],
		[sg.Text('Letras en:'), sg.Text(m)],
		[sg.Submit("Volver")]
		
		]
	
	
	window = sg.Window("grafico", resizable=True).Layout(diseño)
	window.Finalize()
	button,values=window.Read()
	window.Close()
	
	






def juego_nuevo(lista,orientacion,ayuda,colores,mayusMinu,diccionario,colorSop):
	encontradas = []
	if orientacion == True:
		ori = 'Horizontal'
	else:
		ori = 'Vertical'
	if mayusMinu == True:
		m = 'Minúscula'
	else:
		m = 'Mayúscula'
	
	dictioDeClicksDePalabras={"sustantivo":[],"adjetivo":[],"verbo":[]}
	dictioPalabrasAbuscar={"sustantivo":{},"adjetivo":{},"verbo":{}}
	maximo=0

	#diccionario de las definiciones
	diccioDef={}
	for p in lista:
		diccioDef[p.getPalabra()]=p.getDefinicion() #completo el diccionario de definiciones para la Ayuda Minima 
		if len(p.getPalabra()) > maximo:
			maximo=len(p.getPalabra())
		
	nxn=(len(lista))+maximo
	matriz_control = crear_matriz(nxn)
	matriz=crear_matriz(nxn)
	dic= procesar_palabras(matriz,nxn,lista,orientacion,dictioPalabrasAbuscar,m)
	
	#Creo lista de las palabras buscadas para la "AYUDA"
	lisNue=[]
	for valor in dictioPalabrasAbuscar.values():
		for clave, valor2 in valor.items():
			lisNue.append(clave)
	#fin de tratamiento de las palabras. Se usa en "AYUDA"
	
	dicci=dic['dictio']
	matriz= dic['matriz']
	
	## despues es todo lo mismo que hice en el archivo sopaEnd.py		
	matriz = completar_matriz(matriz, nxn, m)
	largo= BOX_SIZE*nxn
	
	co = [
	          [sg.Text('La orientacion es:'), sg.Text(ori)],
		      [sg.Text('Tipo de ayuda:'), sg.Text(ayuda)],
		      [sg.Text('Letras en:'), sg.Text(m)],
		      [sg.Text(' ')],
		      [sg.ReadButton("Sustantivo",button_color=('white',colores["sustantivo"]),key="Sustantivo"),sg.ReadButton("Adjetivo",button_color=("white",colores["adjetivo"]),key="Adjetivo"),sg.ReadButton("Verbo",button_color=("white",colores["verbo"]),key="Verbo")]   
	    
	          ]
	
	
	if ayuda=='Ayuda máxima':
		palabras = [	[sg.T('Total de palabras:'),sg.T(len(lista))],  
						[sg.T('Cantidad verbos:'), sg.T(diccionario['verbo'])],
						[sg.T('Cantidad adjetivos:'), sg.T(diccionario['adjetivo'])],
						[sg.T('Cantidad sustantivos:'), sg.T(diccionario['sustantivo'])],
						[sg.T('Lista de palabras: '), sg.T(lisNue)]
					]
	elif ayuda=='Ayuda mínima':
		palabras = [	[sg.T('Total de palabras:'),sg.T(len(lista))],  
						[sg.T('Cantidad verbos:'), sg.T(diccionario['verbo'])],
						[sg.T('Cantidad adjetivos:'), sg.T(diccionario['adjetivo'])],
						[sg.T('Cantidad sustantivos:'), sg.T(diccionario['sustantivo'])],
						[sg.T('Definiciones de las palabras')],
						[sg.Multiline(diccioDef.values())]
					]
	elif ayuda=='Sin ayuda':
		palabras = [	[sg.T('Total de palabras:'),sg.T(len(lista))],  
						[sg.T('Cantidad verbos:'), sg.T(diccionario['verbo'])],
						[sg.T('Cantidad adjetivos:'), sg.T(diccionario['adjetivo'])],
						[sg.T('Cantidad sustantivos:'), sg.T(diccionario['sustantivo'])],
					]
	diseño=[
		[sg.Frame('PALABRAS A BUSCAR', palabras),(sg.Column(co))],
		[sg.Graph(canvas_size=(400,400),graph_bottom_left=(0,largo),graph_top_right=(largo,0),background_color=colorSop, key='graph',change_submits=True, drag_submits=False)],
        [sg.ReadButton("Listo"), sg.ReadButton("Terminar")]
		]

	window = sg.Window("grafico", resizable=True).Layout(diseño)
	window.Finalize()
	grafico= window.FindElement('graph')
	mostrar(matriz,nxn,grafico)
	color_predeterminado=colorSop
	color=color_predeterminado
	#hasta aca revise

	#UTILIZO LA VARIABLE "QUE_SOY" PARA QUE CUANDO ESTA LA INTERFAZ DE LA SOPA NO PINTE NI HAGA NADA , UNA VEZ QUE PRESIONO LOS BOTONES "SUSTANTIVO","ADJETIVO" , "VERBO" AHI PUEDE ARRANCAR A BUSCAR
	que_soy=""

	#loop
	while True:
		
		button, values = window.Read()
		if button is None:
			break
		if button is "Terminar":
			sys.exit(69)
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
				if (box_x,box_y)in dictioDeClicksDePalabras[que_soy.lower()]:
					grafico.DrawRectangle((box_x*BOX_SIZE,box_y*BOX_SIZE),(box_x * BOX_SIZE + BOX_SIZE  , box_y * BOX_SIZE + BOX_SIZE),fill_color=color_predeterminado)
					dictioDeClicksDePalabras[que_soy.lower()].remove((box_x,box_y))
					matriz_control[box_x][box_y] = color_predeterminado
					if m == 'Minúscula':
						grafico.DrawText(str(matriz[box_y][box_x]).lower(),(box_x*BOX_SIZE+18,box_y*BOX_SIZE+14),font='Courier 25')
					if m == 'Mayúscula':
						grafico.DrawText(str(matriz[box_y][box_x]).upper(),(box_x*BOX_SIZE+18,box_y*BOX_SIZE+14),font='Courier 25')	
				else:
					dictioDeClicksDePalabras[que_soy.lower()].append((box_x,box_y))
					grafico.DrawRectangle((box_x*BOX_SIZE,box_y*BOX_SIZE),(box_x * BOX_SIZE + BOX_SIZE  , box_y * BOX_SIZE + BOX_SIZE),fill_color=color)
					matriz_control[box_x][box_y] = color
					if m == 'Minúscula':
						grafico.DrawText(str(matriz[box_y][box_x]).lower(),(box_x*BOX_SIZE+18,box_y*BOX_SIZE+14),font='Courier 25')
					if m == 'Mayúscula':
						grafico.DrawText(str(matriz[box_y][box_x]).upper(),(box_x*BOX_SIZE+18,box_y*BOX_SIZE+14),font='Courier 25')	
		
					
		if button is 'Listo':
			errores = []
			no_encontradas = []
			
			for clave in dicci.keys():
				for nombre_palabra, elemento in dicci[clave].items():
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

			
			if len(encontradas) < len(lista):
				for i in lista:
					ok = False
					for j in encontradas:
						if i.getPalabra() == j:
							ok = True
					if ok == False:
						no_encontradas.append(i)
			
			if len(no_encontradas) > 0:
				texto = 'Hay más palabras por encontrar:'
				errores.append(texto)
					
			resultado(ori, ayuda, m, errores)
			
			
		
def comenzar():
	palabrasXtipo,cantidadXtipo,orientacion,ayuda,mayusMinu,colores,colorSop=configurarYa()		
	lista=calcularCantidadIngresadas(cantidadXtipo,palabrasXtipo)
	juego_nuevo(lista,orientacion,ayuda,colores,mayusMinu,cantidadXtipo,colorSop)


comenzar()
