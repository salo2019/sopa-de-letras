#!/usr/bin/python3
# -*- coding: utf-8 -*-
import Adafruit_DHT

"""
Conección One-Wire:
Resistencia 10K entre VCC y DATA
1er pin del sensor al VCC 3,3V
2do pin del sensor DATA al BCM 17( pin numero 11 de la raspberry)
4to pin del sensor al GND de la raspberry
"""

class Temperatura:

    def __init__(self, pin=17, sensor=Adafruit_DHT.DHT11):
        # Usamos el DHT11 que es compatible con el DHT12 
        self._sensor = sensor 
        self._data_pin = pin

    def datos_sensor(self):
      """ Devuelve un diccionario con la temperatura y humedad """
      humedad, temperatura = Adafruit_DHT.read_retry(self._sensor, self._data_pin)
      return {'temperatura': temperatura, 'humedad': humedad}
     

if __name__ == "__main__":
    import time

    temp = Temperatura()
    while True:
        datos = temp.datos_sensor()
        # Imprime en la consola las variables temperatura y humedad con un decimal
        print('Temperatura = {0:0.1f}°C  Humedad = {1:0.1f}%'.format(datos['temperatura'], datos['humedad']))
        time.sleep(0.5)
