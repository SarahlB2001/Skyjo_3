import socket
import threading
import pickle

# Globale Variablen
spieler_daten = {}
verbindungen = []
anzahl_spieler = None
anzahl_spieler_event = threading.Event()
lock = threading.Lock()

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
    global anzahl_spieler

    try:
        # Spieler-ID senden
        send_data(conn, {"spieler_id": spieler_id + 1})

        if spieler_id == 0:
            daten = recv_data(conn)
            if daten:
                anzahl_spieler = daten.get("anzahl_spieler", 2)
                print(f"[INFO] Anzahl der Spieler festgelegt auf {anzahl_spieler}")
                anzahl_spieler_event.set()
        else:
            anzahl_spieler_event.wait()

        daten = recv_data(conn)
        if daten:
            name = daten.get("name", f"Spieler{spieler_id + 1}")
            with lock:
                spieler_daten[spieler_id + 1] = name
            print(f"[INFO] Spieler {spieler_id + 1} heißt {name}")

        # Allen Spielern "Warten..." senden
        if spieler_id < anzahl_spieler - 1:
            send_data(conn, {"message": "Warten auf andere Spieler..."})

        # Wenn alle verbunden, allen Startmeldung schicken
        if spieler_id == anzahl_spieler - 1:
            print("[INFO] Alle Spieler verbunden, sende Startnachricht...")
            for v in verbindungen:
                send_data(v, {"message": "Alle Spieler verbunden. Ihr könnt jetzt starten!"})

        # Hier könntest du später die Spiellogik oder weitere Kommunikation einbauen
        while True:
            # Server wartet z.B. auf weitere Daten, verarbeitet sie ...
            # Oder hält Verbindung offen
            pass

    except Exception as e:
        print(f"[FEHLER] Spieler {spieler_id + 1} Verbindung verloren: {e}")

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

        if anzahl_spieler is not None and spieler_id >= anzahl_spieler:
            send_data(conn, {"error": "Maximale Spieleranzahl erreicht. Verbindung abgelehnt."})
            conn.close()
            continue

        print(f"[VERBUNDEN] Spieler {spieler_id + 1} von {addr}")
        verbindungen.append(conn)
        thread = threading.Thread(target=client_thread, args=(conn, spieler_id), daemon=True)
        thread.start()

        spieler_id += 1

        if anzahl_spieler is not None and spieler_id >= anzahl_spieler:
            print("[INFO] Alle Spieler verbunden, das Spiel kann starten.")
            # Warten auf Threads ist hier nicht nötig, da server läuft weiter

if __name__ == "__main__":
    start_server()
