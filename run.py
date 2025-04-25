from flask import Flask, render_template, send_from_directory, jsonify
from flask import Flask, render_template
from flask_socketio import SocketIO
import os
import sqlite3
from events import register_socket_events

app = Flask(__name__)
#app.config['SECRET_KEY']="test"
socket = SocketIO(app)

def get_latest_alarme(limit=10):
    conn = sqlite3.connect("./SQL/melderdb.db")  # ggf. Pfad anpassen
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute("""
        SELECT a.Timestemp, a.Art, a.MelderNr, m.Raum
        FROM alarme a
        LEFT JOIN melder m ON a.MelderNr = m.MelderNr
        ORDER BY a.Timestemp DESC
        LIMIT ?
    """, (limit,))
    rows = cursor.fetchall()
    conn.close()
    return [dict(row) for row in rows]

@app.route("/api/alarme")
def api_alarme():
    return jsonify(get_latest_alarme())

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


