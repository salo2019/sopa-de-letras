import PySimpleGUI as sg
#from pattern.web import Wiktionary
import random
import string
import json
import sys
import palabras as pal
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
def hayPalabras(sus,adj,verb):
	hay=False
	if (sus>0 or adj>0 or verb>0):
		hay=True
	return hay	
def mostrarReportes():
	archivoAbrir= open("archivos de texto/reporte.txt","r")
	datos= json.load(archivoAbrir)
	sg.Popup("REPORTES WIKTIO / PATTERN:", "\n \n".join(datos))
	#nuevo=[[sg.Multiline('\n \n'.join(datos),size=(30,20))]]	
#	w=sg.Window("Reportes").Layout(nuevo)
#	w.Read()	
	archivoAbrir.close()
#	w.Close()	


def	validarInput(input):
	ok = False
	if len(input) == 7 and input[0] == "#":
		ok = True
	return ok
	
	
def verificarColoresRepetidos(CSust, CAdj, CVer):
	listaColRepetidos = []
	if CSust == CAdj:
		listaColRepetidos.append('ColSust')
		listaColRepetidos.append('ColAdj')
	else:
		if CSust == CVer:
			listaColRepetidos.append('ColSust')
			listaColRepetidos.append('ColVer')
		else:
			if CAdj == CVer:
				listaColRepetidos.append('ColAdj')
				listaColRepetidos.append('ColVer')
	
	return listaColRepetidos
	


