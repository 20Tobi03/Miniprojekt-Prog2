from machine import Pin, ADC, UART
import time
import os
import network
from dfplayer import Player
import urequests
import uasyncio as asyncio

# Pin-Zuordnung für ESP8266    
gas_analog = ADC(0)              # A0

class Sensor:
    def __init__(self, digitalPinI, melderNrI):
        self.digitalPin=Pin(digitalPinI, Pin.IN)
        self.melderNr=melderNrI
        self.alarm_active = False  
    
    async def messen(self):
        while True:
            gassensor_digital=self.digitalPin.value()
            if gassensor_digital==0:
                await self.alarm()
            else:
                self.alarm_active=False
            await asyncio.sleep(0.2)

    async def alarm(self):
        global sound_active
        print("gas")
        if not self.alarm_active:
            await self.send_alarm(self.melderNr)
            if not sound_active:
                df.play(01,02)
                sound_active=True
            self.alarm_active = True
            await asyncio.sleep(20) #nach 3 Sekunden wieder aufhören, nur Test!
            df.stop()
            sound_active=False

    async def send_alarm(self, melderNr):
        print("alarm gesendet")
        url = "http://192.168.178.163:5000/api/alarm"  # Flask-Server URL
        headers = {"Content-Type": "application/json"}
        payload = {"melderNr": melderNr}
        response = urequests.post(url, json=payload, headers=headers)
        print("Antwort vom Server:", response.text)
    
async def analog_messen():
    while True:
        print("Analogwert:", gas_analog.read())
        await asyncio.sleep(1)  # alle 1 Sekunde analog messen

async def main():
    global df
    global sound_active
    sound_active=False
    sensor11=Sensor(5, "1/1")	# D1 entspricht GPIO5
    sensor12=Sensor(4, "1/2")
    df = Player()
    await asyncio.sleep(1)
    df.volume(10)


    sta_if = network.WLAN(network.STA_IF)
    sta_if.active(True)
    sta_if.connect('allgaeuDSL-EB', '240606072705')

    while not sta_if.isconnected():
        pass

    ip = sta_if.ifconfig()[0]
    print('IP-Adresse:', ip)
    
    await asyncio.gather(
        sensor11.messen(),
        sensor12.messen(),
        analog_messen()
    )
    
asyncio.run(main())
        





