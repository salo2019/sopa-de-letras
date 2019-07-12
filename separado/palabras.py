import PySimpleGUI as sg
from pattern.web import Wiktionary
import random
import string
import json
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
						[sg.Submit("Agregar"), sg.Submit("Cancelar")]
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
						
					if boton == "Cancelar":
						tipo = "sinTipo"
						valores["definicion"] = "sinDefinicion"
						break
						
				#se cierra la ventana. Si presiona "Cancelar", la ventana se cierra y los valores son iguales a None
				window.Close()
				
				return tipo,valores["definicion"]
			else:
				diseñoo=[
						[sg.Text("Ingrese una Definicion de ",str(p)),sg.InputText(key="definicion")],
						[sg.Text("Tipo"),sg.Radio('Sustantivo','tipo',key="sustantivo"),sg.Radio('Adjetivo','tipo',key="adjetivo"),sg.Radio('Verbo','tipo',key="verbo")],
						[sg.Submit("Agregar"), sg.Submit("Cancelar")]
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
