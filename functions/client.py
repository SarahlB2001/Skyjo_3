"""
Dieses Modul enthält die Client-Funktionen für das Skyjo-Spiel.
Es stellt die Verbindung zum Server her, empfängt und verarbeitet Nachrichten,
und verwaltet die Kommunikation sowie die Spiellogik auf der Client-Seite.
Enthalten sind Funktionen für die Netzwerkverbindung, das Empfangen von Daten,
das Verarbeiten von Server-Nachrichten und Hilfsfunktionen wie die lokale IP-Ermittlung.
"""
import socket
import sys
import server as serv
import pickle
import settings as s
import pygame
from dictionaries import cardSetPosition as cP

def recv_loop(sock, message_queue):
    """Läuft in separatem Thread, um Nachrichten dauerhaft zu empfangen"""
    while True:
        try:
            data = serv.recv_data(sock)
            if data is None:
                print("[INFO] Verbindung zum Server verloren.")
                break
            message_queue.append(data)
        except Exception as e:
            print(f"[FEHLER] Empfang fehlgeschlagen: {e}")
            break

def connect_to_server(SERVER_IP="127.0.0.1"):
    PORT = 65432
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        # Timeout hinzufügen gegen Hängenbleiben
        sock.settimeout(5.0)
        sock.connect((SERVER_IP, PORT))

        data = serv.recv_data(sock)
        if data and "error" in data:
            sock.close()
            raise ConnectionError(data["error"])

        spieler_id = data["spieler_id"]
        return sock, spieler_id

    except socket.gaierror:
        raise ConnectionError("Ungültige IP-Adresse")
    except socket.timeout:
        raise ConnectionError("Zeitüberschreitung beim Verbindungsversuch")
    except ConnectionRefusedError:
        raise ConnectionError("Verbindung verweigert - Server nicht erreichbar")
    except Exception as e:
        raise ConnectionError(f"Verbindungsfehler: {str(e)}")

def get_local_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
    except Exception:
        ip = "127.0.0.1"
    finally:
        s.close()
    return ip

# Ergänze die recv_data Funktion:

def recv_data(conn):
    try:
        data = conn.recv(4096)
        if data:
            return pickle.loads(data)
    except (EOFError, pickle.UnpicklingError, ConnectionResetError):
        return None
    except BlockingIOError:
        # Diese Exception explizit behandeln für non-blocking sockets
        return None
    return None

