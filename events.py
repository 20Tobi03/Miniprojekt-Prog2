def register_socket_events(socket):

    @socket.on("connect")
    def handle_connect():
        print("Connected!")