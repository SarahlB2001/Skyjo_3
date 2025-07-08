import socket
import threading
import pickle
import settings as s
import time
from entities import serv_gameprocess as sgp

def recv_data(conn):
    try:
        data = conn.recv(4096)
        if data:
            return pickle.loads(data)
    except (EOFError, pickle.UnpicklingError, ConnectionResetError, TimeoutError):
        # Added TimeoutError to the exception list
        return None
    except BlockingIOError:
        # Diese Exception explizit behandeln für non-blocking sockets
        return None
    return None

def send_data(conn, data):
    try:
        serialized = pickle.dumps(data)
        conn.sendall(serialized)
        return True
    except Exception as e:
        print(f"[ERROR] Fehler beim Senden: {e}, Daten: {data}")
        return False

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

            # Kartenmatrizen und Aufgedeckt-Matrizen erzeugen (aus serv_gameprocess)
            karten_matrizen = sgp.create_card_matrices(s.player_count, s.ROWS, s.COLS)
            s.karten_matrizen = karten_matrizen

            aufgedeckt_matrizen = sgp.create_flipped_matrices(s.player_count, s.ROWS, s.COLS)
            s.aufgedeckt_matrizen = aufgedeckt_matrizen

            # Erzeuge eine Karte für den Ablagestapel
            discard_card_value = sgp.draw_card_from_deck()
            s.discard_card = discard_card_value

            for v in s.connection:
                send_data(v, {
                    "message": "Alle Spieler verbunden. Ihr könnt jetzt starten!",
                    "anzahl_spieler": s.player_count,
                    "spielernamen": s.player_data,
                    "karten_matrizen": karten_matrizen,
                    "aufgedeckt_matrizen": aufgedeckt_matrizen,
                    "discard_card": discard_card_value
                })
            print(f"[DEBUG] Startnachricht gesendet, Spieleranzahl: {s.player_count}")

        # Hauptspielschleife
        while True:
            daten = recv_data(conn)
            if daten:
                if daten.get("aktion") == "karte_aufdecken":
                    # Karte aufdecken
                    spieler_id, karte = sgp.handle_card_flip(daten, s.connection, send_data)

                    print(f"[DEBUG] Spieler {spieler_id} hat Karte ({karte['row']}, {karte['col']}) aufgedeckt.")
                    print(f"[DEBUG] Aufgedeckte Kartenmatrix für Spieler {spieler_id}: {s.aufgedeckt_matrizen[spieler_id]}")

                    # Prüfen, ob alle Spieler 2 Karten aufgedeckt haben
                    if sgp.check_if_setup_complete(s.player_count, s.cards_flipped, s.connection, send_data):
                        print(f"[DEBUG] Setup abgeschlossen. Spielreihenfolge: {s.spielreihenfolge}")

                elif daten.get("aktion") == "nehme_ablagestapel":
                    # Karte vom Ablagestapel nehmen
                    spieler_id, discard_card = sgp.handle_take_discard_pile(daten, s.connection, send_data)

                    # Pause für Verarbeitung
                    time.sleep(0.1)

                    # Nächster Spieler
                    next_player = sgp.update_next_player(spieler_id, s.connection, send_data)
                    print(f"[DEBUG] Nächster Spieler: {next_player}")

                elif daten.get("aktion") == "nehme_nachziehstapel":
                    # Karte vom Nachziehstapel nehmen
                    spieler_id, neue_karte = sgp.handle_take_draw_pile(daten, s.connection, send_data)
                    print(f"[DEBUG] Spieler {spieler_id} hat Karte {neue_karte} vom Nachziehstapel gezogen")

                elif daten.get("aktion") == "nachziehstapel_tauschen":
                    # Mit gezogener Karte tauschen
                    spieler_id, alte_karte = sgp.handle_swap_with_draw_pile(daten, s.connection, send_data)

                    # Pause für Verarbeitung
                    time.sleep(0.1)

                    # Nächster Spieler
                    next_player = sgp.update_next_player(spieler_id, s.connection, send_data)
                    print(f"[DEBUG] Nächster Spieler: {next_player}")

                elif daten.get("aktion") == "nachziehstapel_ablehnen":
                    # Gezogene Karte ablehnen
                    spieler_id = sgp.handle_reject_draw_pile(daten, s.connection, send_data)

                    # Pause für Verarbeitung
                    time.sleep(0.1)

                    # Nächster Spieler
                    next_player = sgp.update_next_player(spieler_id, s.connection, send_data)
                    print(f"[DEBUG] Nächster Spieler: {next_player}")
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

    # Initialisiere Zieh- und Ablagestapel
    s.draw_pile = []
    s.discard_pile = []

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

             #WICHTIG: Hier game_loop in neuem Thread starten
            if spieler_id == 0:  # Nur bei Host
                 game_thread = threading.Thread(target=game_loop, daemon=True)
                 game_thread.start()

def game_loop():
    for aktuelle_runde in range(1, s.round_count + 1):
        # --- Statusvariablen für neue Runde zurücksetzen ---
        s.runde_beendet = False
        s.round_end_triggered = False
        s.round_end_trigger_player = None
        s.cards_flipped = {}
        s.removed_cards = {}
        s.scores = {}
        s.current_player = None
        s.setup_phase = True
        s.zug_begonnen = False
        # ---------------------------------------------------

        print(f"[INFO] Starte Runde {aktuelle_runde} von {s.round_count}")

        # 1. Matrizen zurücksetzen
        s.karten_matrizen = sgp.create_card_matrices(s.player_count, s.ROWS, s.COLS)
        s.aufgedeckt_matrizen = sgp.create_flipped_matrices(s.player_count, s.ROWS, s.COLS)

        # 2. Allen Spielern den neuen Rundenstart mitteilen
        for v in s.connection:
            send_data(v, {
                "update": "runde_start",
                "runde": aktuelle_runde,
                "gesamt_runden": s.round_count,
                "karten_matrizen": s.karten_matrizen,
                "aufgedeckt_matrizen": s.aufgedeckt_matrizen,
                "discard_card": sgp.draw_card_from_deck()
            })

        # 3. Warten bis Rundenende
        s.runde_beendet = False
        while not s.runde_beendet:
            time.sleep(0.5)

    print("[INFO] Alle Runden gespielt! Spiel vorbei.")

if __name__ == "__main__":
    start_server()
