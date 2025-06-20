from machine import Pin, ADC
import network
import uasyncio as asyncio
from dfplayer import Player
from uwebsockets.client import connect

gas_analog = ADC(0)
WS_URL = "ws://192.168.178.163:8765"

class Sensor:
    def __init__(self, digitalPinI, melderNrI, websocket):
        self.digitalPin = Pin(digitalPinI, Pin.IN)
        self.melderNr = melderNrI
        self.alarm_active = False
        self.ws = websocket

    async def messen(self):
        while True:
            if self.digitalPin.value() == 0:
                await self.alarm()
            else:
                self.alarm_active = False
            await asyncio.sleep(0.05)

    async def alarm(self):
        global sound_active
        if not self.alarm_active:
            await self.ws.send(f"alarm:{self.melderNr}")
            print(sound_active)
            if not sound_active:
                df.play(1, 2)
                sound_active = True
            self.alarm_active = True
            

async def websocket_lesen(ws, sensoren):
    global sound_active
    while True:
        try:
            msg = await asyncio.wait_for(ws.recv(), timeout=0.1)
            if msg.startswith("quittieren:"):
                melderNr = msg.split(":")[1]
                for sensor in sensoren:
                    if sensor.melderNr == melderNr:
                        print(f"Quittierung erhalten für {melderNr}")
                        sensor.alarm_active=False
                        df.stop()
                        sound_active = False
        except asyncio.TimeoutError:
            print("Websocket Timeout Error")
            await asyncio.sleep(0.1)  # Expliziter Task-Wechsel
            continue 
        except Exception as e:
            print(f"WebSocket-Lesefehler: {e}")
            await asyncio.sleep(1)


async def analog_messen():
    while True:
        print("Analogwert:", gas_analog.read())
        await asyncio.sleep(1)

async def main():
    global df
    global sound_active
    sound_active = False
    df = Player()
    await asyncio.sleep(1)
    df.volume(1)

    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.connect('allgaeuDSL-EB', '240606072705')

    while not wlan.isconnected():
        await asyncio.sleep(0.5)
    print("WLAN verbunden")
    try:
        print("Versuche WebSocket-Verbindung...")
        ws = await connect(WS_URL)
        print("WebSocket verbunden")
    except Exception as e:
        print(f"Fehler beim Herstellen der WebSocket-Verbindung: {e}")
        return
    
    try:
        await ws.send("register:1/1,1/2")
        print("Daten gesendet")
    except Exception as e:
        print(f"Fehler beim Daten senden: {e}")
    ws.settimeout(0.5)

    sensor11 = Sensor(5, "1/1", ws)
    sensor12 = Sensor(4, "1/2", ws)

    sensoren = [sensor11, sensor12]

    await asyncio.gather(
        websocket_lesen(ws, sensoren),
        sensor11.messen(),
        sensor12.messen(),
        analog_messen(),
        return_exceptions=True  # Verhindert Abbruch bei Fehlern
    )

try:
    asyncio.run(main())
except Exception as e:
    print("Fehler:", e)
    while True:
        pass  # verhindert Neustart

