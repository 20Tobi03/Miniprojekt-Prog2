from machine import Pin, ADC
import time
import os

# Pin-Zuordnung für ESP8266
gas_digital = Pin(5, Pin.IN)     # D1 entspricht GPIO5
gas_analog = ADC(0)              # A0

class Sensor:
    def __init__(self, digitalPinI):
        self.digitalPin=Pin(digitalPinI, Pin.IN)
    
    def messen(self):
        gassensor_digital=self.digitalPin.value()
        if gassensor_digital==0:
            self.alarm()

    def alarm(self):
        print("Gas!")

sensor11=Sensor(5)
while True:
    sensor11.messen()
    time.sleep(0.2)

