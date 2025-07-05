import socket
import threading
import pickle
import settings as s
import time
import random

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
                s.player_count = daten.get("anzahl_spieler", 2)  # <-- Nur noch player_count!
                print(f"[INFO] Anzahl der Spieler festgelegt auf {s.player_count}")
                s.player_count_event.set()

            daten = recv_data(conn)
            if daten:
                name = daten.get("name", f"Spieler{spieler_id +1}")
                with s.lock:
                    s.player_data[spieler_id + 1] = name
                print(f"[INFO] Spieler {spieler_id +1} heißt {name}")

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

        if spieler_id == s.player_count - 1:
            print("[INFO] Alle Spieler verbunden, sende Startnachricht...")

            # Kartenmatrizen für alle Spieler erzeugen
            karten_matrizen = {}
            for pid in range(1, s.player_count + 1):
                matrix = []
                for row in range(s.ROWS):
                    matrix.append([random.randint(-2, 12) for _ in range(s.COLS)])
                karten_matrizen[pid] = matrix
            s.karten_matrizen = karten_matrizen  # Optional: global speichern

            aufgedeckt_matrizen = {}
            for pid in range(1, s.player_count + 1):
                aufgedeckt_matrizen[pid] = [[False for _ in range(s.COLS)] for _ in range(s.ROWS)]
            s.aufgedeckt_matrizen = aufgedeckt_matrizen

            for v in s.connection:
                send_data(v, {
                    "message": "Alle Spieler verbunden. Ihr könnt jetzt starten!",
                    "anzahl_spieler": s.player_count,
                    "spielernamen": s.player_data,
                    "karten_matrizen": karten_matrizen  # <--- Kartenmatrizen mitsenden!
                })
            print(f"[DEBUG] Startnachricht gesendet, Spieleranzahl: {s.player_count}")

            # Nach dem Senden der Startnachricht an alle Spieler:


        # Hier könntest du später die Spiellogik oder weitere Kommunikation einbauen
        while True:
            daten = recv_data(conn)
            if daten:
                if daten.get("aktion") == "karte_aufdecken":
                    spieler_id = daten["spieler_id"]
                    karte = daten["karte"]
                    s.aufgedeckt_matrizen[spieler_id][karte["row"]][karte["col"]] = True  # Karte als aufgedeckt markieren
                    for v in s.connection:
                        send_data(v, {
                            "update": "karte_aufgedeckt",
                            "spieler": spieler_id,
                            "karte": karte
                        })
                    # Nach dem Aufdecken einer Karte:
                    if not hasattr(s, "cards_flipped"):
                        s.cards_flipped = {}
                    s.cards_flipped[spieler_id] = s.cards_flipped.get(spieler_id, 0) + 1

                    print(f"[DEBUG] Spieler {spieler_id} hat Karte ({karte['row']}, {karte['col']}) aufgedeckt.")
                    print(f"[DEBUG] Aufgedeckte Kartenmatrix für Spieler {spieler_id}: {s.aufgedeckt_matrizen[spieler_id]}")

                    # Prüfen, ob alle Spieler 2 Karten aufgedeckt haben
                    if all(s.cards_flipped.get(pid, 0) >= 2 for pid in range(1, s.player_count + 1)):
                        # Punktzahlen berechnen
                        scores = {}
                        for pid in range(1, s.player_count + 1):
                            matrix = s.karten_matrizen[pid]
                            aufgedeckt_matrix = s.aufgedeckt_matrizen[pid]
                            scores[pid] = berechne_punktzahl(matrix, aufgedeckt_matrix)

                        # Spieler mit höchster Punktzahl bestimmen
                        startspieler = max(scores, key=scores.get)

                        # Sitzordnung (IDs in der Reihenfolge, wie sie im Kreis sitzen)
                        sitzordnung = list(range(1, s.player_count + 1))
                        start_idx = sitzordnung.index(startspieler)
                        reihenfolge = sitzordnung[start_idx:] + sitzordnung[:start_idx]

                        print("Spielreihenfolge:", reihenfolge)
                        print("Scores:", scores)
                        for v in s.connection:
                            send_data(v, {"update": "spielreihenfolge", "reihenfolge": reihenfolge, "scores": scores})
                            print(f"[DEBUG] Punktzahlen für Spieler {pid}: {scores[pid]}")
            else:
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

def berechne_punktzahl(matrix, aufgedeckt_matrix):
    punkte = 0
    for row in range(len(matrix)):
        for col in range(len(matrix[0])):
            if aufgedeckt_matrix[row][col]:
                punkte += matrix[row][col]
    return punkte

if __name__ == "__main__":
    start_server()