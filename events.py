
import sqlite3
from flask import request
import datetime


def register_socket_events(socket):

    @socket.on("connect")
    def handle_connect(melderNr):
        print("Someone joined!")

    #Von ESP zu Webseite
    @socket.on("melder_join")
    def handle_connect(melderNr):
        print("Connected: "+ melderNr)
        socket.emit("melder_join", melderNr, to=None)

    @socket.on("esp_disconnect")
    def handle_esp_disconnect(melderNr):
        socket.emit("esp_disconnect", melderNr, to=None)

        #DB Eintrag
        conn = sqlite3.connect('./SQL/melderdb.db')
        cursor = conn.cursor()
        timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        cursor.execute(
        "INSERT INTO alarme (Art, Timestemp, MelderNr) VALUES (?, ?, ?)",
        ("Offline", timestamp, melderNr)
        )
        conn.commit()
        conn.close()

    @socket.on("alarm")
    def handle_alarm(melderNr):
        print("Alarm: "+ melderNr)

        #Melder Plan abfragen
        conn = sqlite3.connect('./SQL/melderdb.db')
        cursor = conn.cursor()
        cursor.execute("SELECT PlanPath FROM melder WHERE MelderNr = ?", (melderNr,))
        result = cursor.fetchone()
        plan_path = result[0]

        #Alarm in DB eintragen
        timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        cursor.execute(
        "INSERT INTO alarme (Art, Timestemp, MelderNr) VALUES (?, ?, ?)",
        ("Brand", timestamp, melderNr)
        )
        conn.commit()

        socket.emit("alarm", {'melderNr': melderNr, 'melderPath': plan_path}, to=None) #Alarm und Pfad an Webseite
        conn.close()

    #Von Webseite zu ESP
    @socket.on("quittieren")
    def handle_quittieren(melderNr):
        print("Quittiert: "+ melderNr)
        socket.emit("quittieren", melderNr, to=None)

    @socket.on("alarm_aus")
    def handle_alarm_aus():
        print("Alarm aus!")
        socket.emit("alarm_aus", to=None)

    

