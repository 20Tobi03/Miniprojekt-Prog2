def register_socket_events(socket):

    @socket.on("connect")
    def handle_connect():
        print("Connected!")

    @socket.on("noAlarms")
    def handle_noAlarms(message):
        print(message)

    @socket.on("Alarm")
    def handle_Alarm(message):
        print(message)
