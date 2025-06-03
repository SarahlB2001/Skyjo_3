import socket
import threading
import pickle
import settings as s


def recv_data(conn):
    try:
        data = conn.recv(4096)
        if data:
            return pickle.loads(data)
    except (EOFError, pickle.UnpicklingError, ConnectionResetError):
        return None
    return None

def send_data(conn, data):
    try:
        conn.sendall(pickle.dumps(data))
    except:
        pass

def client_thread(conn, spieler_id):


    try:
        # Spieler-ID senden
        send_data(conn, {"spieler_id": s.spieler_id + 1})

        if s.spieler_id == 0:
            daten = recv_data(conn)
            if daten:
                s.anzahl_spieler = daten.get("anzahl_spieler", 2)
                print(f"[INFO] Anzahl der Spieler festgelegt auf {s.anzahl_spieler}")
                s.anzahl_spieler_event.set()
        else:
            s.anzahl_spieler_event.wait()

        daten = recv_data(conn)
        if daten:
            name = daten.get("name", f"Spieler{s.spieler_id + 1}")
            with s.lock:
                s.spieler_daten[s.spieler_id + 1] = name
            print(f"[INFO] Spieler {s.spieler_id + 1} heißt {name}")

        # Allen Spielern "Warten..." senden
        if s.spieler_id < s.anzahl_spieler - 1:
            send_data(conn, {"message": "Warten auf andere Spieler..."})

        # Wenn alle verbunden, allen Startmeldung schicken
        if s.spieler_id == s.anzahl_spieler - 1:
            print("[INFO] Alle Spieler verbunden, sende Startnachricht...")
            for v in s.verbindungen:
                send_data(v, {"message": "Alle Spieler verbunden. Ihr könnt jetzt starten!"})

        # Hier könntest du später die Spiellogik oder weitere Kommunikation einbauen
        while True:
            # Server wartet z.B. auf weitere Daten, verarbeitet sie ...
            # Oder hält Verbindung offen
            pass

    except Exception as e:
        print(f"[FEHLER] Spieler {s.spieler_id + 1} Verbindung verloren: {e}")

def start_server():
    HOST = "0.0.0.0"
    PORT = 65432
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((HOST, PORT))
    server.listen(8)

    print(f"[SERVER] Server läuft auf {HOST}:{PORT}")

    spieler_id = 0

    while True:
        conn, addr = server.accept()

        if s.anzahl_spieler is not None and spieler_id >= s.anzahl_spieler:
            send_data(conn, {"error": "Maximale Spieleranzahl erreicht. Verbindung abgelehnt."})
            conn.close()
            continue

        print(f"[VERBUNDEN] Spieler {spieler_id + 1} von {addr}")
        s.verbindungen.append(conn)
        thread = threading.Thread(target=client_thread, args=(conn, spieler_id), daemon=True)
        thread.start()

        spieler_id += 1

        if s.anzahl_spieler is not None and spieler_id >= s.anzahl_spieler:
            print("[INFO] Alle Spieler verbunden, das Spiel kann starten.")
            # Warten auf Threads ist hier nicht nötig, da server läuft weiter

if __name__ == "__main__":
    start_server()
