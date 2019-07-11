# -*- coding: utf-8 -*-
import time
from luma.led_matrix.device import max7219
from luma.core.interface.serial import spi, noop
from luma.core.render import canvas
from luma.core.virtual import viewport
from luma.core.legacy import text, show_message
from luma.core.legacy.font import proportional, CP437_FONT, TINY_FONT, SINCLAIR_FONT, LCD_FONT

class Matriz:
    def __init__(self, numero_matrices=1, orientacion=0, rotacion=0, ancho=8, alto=8):
        self.font = [CP437_FONT, TINY_FONT, SINCLAIR_FONT, LCD_FONT]
        self.serial = spi(port=0, device=0, gpio=noop())
        self.device = max7219(self.serial, width=ancho, height=alto, cascaded=numero_matrices, rotate=rotacion)
    
    def mostrar_mensaje(self, msg, delay=0.1, font=1):
        show_message(self.device, msg, fill="white",
                     font=proportional(self.font[font]),
                     scroll_delay=delay)
    
    def dibujar(self, msg):
        with canvas(self.device) as draw:
            text(draw, (0, 0), chr(msg), fill="white")
            self.device.contrast(10 * 16)
            
    def dibujar_corazon(self):
        self.dibujar(3)
        
    def dibujar_vertical(self):
        words = ["Victor", "Echo", "Romeo"]

        virtual = viewport(self.device, width=self.device.width, height=len(words) * 8)
        with canvas(virtual) as draw:
            for i, word in enumerate(words):
                text(draw, (0, i * 8), word, fill="white", font=proportional(CP437_FONT))

        for i in range(virtual.height - self.device.height):
            virtual.set_position((0, i))
            time.sleep(0.05)
        
    
if __name__ == "__main__":
    matriz = Matriz()
    while True:
        matriz.mostrar_mensaje("Ciro", font=3)
        matriz.dibujar_corazon()
        time.sleep(1)
