import asyncio
import websockets
import socketio

# Flask-SocketIO Client
sio = socketio.Client()

# Speichert verbundene ESPs mit zugehöriger melderNr
esp_websockets = {}

# Wir speichern den Event Loop
event_loop = asyncio.get_event_loop()

@sio.event
def connect():
    print("✅ Verbunden mit Flask-SocketIO-Server")

@sio.event
def disconnect():
    print("❌ Verbindung zu Flask-SocketIO-Server getrennt")

# Flask sendet "quittieren" → an passenden ESP weiterleiten
@sio.on("quittieren")
def on_quittieren(melderNr):
    print(f"➡️ Flask sendet quittieren für: {melderNr}")
    for ws, melderListe in esp_websockets.items():
        if melderNr in melderListe:
            asyncio.run_coroutine_threadsafe(
                ws.send(f"quittieren:{melderNr}"),
                event_loop
            )

# Mit Flask verbinden
sio.connect("http://localhost:5000")



# WebSocket-Handler für ESPs
async def handler(websocket):
    print("🔌 ESP verbunden")
    melderNr = None
    try:
        async for message in websocket:
            print(f"⬅️ ESP sendet: {message}")
            if message.startswith("register:"):
                melder_string = message.split(":")[1]
                melderListe = melder_string.split(",")
                esp_websockets[websocket] = melderListe
                print(f"🆔 Registriert mit Meldern: {melderListe}")

            elif message.startswith("alarm:"):
                melderNr = message.split(":")[1]
                print(f"🚨 Alarm von Melder {melderNr}")
                sio.emit("alarm", melderNr)
    except websockets.exceptions.ConnectionClosed:
        print(f"⚠️ ESP getrennt (Melder: {melderNr})")
    finally:
        if websocket in esp_websockets:
            abgemeldete_nr = esp_websockets.pop(websocket)
            print(f"🧹 Entfernt Melder {abgemeldete_nr}")
            # Optional: Flask über Trennung informieren
            sio.emit("melder_disconnect", {"melderNr": abgemeldete_nr})

# Startet WebSocket-Server für ESPs
async def main():
    async with websockets.serve(handler, "0.0.0.0", 8765):
        print("🚀 WebSocket-Bridge läuft auf Port 8765")
        await asyncio.Future()

if __name__ == "__main__":
    event_loop.run_until_complete(main())
