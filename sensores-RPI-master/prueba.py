#!/usr/bin/python
# -*- coding: utf-8 -*-
import time
from matriz import Matriz
from sonido import Sonido
from temperatura import Temperatura

# Conexión de los sensores en sus respectivos pines
# Matriz --> vcc: 2, gnd: 6, din: 19, cs: 24, clk: 23
# Sonido --> a0: 7, gnd: 9, vc: 3, d0: 15
# Temperatura --> vcc: 1, sda: 11, clk: 14

# Activamos los sensores que vamos a usar
# matriz = Matriz(numero_matrices=2, ancho=16)
matriz = Matriz()
sonido = Sonido()
temperatura = Temperatura()
def guardar_temp(info):
    with open("oficinas.json"), "r") as log_file:
        try:
            lista_de_temperaturas = json.load(log_file)
        except Exception:
            # En caso de que el json no sea una lista
            lista_de_temperaturas = []
    lista_de_temperaturas.append(info)
    with open("oficinas.json"), "w") as log_fil:
        json.dump(lista_de_temperaturas, log_fil, indent=4)

def acciones():
    print ("Sonido Detectado!")
    temp_data = temperatura.datos_sensor()
    temp_formateada = 'Temperatura = {0:0.1f}°C  Humedad = {1:0.1f}%'.format(temp_data['temperatura'], temp_data['humedad'])
    temp_data.update({"fecha": time.asctime(time.localtime(time.time()))})
    #guardar temp_data en un archivo
    guardar_temp(temp_data)
    matriz.mostrar_mensaje(temp_formateada, delay=0.08, font=2)
