import socketio
import threading
import time

socket=socketio.Client()
melderNr="1/1"

@socket.on("quittieren")
def handle_quitteren(melderNrInput):
    if melderNr==melderNrInput:
        print("Quittiert!")

@socket.on("connect")
def handle_connect():
    socket.emit("melder_join", melderNr)

socket.connect("http://localhost:5000/")
time.sleep(5)
socket.emit("alarm", melderNr)
time.sleep(5)
socket.emit("noAlarm", melderNr)
socket.wait()