def process_messages(sock, screen):
    """Verarbeitet alle eingehenden Nachrichten vom Server"""
    if not sock:
        return

    try:
        sock.settimeout(0.3)
        while True:
            try:
                msg = serv.recv_data(sock)
                if not msg:
                    break  # verlässt nur die innere while, nicht die Funktion!

                if msg.get("update") == "game_ended":
                    s.status_message = msg["message"]
                    s.game_over = True
                    s.game_ended_time = pygame.time.get_ticks()
                    s.podium_shown = False  # Damit das Podium wieder angezeigt wird
                    continue
                # HIER ist die richtige Stelle:
                if hasattr(s, "game_ended_time") and msg.get("update") != "game_ended":
                    continue # oder: continue, wenn du die Schleife weiterlaufen lassen willst

                # WICHTIG: Detailliertere Debug-Ausgabe
                print(f"[DEBUG] Client empfängt Nachricht vom Typ: {msg.get('update', 'unknown')}")
                if msg.get('update') == "triplet_removed":
                    print(f"[DEBUG] !! TRIPLET NACHRICHT EMPFANGEN !!: {msg}")

                if msg.get("update") == "new_round_starting":
                    s.status_message = msg["message"]
                    if "karten_matrizen" in msg:
                        s.karten_matrizen = msg["karten_matrizen"]
                    if "aufgedeckt_matrizen" in msg:
                        s.aufgedeckt_matrizen = msg["aufgedeckt_matrizen"]
                    if "discard_card" in msg:
                        s.discard_card = msg["discard_card"]
                    if "current_round" in msg:
                        s.current_round = msg["current_round"]
                    if "round_count" in msg:
                        s.round_count = msg["round_count"]
                    print(f"[DEBUG] Neue Runde: {s.current_round}/{s.round_count}")
                    if hasattr(s, "final_round_scores"):
                       del s.final_round_scores
                    # Layouts wirklich neu erzeugen
                    s.player_cardlayouts = {}
                    cP.card_set_positions(screen)
                    # --- Kartenstatus synchronisieren ---
                    for pid, layout in s.player_cardlayouts.items():
                        if hasattr(s, "aufgedeckt_matrizen") and pid in s.aufgedeckt_matrizen:
                            aufgedeckt = s.aufgedeckt_matrizen[pid]
                            for row_idx, row in enumerate(layout.cards):
                                for col_idx, card in enumerate(row):
                                    card.is_face_up = aufgedeckt[row_idx][col_idx]
                                    card.removed = False
                    # Statusvariablen zurücksetzen
                    s.setup_phase = True
                    s.cards_flipped_this_turn = 0
                    for pid in s.player_data: #
                     s.cards_flipped[pid] = 0 #
                    s.waiting_for_start = False
                    s.zug_begonnen = False
                    s.gezogene_karte = None
                    s.muss_karte_aufdecken = False
                    s.tausche_mit_ablagestapel = False
                    s.warte_auf_entscheidung = False
                    s.round_end_triggered = False
                    s.round_end_trigger_player = None
                    s.current_player = None
                    if hasattr(s, "points_calculated_time"):
                        del s.points_calculated_time
                    s.status_message = "Decke zwei Karten auf"

                # Startnachricht behandeln
                elif "message" in msg and ("startet" in msg["message"].lower() or "starten" in msg["message"].lower()):
                    s.status_message = msg["message"]
                    if "spielernamen" in msg:
                        s.player_data = {int(k): v for k, v in msg["spielernamen"].items()}
                    if "anzahl_spieler" in msg:
                        s.player_count = int(msg["anzahl_spieler"])
                    if "karten_matrizen" in msg:
                        s.karten_matrizen = msg["karten_matrizen"]
                    if "aufgedeckt_matrizen" in msg:
                        s.aufgedeckt_matrizen = msg["aufgedeckt_matrizen"]
                    if "discard_card" in msg:
                        s.discard_card = msg["discard_card"]
                    if "current_round" in msg and msg["current_round"] is not None:
                        s.current_round = msg["current_round"]
                    if "round_count" in msg and msg["round_count"] is not None:
                        s.round_count = msg["round_count"]
                    cP.card_set_positions(screen)
                    for pid, layout in s.player_cardlayouts.items():
                        if hasattr(s, "aufgedeckt_matrizen") and pid in s.aufgedeckt_matrizen:
                            aufgedeckt = s.aufgedeckt_matrizen[pid]
                            for row_idx, row in enumerate(layout.cards):
                                for col_idx, card in enumerate(row):
                                    card.is_face_up = aufgedeckt[row_idx][col_idx]
                                    card.removed = False
                    s.waiting_for_start = False
                    s.game_started = True
                    print("[DEBUG] Spiel gestartet!")
                    s.status_message = "Decke zwei Karten auf"


                # Andere Nachrichten behandeln
                elif msg.get("update") == "karte_aufgedeckt":
                    spieler = msg["spieler"]
                    row = msg["karte"]["row"]
                    col = msg["karte"]["col"]
                    layout = s.player_cardlayouts.get(spieler)
                    if layout:
                        card = layout.cards[row][col]
                        card.is_face_up = True
                    if hasattr(s, "aufgedeckt_matrizen"):
                        s.aufgedeckt_matrizen[spieler][row][col] = True

                elif msg.get("update") == "spielreihenfolge":
                    if hasattr(s, "game_ended_time"):
                        return
                    s.spielreihenfolge = msg["reihenfolge"]
                    s.scores = msg["scores"]
                    s.setup_phase = False
                    s.current_player = s.spielreihenfolge[0]
                    current_player_name = s.player_data.get(s.current_player, f"Spieler{s.current_player}")  # <--- Diese Zeile ergänzen!
                    s.status_message = f"{current_player_name} ist am Zug"


                elif msg.get("update") == "nachziehstapel_karte":
                    s.gezogene_karte = msg["karte"]
                    s.status_message = "Tausche mit Karte auf Spielfeld"

                elif msg.get("update") == "karten_getauscht":
                    spieler = msg["spieler"]
                    row = msg["karte"]["row"]
                    col = msg["karte"]["col"]
                    neue_karte = msg["neue_karte"]
                    ablagestapel = msg["ablagestapel"]

                    layout = s.player_cardlayouts.get(spieler)
                    if layout:
                        card = layout.cards[row][col]
                        card.value = neue_karte
                        card.front_image = pygame.transform.scale(pygame.image.load(f"Karten_png/card_{neue_karte}.png"), (s.CARD_WIDTH, s.CARD_HEIGHT))
                        card.is_face_up = True

                    # Ablagestapel aktualisieren
                    s.discard_card = ablagestapel

                    # Ablagestapel-Array korrekt aktualisieren
                    if not hasattr(s, "discard_pile"):
                        s.discard_pile = []

                    # Wenn ein Ablagestapel existiert, die oberste Karte entfernen und neue hinzufügen
                    if len(s.discard_pile) > 0:
                        s.discard_pile.pop()
                    s.discard_pile.append(ablagestapel)

                elif msg.get("update") == "karte_abgelehnt":
                    spieler = msg["spieler"]
                    row = msg["aufgedeckte_karte"]["row"]
                    col = msg["aufgedeckte_karte"]["col"]
                    ablagestapel = msg["ablagestapel"]

                    layout = s.player_cardlayouts.get(spieler)
                    if layout:
                        card = layout.cards[row][col]
                        card.is_face_up = True

                    s.discard_card = ablagestapel

                elif msg.get("update") == "naechster_spieler":
                    print(f"[DEBUG] WICHTIG! Nachricht 'naechster_spieler' empfangen: {msg}")
                    if hasattr(s, "game_ended_time"):
                        return
                    old_player = s.current_player
                    s.current_player = msg["spieler"]
                    s.zug_begonnen = False

                    current_player_name = s.player_data.get(s.current_player, f"Spieler{s.current_player}")
                    s.status_message = f"{current_player_name} ist am Zug"

                    print(f"[DEBUG] WICHTIG! Spielerwechsel von {old_player} zu {s.current_player}")

                elif "message" in msg:
                    # Nur anzeigen, wenn das Spiel noch nicht gestartet ist
                    if not getattr(s, "game_started", False) or "warten auf andere spieler" not in msg["message"].lower():
                        s.status_message = msg["message"]

                elif msg.get("update") == "test":
                    print(f"[DEBUG] Test-Nachricht empfangen: {msg}")

                # Im process_messages, nach dem Handler für karte_abgelehnt:
                elif msg.get("update") == "triplet_removed":
                    print(f"[DEBUG] TRIPLET ENTFERNT! Vollständige Nachricht: {msg}")
                    spieler = msg["spieler"]
                    col = msg["col"]

                    # Überprüfen, ob card_values oder card_value in der Nachricht ist
                    if "card_values" in msg:
                        card_values = msg["card_values"]
                    elif "card_value" in msg:
                        card_values = [msg["card_value"]] * 3
                    else:
                        print("[ERROR] Weder card_values noch card_value in der Nachricht gefunden!")
                        card_values = [0, 0, 0]  # Fallback

                    discard_value = msg["discard_value"]

                    # Ablagestapel aktualisieren
                    s.discard_card = discard_value

                    # Karten als entfernt markieren
                    layout = s.player_cardlayouts.get(spieler)
                    if layout:
                        for row in range(len(layout.cards)):
                            if row < len(layout.cards) and col < len(layout.cards[row]):
                                card = layout.cards[row][col]
                                card.removed = True
                                card.is_face_up = True
                                print(f"[DEBUG] Karte ({row},{col}) als entfernt markiert")


                    print(f"[DEBUG] Dreierkombination entfernt: Spieler {spieler}, Spalte {col}")

                elif msg.get("update") == "round_end_triggered":
                    ausloeser = msg["spieler"]
                    s.round_end_triggered = True
                    s.round_end_trigger_player = ausloeser
                    s.status_message = "Rundenende ausgelöst. Alle Spieler haben noch einen Zug!"
                    # Zeit merken, wann die Nachricht angezeigt wurde
                    s.round_end_triggered_time = pygame.time.get_ticks()

                elif msg.get("update") == "round_ended":
                    s.round_end_triggered = False
                    s.round_end_trigger_player = None
                    s.round_ended_time = pygame.time.get_ticks()
                    s.block_until = s.round_ended_time + 4000  # 4 Sekunden blockieren

                elif msg.get("update") == "punkte_aktualisiert":
                    # Wenn gerade "Runde beendet!" angezeigt wird, warte ab
                    if hasattr(s, "block_until") and pygame.time.get_ticks() < s.block_until:

                        return

                    s.scores = msg["scores"]
                    s.last_round_scores = msg["scores"].copy()
                    print("[DEBUG] Punktzahlen empfangen:", msg["scores"])
                    print("[DEBUG] Spieler-ID dieses Clients:", s.spieler_id)

                    if not hasattr(s, "total_scores"):
                     s.total_scores = {}
                    if not hasattr(s, "score_history"):
                        s.score_history = {}
                    for pid, score in msg["scores"].items():
                        pid_key = int(pid)
                        if pid_key not in s.score_history:
                            s.score_history[pid_key] = []
                        s.score_history[pid_key].append(score)

                        if pid_key not in s.total_scores:
                             s.total_scores[pid_key] = 0
                        s.total_scores[pid_key] += score



                    s.final_round_scores = s.scores.copy()
                    s.points_calculated_time = pygame.time.get_ticks()

                    print(f"[DEBUG] Punktzahlen empfangen: {msg['scores']}")
                    print(f"[DEBUG] points_calculated_time gesetzt: {s.points_calculated_time}")

                # Nach dem Handler für "triplet_removed":

                elif msg.get("update") == "triplet_punkte_aktualisiert":
                    # Punktzahlen aktualisieren, aber keine Rundenende-Meldung anzeigen
                    s.scores = msg["scores"]
                    print("[DEBUG] Neue Punktzahlen nach Triplet:", s.scores)
                    s.status_message = "Dreierkombination entfernt. Punkte aktualisiert!"

                elif msg.get("update") == "reveal_all_cards":
                    print("[DEBUG] Nachricht zum Aufdecken aller Karten empfangen")
                    all_cards = msg["all_cards"]
                    for pid_str, cards in all_cards.items():
                        pid = int(pid_str) if isinstance(pid_str, str) else pid_str
                        layout = s.player_cardlayouts.get(pid)
                        if layout:
                            for card_info in cards:
                                row = card_info["row"]
                                col = card_info["col"]
                                card = layout.cards[row][col]
                                card.is_face_up = True
                                # Auch die Aufgedeckt-Matrix aktualisieren
                                if hasattr(s, "aufgedeckt_matrizen"):
                                    s.aufgedeckt_matrizen[pid][row][col] = True
                    s.status_message = "Alle Karten aufgedeckt!"





            except (BlockingIOError, ConnectionError, TimeoutError):
                break
    finally:
        sock.setblocking(True)
