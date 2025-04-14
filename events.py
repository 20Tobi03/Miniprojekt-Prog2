
def register_socket_events(socket):

    @socket.on("connect")
    def handle_connect(melderNr):
        print("Someone joined!")

    @socket.on("melder_join")
    def handle_connect(melderNr):
        print("Connected: "+ melderNr)
        socket.emit("melder_join", melderNr, to=None)

    @socket.on("melder_leave")
    def handle_disconnect(melderNr):
        print("Disonnected: "+ melderNr)
        socket.emit("melder_leave", melderNr, to=None)

    @socket.on("quittieren")
    def handle_quittieren(melderNr):
        print("Quittiert: "+ melderNr)
        socket.emit("quittieren", melderNr, to=None)

    @socket.on("noAlarm")
    def handle_noAlarms(melderNr):
        socket.emit("noAlarm", melderNr, to=None)

    @socket.on("alarm")
    def handle_alarm(melderNr):
        print("Alarm: "+ melderNr)
        socket.emit("alarm", melderNr, to=None)

