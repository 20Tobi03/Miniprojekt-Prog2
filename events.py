
from flask import request

def register_socket_events(socket):

    connected_melder = {}  # key: sid, value: melderNr

    @socket.on("connect")
    def handle_connect(melderNr):
        print("Someone joined!")

    @socket.on("melder_join")
    def handle_connect(melderNr):
        print("Connected: "+ melderNr)
        connected_melder[request.sid] = melderNr
        socket.emit("melder_join", melderNr, to=None)

    @socket.on("disconnect")
    def handle_disconnect():
        sid = request.sid
        if sid in connected_melder:
            melderNr = connected_melder.pop(sid)
            print("Melder disconnected: " + melderNr)
            socket.emit("melder_leave", melderNr, to=None)
        else:
            print("Browser disconnected (sid: " + sid + ")")

    @socket.on("quittieren")
    def handle_quittieren(melderNr):
        print("Quittiert: "+ melderNr)
        socket.emit("quittieren", melderNr, to=None)

    @socket.on("alarm_aus")
    def handle_alarm_aus():
        print("Alarm aus!")
        socket.emit("alarm_aus", to=None)

    @socket.on("noAlarm")
    def handle_noAlarms(melderNr):
        socket.emit("noAlarm", melderNr, to=None)

    @socket.on("alarm")
    def handle_alarm(melderNr):
        print("Alarm: "+ melderNr)
        socket.emit("alarm", melderNr, to=None)

