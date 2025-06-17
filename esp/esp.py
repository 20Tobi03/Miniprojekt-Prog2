from machine import Pin, ADC
import network
import uasyncio as asyncio
from dfplayer import Player
import uwebsockets.client

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
            await asyncio.sleep(0.2)

    async def alarm(self):
        global sound_active
        if not self.alarm_active:
            await self.ws.send(f"alarm:{self.melderNr}")
            if not sound_active:
                df.play(1, 2)
                sound_active = True
            self.alarm_active = True
            await asyncio.sleep(20)
            df.stop()
            sound_active = False

    async def empfangen(self):
        while True:
            try:
                msg = await self.ws.recv()
                if msg.startswith("quittieren:"):
                    melderNr = msg.split(":")[1]
                    if melderNr == self.melderNr:
                        print(f"Quittierung erhalten für {melderNr}")
            except:
                break

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

    ws = await uwebsockets.client.connect(WS_URL)

    await ws.send("register:1/1")
    await ws.send("register:1/2")

    sensor11 = Sensor(5, "1/1", ws)
    sensor12 = Sensor(4, "1/2", ws)

    await asyncio.gather(
        sensor11.empfangen(),
        sensor12.empfangen(),
        sensor11.messen(),
        sensor12.messen(),
        analog_messen()
    )

try:
    asyncio.run(main())
except Exception as e:
    print("Fehler:", e)
