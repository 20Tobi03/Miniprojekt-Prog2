import socketio
import threading
import time

socket=socketio.Client()

#def on_aaa_response(args):
    #print('on_aaa_response', args['data'])

def noAlarms():
    for i in range(5):
        socket.emit("noAlarms", "Alles in Ordnung")
    socket.emit("Alarm", "Melder 2") 

@socket.on("connect")
def handle_connect():
    threading.Thread(target=noAlarms, daemon=True).start()


socket.connect("http://192.168.178.126:5000")
socket.wait()