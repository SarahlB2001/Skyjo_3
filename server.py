import socket
import threading
import pickle
import pygame

# Server-Daten
spieler_daten = {}
verbindungen = []
anzahl_spieler = None  # Wird vom ersten Spieler gesetzt
anzahl_spieler_event = threading.Event()  # Synchronisation
lock = threading.Lock()

def client_thread(conn, spieler_id):
    global anzahl_spieler

    try:
        # Sende die Spieler-ID an den Client
        conn.sendall(pickle.dumps({"spieler_id": spieler_id + 1}))

        if spieler_id == 0:
            # Erster Spieler gibt die gewünschte Spielerzahl an
            daten = recv_data(conn)
            if daten:
                anzahl_spieler = daten.get("anzahl_spieler", 2)
                print(f"[INFO] Anzahl der Spieler festgelegt auf {anzahl_spieler}")
                anzahl_spieler_event.set()  # Anderen Threads Bescheid geben
        else:
            # Andere Spieler warten, bis Anzahl festgelegt wurde
            anzahl_spieler_event.wait()

        # Spielername empfangen
        daten = recv_data(conn)
        if daten:
            name = daten.get("name", f"Spieler{spieler_id + 1}")
            with lock:
                spieler_daten[spieler_id + 1] = name
            print(f"[INFO] Spieler {spieler_id + 1} heißt {name}")

        # Falls noch nicht alle Spieler verbunden sind, warten
        if spieler_id < anzahl_spieler - 1:
            send_data(conn, {"message": "Warten auf andere Spieler..."})

        # Wenn der letzte Spieler erreicht ist, starte das Spiel
        if spieler_id == anzahl_spieler - 1:
            # Allen Spielern die Start-Nachricht schicken
            for v in verbindungen:
                send_data(v, {"message": "Alle Spieler verbunden. Ihr könnt jetzt starten!"})

    except Exception as e:
        print(f"[FEHLER] Spieler {spieler_id + 1} Verbindung verloren: {e}")

    finally:
        conn.close()
        print(f"[TRENNUNG] Spieler {spieler_id + 1} getrennt")

def recv_data(conn):
    """Hilfsfunktion für sicheres Empfangen von Daten"""
    try:
        data = conn.recv(4096)
        if data:
            return pickle.loads(data)
    except (EOFError, pickle.UnpicklingError, ConnectionResetError):
        return None
    return None

def send_data(conn, data):
    """Hilfsfunktion für das Senden von Daten"""
    try:
        conn.sendall(pickle.dumps(data))
    except:
        pass

def start_server():
    HOST = "0.0.0.0"
    PORT = 65432
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((HOST, PORT))
    server.listen(8)

    print(f"[SERVER] Server läuft auf {HOST}:{PORT}")

    spieler_id = 0
    threads = []

    while True:
        conn, addr = server.accept()

        # Warte, bis anzahl_spieler gesetzt ist (nachdem Spieler 1 gewählt hat)
        if anzahl_spieler is not None and spieler_id >= anzahl_spieler:
            send_data(conn, {"error": "Maximale Spieleranzahl erreicht. Verbindung abgelehnt."})
            conn.close()
            continue

        print(f"[VERBUNDEN] Spieler {spieler_id + 1} von {addr}")
        verbindungen.append(conn)
        thread = threading.Thread(target=client_thread, args=(conn, spieler_id))
        thread.start()
        threads.append(thread)

        spieler_id += 1

        # Nur prüfen, wenn anzahl_spieler gesetzt ist!
        if anzahl_spieler is not None and spieler_id >= anzahl_spieler:
            print("[INFO] Alle Spieler verbunden, das Spiel kann starten.")
            break

    # Optional: Warten bis alle Threads fertig sind
    for t in threads:
        t.join()

    server.close()

if __name__ == "__main__":
    start_server()