def configurarYa():
	#calcula las oficinas a mostrar
	archivo=open("archivos de texto/oficinas.txt","r")	
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
	
	#aqui para que funcione el eliminar y se actualize el multiline, tuve que cambiar por TRUE el "do_not_clear". Si no se cambia esto
	#el contenido queda fijo y no se actualiza
	columna_1 =[[sg.Text('Sustantivos')],
				[sg.Multiline(do_not_clear=False, disabled=False, key='sustantivo')]
				]
	columna_2 = [[sg.Text('Adjetivos')],
				[sg.Multiline(do_not_clear=False, disabled=False, key='adjetivo')]
				]
	columna_3 = [[sg.Text('Verbos')],
				[sg.Multiline(do_not_clear=False, disabled=False, key='verbo')]
				]
			
	#Armo para la eleccion de colores
	frame_layout = [	  
					[sg.T('Color Verbos: '),sg.In(change_submits=True, size=(10,1), do_not_clear=True, key='ColVer') , sg.ColorChooserButton('Elegir', target=(sg.ThisRow, -1))],
					[sg.T('Color Adjetivos: '), sg.In(change_submits=True, size=(10,1), do_not_clear=True, key='ColAdj'), sg.ColorChooserButton('Elegir', target=(sg.ThisRow, -1))],
					[sg.T('Color Sustantivos: '),sg.In(change_submits=True, size=(10,1), do_not_clear=True, key='ColSust'), sg.ColorChooserButton('Elegir', target=(sg.ThisRow, -1))]
				]	  

	#Armo el diseño de la interface
	diseño = [  [sg.Frame('Seleccion de colores', frame_layout)],
				[sg.Text('Ingreso de palabra'), sg.InputText(key="palabra")],
				[sg.Text("",size=(60,1),key="out1",text_color="red")],
				[sg.Submit('Aceptar'), sg.Button("Eliminar", button_color = ('white', 'red')),sg.Button("Reportes")],				
				[sg.Column(columna_1), sg.Column(columna_2), sg.Column(columna_3)],
				#cantidad a mostrar
				[sg.Text("Cantidad de sustantivos",size=(18,1)),sg.InputText(key="sustantivo1",size=(5,1))],
				[sg.Text("",text_color="red",key="sus",size=(20,1))],
				[sg.Text("Cantidad de adjetivos",size=(18,1)),sg.InputText(key="adjetivo1",size=(5,1))],
				[sg.Text("",text_color="red",key="adj",size=(20,1))],
				[sg.Text("Cantidad de verbos",size=(18,1)),sg.InputText(key="verbo1",size=(5,1))],
				[sg.Text("",text_color="red",key="ver",size=(25,1))],
				#fin
				[sg.Text('Orientacion: '), sg.Radio('Horizontal', 'orientacion',default=True,key="h"),  sg.Radio('Vertical', 'orientacion',key="v")],
				[sg.Text('Tipo de Ayuda: '), sg.Radio('Sin ayuda', 'ayuda',default=True,key="SA"),  sg.Radio('Ayuda mínima', 'ayuda',key="AMin"), sg.Radio('Ayuda máxima', 'ayuda',key="AM")],
				[sg.Text('¿Letras en mayúscula ó minúscula?'), sg.Radio('Letra mayúscula', 'tipo_letra',key="mayus"),  sg.Radio('Letra minúscula', 'tipo_letra',default=True,key="min")],
				 listaOfi,
				 [sg.Text('Fuente:'),sg.Radio('Courier 25','fuente',default=True,key='FontA'),sg.Radio('Aharoni',"fuente",key='FontB'),sg.Radio("Verdana","fuente",key='FontC')],
				[sg.Submit('Terminar')]		
			]

	window = sg.Window('Ajustes', resizable=True).Layout(diseño)
	while True:
		boton,valores=window.Read()
		if boton is None:
			sys.exit(0)
		eliminada=False
		if boton =="Aceptar":
			window.FindElement("out1").Update("")
			if valores["palabra"] !="" and len(valores["palabra"])>1:
				palabra=valores["palabra"]
				if not palabra.isalpha():
					window.FindElement("out1").Update("{} no es una palabra".format(str(palabra)))
					window.FindElement('sustantivo').Update(value=list(map(lambda x: x.getPalabra(),palabrasXtipo['sustantivo'])),append=True)
					window.FindElement('adjetivo').Update(value=list(map(lambda x: x.getPalabra(),palabrasXtipo['adjetivo'])),append=True)
					window.FindElement('verbo').Update(value=list(map(lambda x: x.getPalabra(),palabrasXtipo['verbo'])),append=True)
				else:
					#en la siguiente línea, todos los caracteres son convertidos en minúsculas y se crea el objeto Palabra
					p = pal.Palabra(palabra.lower())
					#tener en cuenta si no tiene clasificacion 
					#como uso multiline me debo fijar como agregar esta palabra
					
					#chequea si se cancelaron los ingresos manuales de tipo y definición de la palabra
					if p.getDefinicion() == "sinDefinicion":
						window.FindElement("out1").Update("El ingreso de la palabra '{}' fue cancelado".format(str(palabra)))
						window.FindElement('sustantivo').Update(value=list(map(lambda x: x.getPalabra(),palabrasXtipo['sustantivo'])),append=True)
						window.FindElement('adjetivo').Update(value=list(map(lambda x: x.getPalabra(),palabrasXtipo['adjetivo'])),append=True)
						window.FindElement('verbo').Update(value=list(map(lambda x: x.getPalabra(),palabrasXtipo['verbo'])),append=True)	
					else:
						#mirar las siguientes modificaciones para que se tuvo que hacer para el "ELIMINAR"
						tuplaVerificacion = repetido(p, palabrasXtipo)
						if tuplaVerificacion[0]:
							palabrasXtipo[p.esTipo()].append(p)
							#agregado para que se muestre
							window.FindElement('sustantivo').Update(value=list(map(lambda x: x.getPalabra(),palabrasXtipo['sustantivo'])),append=True)
							window.FindElement('adjetivo').Update(value=list(map(lambda x: x.getPalabra(),palabrasXtipo['adjetivo'])),append=True)
							window.FindElement('verbo').Update(value=list(map(lambda x: x.getPalabra(),palabrasXtipo['verbo'])),append=True)
						else:
							window.FindElement("out1").Update("La palabra '{}' fue agregada anteriormente como {}".format(str(palabra.lower()), tuplaVerificacion[1]))
							#agregado para que se muestre
							window.FindElement('sustantivo').Update(value=list(map(lambda x: x.getPalabra(),palabrasXtipo['sustantivo'])),append=True)
							window.FindElement('adjetivo').Update(value=list(map(lambda x: x.getPalabra(),palabrasXtipo['adjetivo'])),append=True)
							window.FindElement('verbo').Update(value=list(map(lambda x: x.getPalabra(),palabrasXtipo['verbo'])),append=True)	
					
			else:
				window.FindElement("out1").Update("Ingrese una palabra")
				#agregado para que se muestre
				window.FindElement('sustantivo').Update(value=list(map(lambda x: x.getPalabra(),palabrasXtipo['sustantivo'])),append=True)
				window.FindElement('adjetivo').Update(value=list(map(lambda x: x.getPalabra(),palabrasXtipo['adjetivo'])),append=True)
				window.FindElement('verbo').Update(value=list(map(lambda x: x.getPalabra(),palabrasXtipo['verbo'])),append=True)
			
		#Funcionalidad nueva para eliminar palabras. Se ha modificado tambien los botones en el multiline de las palabras en configurar. Mirar mas arriba
		#Tambien tuve que modificar funcionalidades del boton aceptar
		
		if boton == "Reportes":
			# abro el archivo de reportes,datos  es una lista con los reportes
			mostrarReportes()
			#agregado para que se muestre. Esto es agregado por el ELIMINAR
			window.FindElement('sustantivo').Update(value=list(map(lambda x: x.getPalabra(),palabrasXtipo['sustantivo'])),append=True)
			window.FindElement('adjetivo').Update(value=list(map(lambda x: x.getPalabra(),palabrasXtipo['adjetivo'])),append=True)
			window.FindElement('verbo').Update(value=list(map(lambda x: x.getPalabra(),palabrasXtipo['verbo'])),append=True)
		if boton == "Eliminar":
			window.FindElement("out1").Update("")
			if valores["palabra"] !="":
				palEliminar=valores["palabra"].lower()
				for clave in palabrasXtipo.keys():
					for valor in palabrasXtipo[clave]:
						if valor.getPalabra() == palEliminar:
							palabrasXtipo[clave].remove(valor)
							eliminada=True
				if eliminada==False:
					window.FindElement("out1").Update('No Exite esa palabra')
					window.FindElement('sustantivo').Update(value=list(map(lambda x: x.getPalabra(),palabrasXtipo['sustantivo'])),append=True)
					window.FindElement('adjetivo').Update(value=list(map(lambda x: x.getPalabra(),palabrasXtipo['adjetivo'])),append=True)
					window.FindElement('verbo').Update(value=list(map(lambda x: x.getPalabra(),palabrasXtipo['verbo'])),append=True)
				else:
					window.FindElement('sustantivo').Update(value=list(map(lambda x: x.getPalabra(),palabrasXtipo['sustantivo'])),append=True)
					window.FindElement('adjetivo').Update(value=list(map(lambda x: x.getPalabra(),palabrasXtipo['adjetivo'])),append=True)
					window.FindElement('verbo').Update(value=list(map(lambda x: x.getPalabra(),palabrasXtipo['verbo'])),append=True)
					window.FindElement("out1").Update("Palabra eliminada correctamente")
			else:
				window.FindElement("out1").Update("Ingrese la palabra que desea eliminar")
				window.FindElement('sustantivo').Update(value=list(map(lambda x: x.getPalabra(),palabrasXtipo['sustantivo'])),append=True)
				window.FindElement('adjetivo').Update(value=list(map(lambda x: x.getPalabra(),palabrasXtipo['adjetivo'])),append=True)
				window.FindElement('verbo').Update(value=list(map(lambda x: x.getPalabra(),palabrasXtipo['verbo'])),append=True)
		#hasta aqui el eliminar
		
		#Esto que sigue a continuacion es para resolver el problema ocurrido si configuro los colores despues de agregar palabras.
		#Si esto no esta, al elegir los colores despues de agregar palabras, se deja de mostrar la lista en la pantalla, pero si esta internamente.
		if boton == "ColVer" or boton == "ColAdj" or boton == "ColSust":
			if len(palabrasXtipo['sustantivo']) != 0 or len(palabrasXtipo['adjetivo']) != 0 or len(palabrasXtipo['verbo']) != 0:
				window.FindElement('sustantivo').Update(value=list(map(lambda x: x.getPalabra(),palabrasXtipo['sustantivo'])),append=True)
				window.FindElement('adjetivo').Update(value=list(map(lambda x: x.getPalabra(),palabrasXtipo['adjetivo'])),append=True)
				window.FindElement('verbo').Update(value=list(map(lambda x: x.getPalabra(),palabrasXtipo['verbo'])),append=True)		
		
		
		if boton=="Terminar":
			if not hayPalabras(len(palabrasXtipo["sustantivo"]), len(palabrasXtipo["adjetivo"]),len(palabrasXtipo["verbo"])):
				window.FindElement("out1").Update('<INGRESE UNA PALABRA>')	
				continue
			
			#Esto se ha retocado para el eliminar. Simplemente encadeno los if para que sea mas facil mostrar las palabras
			if valores["sustantivo1"].isdigit():
				cantidadXtipo["sustantivo"]= int(valores["sustantivo1"])
				window.FindElement("sus").Update('')
				if valores["adjetivo1"].isdigit():
					cantidadXtipo["adjetivo"]= int(valores["adjetivo1"])
					window.FindElement("adj").Update('')
					if valores["verbo1"].isdigit():
						cantidadXtipo["verbo"]= int(valores["verbo1"])
						window.FindElement("ver").Update('')
						if cantidadXtipo["sustantivo"] == 0:
							if cantidadXtipo["adjetivo"] == 0:
								if cantidadXtipo["verbo"] == 0:
									window.FindElement("ver").Update('NO PUEDEN SER TODOS 0')
									#agregado para que se muestre
									window.FindElement('sustantivo').Update(value=list(map(lambda x: x.getPalabra(),palabrasXtipo['sustantivo'])),append=True)
									window.FindElement('adjetivo').Update(value=list(map(lambda x: x.getPalabra(),palabrasXtipo['adjetivo'])),append=True)
									window.FindElement('verbo').Update(value=list(map(lambda x: x.getPalabra(),palabrasXtipo['verbo'])),append=True)
									continue   				
					else:
						window.FindElement("ver").Update('<INGRESE UN NUMERO>')
						#agregado para que se muestre
						window.FindElement('sustantivo').Update(value=list(map(lambda x: x.getPalabra(),palabrasXtipo['sustantivo'])),append=True)
						window.FindElement('adjetivo').Update(value=list(map(lambda x: x.getPalabra(),palabrasXtipo['adjetivo'])),append=True)
						window.FindElement('verbo').Update(value=list(map(lambda x: x.getPalabra(),palabrasXtipo['verbo'])),append=True)
						continue
				else:
					window.FindElement("adj").Update('<INGRESE UN NUMERO>')
					#agregado para que se muestre
					window.FindElement('sustantivo').Update(value=list(map(lambda x: x.getPalabra(),palabrasXtipo['sustantivo'])),append=True)
					window.FindElement('adjetivo').Update(value=list(map(lambda x: x.getPalabra(),palabrasXtipo['adjetivo'])),append=True)
					window.FindElement('verbo').Update(value=list(map(lambda x: x.getPalabra(),palabrasXtipo['verbo'])),append=True)
					continue
			else:
				window.FindElement("sus").Update('<INGRESE UN NUMERO>')
				#agregado para que se muestre
				window.FindElement('sustantivo').Update(value=list(map(lambda x: x.getPalabra(),palabrasXtipo['sustantivo'])),append=True)
				window.FindElement('adjetivo').Update(value=list(map(lambda x: x.getPalabra(),palabrasXtipo['adjetivo'])),append=True)
				window.FindElement('verbo').Update(value=list(map(lambda x: x.getPalabra(),palabrasXtipo['verbo'])),append=True)
				continue
					
		
			
			
			#Chequeo de colores repetidos
			if validarInput(valores["ColSust"]) == False or validarInput(valores["ColAdj"]) == False or validarInput(valores["ColVer"]) == False:
				sg.Popup('ERROR','Los colores deben ser seleccionados nuevamente por error de carga. Si desea seleccionar un color de la manera adecuada, presione el botón "Elegir" en la categoría correspondiente. A continuación, marque el color y haga click en "Aceptar"')
				window.FindElement("ColSust").Update('')
				window.FindElement("ColAdj").Update('')
				window.FindElement("ColVer").Update('')
				#agregado para que se muestre
				window.FindElement('sustantivo').Update(value=list(map(lambda x: x.getPalabra(),palabrasXtipo['sustantivo'])),append=True)
				window.FindElement('adjetivo').Update(value=list(map(lambda x: x.getPalabra(),palabrasXtipo['adjetivo'])),append=True)
				window.FindElement('verbo').Update(value=list(map(lambda x: x.getPalabra(),palabrasXtipo['verbo'])),append=True)
				continue
			else: 
				listaRepetidos = verificarColoresRepetidos(valores['ColSust'], valores['ColAdj'], valores['ColVer'])
				if len(listaRepetidos) > 0:
					sg.Popup('ERROR','Los colores para sustantivos, adjetivos y verbos deben ser diferentes. Vuelva a seleccionar los colores repetidos')
					window.FindElement(listaRepetidos[0]).Update('')
					window.FindElement(listaRepetidos[1]).Update('')
					#agregado para que se muestre
					window.FindElement('sustantivo').Update(value=list(map(lambda x: x.getPalabra(),palabrasXtipo['sustantivo'])),append=True)
					window.FindElement('adjetivo').Update(value=list(map(lambda x: x.getPalabra(),palabrasXtipo['adjetivo'])),append=True)
					window.FindElement('verbo').Update(value=list(map(lambda x: x.getPalabra(),palabrasXtipo['verbo'])),append=True)
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
	if valores['FontA']== True:
		fuente='Courier 25'
	elif valores['FontB']==True:
		fuente= 'Aharoni'
	elif valores['FontC']==True:
		fuente='Verdana'
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

	
	return palabrasXtipo,cantidadXtipo,orientacion,ayuda,mayusMinu,colores,color,fuente
