import asyncio
import websockets
import socketio

# Flask-SocketIO Client
sio = socketio.Client()

# Speichert verbundene ESPs mit zugehöriger melderNr
esp_websockets = {}

event_loop = asyncio.get_event_loop()

#Von Flask Server zu ESP
@sio.event
def connect():
    print("Verbunden mit Flask-SocketIO-Server")

@sio.event
def disconnect():
    print("Verbindung zu Flask-SocketIO-Server getrennt")

@sio.on("quittieren")
def on_quittieren(melderNr):
    print(f"Flask sendet quittieren für: {melderNr}")
    for ws, melderListe in esp_websockets.items():
        if melderNr in melderListe:
            asyncio.run_coroutine_threadsafe(
                ws.send(f"quittieren:{melderNr}"), #an ESP
                event_loop
            )

# Mit Flask verbinden
sio.connect("http://localhost:5000")



# Von ESP zu FLask Server
async def handler(websocket):
    print("ESP verbunden")
    melderNr = None
    try:
        async for message in websocket:
            print(f"ESP sendet: {message}")

            #speichern der Sensoren
            if message.startswith("register:"):
                melder_string = message.split(":")[1]
                melderListe = melder_string.split(",")
                esp_websockets[websocket] = melderListe
                print(f"Registriert mit Meldern: {melderListe}")
                for nummer in melderListe:
                    sio.emit("melder_join", nummer) #Online auf Webseite

            elif message.startswith("alarm:"):
                melderNr = message.split(":")[1]
                print(f"Alarm von Melder {melderNr}")
                sio.emit("alarm", melderNr) #an Flask Server senden
                
    #Wenn der ESP offline geht
    except websockets.exceptions.ConnectionClosed:
        for melder in esp_websockets[websocket]:
            print(f"ESP getrennt (Melder: {melder})")
            sio.emit("esp_disconnect", melder)
            if websocket in esp_websockets:
                abgemeldete_nr = esp_websockets.pop(websocket)
                print(f"Entfernt Melder {abgemeldete_nr}")

        

# Startet WebSocket-Server für ESPs
async def main():
    async with websockets.serve(handler, "0.0.0.0", 8765):
        print("WebSocket-Bridge läuft auf Port 8765")
        await asyncio.Future()

if __name__ == "__main__":
    event_loop.run_until_complete(main())
