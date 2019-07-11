#! /usr/bin/python
# -*- coding: utf-8 -*-
import os
import json
import time
from temperatura import Temperatura

temperatura = Temperatura()


def leer_temp():
    info_temperatura = temperatura.datos_sensor()
    info_temperatura.update({"fecha": time.asctime(time.localtime(time.time()))})
    return info_temperatura
 
def guardar_temp(info):
    with open(os.path.join("archivos_texto", "ultimo_log_temperatura.json"), "r") as log_file:
        try:
            lista_de_temperaturas = json.load(log_file)
        except Exception:
            # En caso de que el json no sea una lista
            lista_de_temperaturas = []
    lista_de_temperaturas.append(info)
    with open(os.path.join("archivos_texto", "ultimo_log_temperatura.json"), "w") as log_file:
        json.dump(lista_de_temperaturas, log_file, indent=4)

if __name__ == "__main__":
    while True:
        time.sleep(300) # Espera 5 min antes de la proxima lectura
        temp = leer_temp()
        guardar_temp(temp)

