from machine import Pin, ADC, UART
import time
import os
from dfplayer import Player

# Pin-Zuordnung für ESP8266    
gas_analog = ADC(0)              # A0

class Sensor:
    def __init__(self, digitalPinI):
        self.digitalPin=Pin(digitalPinI, Pin.IN)
        self.alarm_active = False  
    
    def messen(self):
        gassensor_digital=self.digitalPin.value()
        if gassensor_digital==0:
            self.alarm()
        else:
            self.alarm_active=False

    def alarm(self):
        print("gas")
        if not self.alarm_active:
            df.play(01,01)
            self.alarm_active = True
            time.sleep(3) #nach 3 Sekunden wieder aufhören, nur Test!
            df.stop()
            

sensor11=Sensor(5)	# D1 entspricht GPIO5
sensor12=Sensor(4)
df = Player()
time.sleep(1)
df.volume(10)


while True:
    sensor11.messen()
    sensor12.messen()
    time.sleep(0.2)
    print(gas_analog.read())


