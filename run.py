from flask import Flask, render_template, send_from_directory   
from flask import Flask, render_template
from flask_socketio import SocketIO
import os
from events import register_socket_events

app = Flask(__name__)
#app.config['SECRET_KEY']="test"
socket = SocketIO(app)

# Route für statische Bilder im "Plaene"-Ordner
@app.route('/Plaene/<path:filename>')
def serve_image(filename):
    # Gebe die Datei aus dem Plaene-Ordner zurück
    return send_from_directory(os.path.join(app.root_path, 'Plaene'), filename)

@app.route("/")
def main():
    return render_template("main.html")

register_socket_events(socket)

if __name__== "__main__":
    socket.run(app, host="0.0.0.0", port=5000)


