import PySimpleGUI as sg
#from pattern.web import Wiktionary
import random
import string
import json
import sys
import palabras as pal
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

def mostrar(matrix,nxn,grph,fuente):
	for row in range(nxn):
		for col in range(nxn):
			grph.DrawRectangle((col * BOX_SIZE , row * BOX_SIZE ), (col * BOX_SIZE + BOX_SIZE  , row * BOX_SIZE + BOX_SIZE  ), line_color='black')
			#print((col * BOX_SIZE , row * BOX_SIZE ),(col * BOX_SIZE + BOX_SIZE  , row * BOX_SIZE + BOX_SIZE  ))
			grph.DrawText(str(matrix[row][col]),(col*BOX_SIZE+18,row*BOX_SIZE+14),font=fuente)

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
		[sg.Button("No quiero jugar mas", button_color = ('white', 'red'))]
		
		
		]
	
	
	window = sg.Window("grafico", resizable=True).Layout(diseño)
#	window.Finalize()
	
	while True:
		button,values=window.Read()
		if button is None:
			sys.exit(0)
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
			import jugar as game
# funcion terminar	
def terminar(dictioPalabrasAbuscar,dictioDeClicksDePalabras,colores,matriz_control,ok,encontradas,lista,lisNue):
	
	#linea Nueva.... esto es para contar por si hay clicks de mas	
	cant = 0
	cantClicks = 0
	errorTipo = False
	errorClick = False
	#hasta aqui las variables nuevas .......
	
	
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
					errores.append('La palabra ' + nombre_palabra + ' es ' + clave + '. Erróneamente fue coloreada como ' + t)
					#Linea Nueva, el OK se pondra en False porque el juego estuvo incompleto o mal echo
					ok=False
					errorTipo = True
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
			
	
	
	#Apartir de esta parte es para verificar si se clickearon letras de mas-----------------------------------
	#linea Nueva.... Recorro el diccionario de clicks y suma la cantidad de click realizados por el usuario			
	for claveClik in dictioDeClicksDePalabras.keys():
		for valor in dictioDeClicksDePalabras[claveClik]:
			cantClicks = cantClicks + 1
				
	#Linea Nueva.... Recorro la lista de palabras y sumo el total de caracteres
	for p in lista:
		cant= cant + len(p.getPalabra())
				
	#lineas Nuevas.... Si la cantidad de clicks es mayor a la cantidad de caracteres a buscar es porque hubo clicks de mas
	if cantClicks > cant:
		texto = 'Atencion!!  Coloreaste ' + str(cantClicks-cant) + ' letras de mas que no iban en la sopa. Vuelva a intentarlo'
		errores.append(texto)
		ok = False
		errorClick = True
	#hasta aqui..... lo nuevo--------------------------------------------------------------------------------------	
	
	#Parte modificada
	if len(encontradas) < len(lista):
		#Linea Nueva, el ok se pone en FALSE dado que falton palabras
		ok=False
		texto = 'Faltaron encontrar palabras. La lista total de palabras que debias encontrar son: '
		texto = texto + ' - '.join(lisNue)
		errores.append(texto)
	elif len(no_encontradas) == 0: #Linea nueva, indica que las palabras se encontraron todas, acertando o no el tipo. Se vera si en le acerto al tipo indicado en las "Observaciones"
		if errorTipo == True:
			if errorClick == True:
				#Si ocurrieron los dos errores informara los dos
				texto = 'Has encontrado todas las palabras en la sopa, pero coloreaste letras de mas y te equivocaste en los tipos'
				errores.append(texto)
			else:
				#Si solo ocurrio error de tipos
				texto = 'Has encontrado todas las palabras en la sopa, pero te equivocaste en los tipos'
				errores.append(texto)
		elif errorClick == True:
			#Si solo ocurrio error de letras extras coloreadas
			texto = 'Has encontrado todas las palabras en la sopa, pero coloreaste letras de mas'
			errores.append(texto)
					
	return errores,ok

def completarAyuda(cantLista,cantSust,cantAdj,cantVerbo,lisNue,ayuda):
	diseño= [	[sg.T('Total de palabras:'),sg.T(cantLista)],  
				[sg.T('Cantidad verbos:'), sg.T(cantVerbo)],
				[sg.T('Cantidad adjetivos:'), sg.T(cantAdj)],
				[sg.T('Cantidad sustantivos:'), sg.T(cantSust)]
			]
	if ayuda=='Ayuda máxima':
		diseño.append([sg.T('Lista de palabras: '), sg.T(" ".join(lisNue))])
	elif ayuda =='Ayuda mínima':
		diseño.append([sg.Button('Definiciones')])
	return diseño

def juego_nuevo(lista,orientacion,ayuda,colores,mayusMinu,diccionario,colorSop, diccioTodasPalabras,fuente):
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
	mostrar(matriz,nxn,grafico,fuente)
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
			sys.exit(0)
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
			errores,ok=terminar(dictioPalabrasAbuscar,dictioDeClicksDePalabras,colores,matriz_control,ok,encontradas,lista,lisNue)
			resultado(errores,lista,orientacion,ayuda,colores,mayusMinu,diccionario,colorSop, diccioTodasPalabras, ok)
