import socket
import threading
import pickle
import settings as s
import time

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
        send_data(conn, {"spieler_id": spieler_id + 1})

        if spieler_id == 0:
            daten = recv_data(conn)
            if daten:
                s.player_count = daten.get("anzahl_spieler", 2)
                print(f"[INFO] Anzahl der Spieler festgelegt auf {s.player_count}")
                s.player_count_event.set()
        else:
            s.player_count_event.wait()

        daten = recv_data(conn)
        if daten:
            name = daten.get("name", f"Spieler{spieler_id + 1}")
            with s.lock:
                s.player_data[spieler_id + 1] = name
            print(f"[INFO] Spieler {spieler_id + 1} heißt {name}")

        # Allen Spielern "Warten..." senden
        if spieler_id < s.player_count - 1:
            send_data(conn, {"message": "Warten auf andere Spieler..."})

        # Wenn alle verbunden, allen Startmeldung schicken
        if spieler_id == s.player_count - 1:
            print("[INFO] Alle Spieler verbunden, sende Startnachricht...")
            for v in s.connection:
                send_data(v, {"message": "Alle Spieler verbunden. Ihr könnt jetzt starten!"})

        # Hier könntest du später die Spiellogik oder weitere Kommunikation einbauen
        while True:
            daten = recv_data(conn)
            if daten:
                # Beispiel: Spieler macht einen Zug
                if daten.get("aktion") == "karte_aufdecken":
                    # Spiellogik ausführen, z.B. Karte aufdecken
                    # Dann allen Spielern neuen Zustand schicken
                    for v in s.connection:
                        send_data(v, {
                            "update": "karte_aufgedeckt",
                            "spieler": spieler_id + 1,
                            "karte": daten["karte"]
                        })
                # Weitere Aktionen hier behandeln
            else:
                # Verbindung verloren
                break

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

        if s.player_count is not None and spieler_id >= s.player_count:
            send_data(conn, {"error": "Maximale Spieleranzahl erreicht. Verbindung abgelehnt."})
            conn.close()
            continue

        print(f"[VERBUNDEN] Spieler {spieler_id + 1} von {addr}")
        s.connection.append(conn)
        thread = threading.Thread(target=client_thread, args=(conn, spieler_id), daemon=True)
        thread.start()

        spieler_id += 1

        if s.player_count is not None and spieler_id >= s.player_count:
            print("[INFO] Alle Spieler verbunden, das Spiel kann starten.")
            # Warten auf Threads ist hier nicht nötig, da server läuft weiter

if __name__ == "__main__":
    start_server()