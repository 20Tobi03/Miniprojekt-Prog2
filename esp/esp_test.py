import socketio
import threading
import time

socket=socketio.Client()
melderNr="1/2"

@socket.on("quittieren")
def handle_quitteren(melderNrInput):
    if melderNr==melderNrInput:
        print("Quittiert!")

@socket.on("connect")
def handle_connect():
    socket.emit("melder_join", melderNr)

@socket.on("alarm_aus")
def handle_alarm_aus():
    print("Alarm aus!")

socket.connect("http://localhost:5000/")
time.sleep(5)
socket.emit("alarm", melderNr)
time.sleep(5)
socket.emit("alarm", melderNr)
time.sleep(5)
socket.emit("noAlarm", melderNr)
socket.wait()