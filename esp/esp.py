import socketio
import threading
import time

socket=socketio.Client()

#def on_aaa_response(args):
    #print('on_aaa_response', args['data'])

def noAlarms():
    while True:
        socket.emit("noAlarms", "Alles in Ordnung")
        time.sleep(5)
     

@socket.on("connect")
def handle_connect():
    threading.Thread(target=noAlarms, daemon=True).start()
    socket.emit("Alarm", "Melder 2")

socket.connect("http://192.168.178.126:5000")
socket.wait()