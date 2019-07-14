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
			sys.exit(0)
		if boton =="Aceptar":
			window.FindElement("out1").Update("")
			if valores["palabra"] !="":
				palabra=valores["palabra"]
				if not palabra.isalpha():
					window.FindElement("out1").Update("{} no es una palabra".format(str(palabra)))
				else:
					#en la siguiente línea, todos los caracteres son convertidos en minúsculas y se crea el objeto Palabra
					p = pal.Palabra(palabra.lower())
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
			if not hayPalabras( len(palabrasXtipo["sustantivo"]), len(palabrasXtipo["adjetivo"]),len(palabrasXtipo["verbo"])):
				window.FindElement("out1").Update('<INGRESE UNA PALABRA>')	
				continue
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
