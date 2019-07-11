# Sensores Raspberry Pi 3

Interfaz de Python para el manejo de los sensores de temperatura, sonido y la matriz de leds provistas por la cátedra de Python de la UNLP

![Raspberry Pi logo](https://upload.wikimedia.org/wikipedia/commons/thumb/f/fa/RPi-Logo-Stacked-PRINT.png/256px-RPi-Logo-Stacked-PRINT.png)

---

### Distribución de los pins.

  * [Pinout](https://pinout.xyz/#)

### Información sobre los dispositivos:

  * [Sensor de temperatura y humedad DHT12](http://www.robototehnika.ru/file/DHT12.pdf)
  * [Sensor de sonido] -- TODO
  * [Matriz de led MAX7219](https://www.sparkfun.com/datasheets/Components/General/COM-09622-MAX7219-MAX7221.pdf)

---

## Instalación:

### Dependencias:
  
  Asegurese de que su sistema es capaz de descargar e instalar librerías de Python con el package manager `pip3`

  ```shell
    sudo apt-get update
    sudo apt-get install python3-pip build-essential python-dev libfreetype6-dev libjpeg-dev
    sudo -H pip3 install -U pip setuptools wheel
  ```
  > Importante:
  > También deberia asegurarse de que su Raspberry tenga activado el uso de conecciones 1-wire, I2C y SPI. Esto puede verificarse facilmente en "configuración de Raspberry" dentro de la pestaña "interfaz"
  
### Instalación:
  Primero descargue y descomprima el repositorio en el directorio que desee, luego ejecute en la terminal:
  
  ```shell
    cd sensores-RPI
    sudo -H pip3 install -r requirements.txt
  ```
  También puede clonar el repositorio y repetir los pasos anteriores:
  
  ```shell
    git clone https://github.com/Skydler/sensores-RPI.git
  ```
  
  ---
  
  ## Uso:
    
  Después de la instalación cambie al directorio del repositorio
  
  ```shell
    cd sensores-RPI
  ```
  
  Allí se pueden ejecutar cualquiera de los modulos individualmente para probar un sensor en particular o si lo desea hay un ejemplo que prueba los 3 sensores en conjunto.
  
  Para ejecutar un modulo escriba en la terminal
  
  ```shell
    python3 modulo_a_ejecutar.py
  ```
 
 
