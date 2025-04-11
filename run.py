from flask import Flask, render_template
from flask_socketio import SocketIO
from events import register_socket_events

app = Flask(__name__)
#app.config['SECRET_KEY']="test"
socket = SocketIO(app)

@app.route("/")
def main():
    return render_template("main.html")

register_socket_events(socket)

if __name__== "__main__":
    socket.run(app, host="0.0.0.0", port=5000)


