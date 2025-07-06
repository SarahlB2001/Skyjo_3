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
    sock.connect((SERVER_IP, PORT))

    data = serv.recv_data(sock)
    if data and "error" in data:
        print("[SERVER]:", data["error"])
        sock.close()
        sys.exit()

    spieler_id = data["spieler_id"]
    print(f"[INFO] Verbunden als Spieler {spieler_id}")
    return sock, spieler_id

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
        sock.setblocking(False)
        # Mehrere Nachrichten in einer Schleife verarbeiten!
        while True:
            try:
                msg = serv.recv_data(sock)
                if not msg:
                    break
                
                print(f"[DEBUG] Client empfängt Nachricht: {msg}")
                
                # Startnachricht behandeln
                if "message" in msg and ("startet" in msg["message"].lower() or "starten" in msg["message"].lower()):
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
                    cP.card_set_positions(screen)
                    s.waiting_for_start = False
                    s.game_started = True
                    s.setup_phase = True  # Explizit den Setup-Modus aktivieren
                    s.cards_flipped_this_turn = 0  # Zähler zurücksetzen
                    print("[DEBUG] Spiel gestartet! Setup-Modus aktiviert.")
                    s.status_message = "Decke zwei Karten auf"
                
                # Andere Nachrichten behandeln
                elif msg.get("update") == "karte_aufgedeckt":
                    spieler = msg["spieler"]
                    row = msg["karte"]["row"]
                    col = msg["karte"]["col"]
                    print(f"[DEBUG] Nachricht karte_aufgedeckt empfangen: Spieler {spieler}, Reihe {row}, Spalte {col}")
                    
                    layout = cP.player_cardlayouts.get(spieler)
                    if layout:
                        if row < len(layout.cards) and col < len(layout.cards[0]):
                            card = layout.cards[row][col]
                            print(f"[DEBUG] Karte vor flip(): is_face_up={card.is_face_up}")
                            card.is_face_up = True  # Direkt setzen statt flip() aufrufen
                            print(f"[DEBUG] Karte nach Setzen: is_face_up={card.is_face_up}")
                        else:
                            print(f"[DEBUG] Ungültige Kartenindizes: {row}, {col}")
                    else:
                        print(f"[DEBUG] Layout für Spieler {spieler} nicht gefunden")
                        
                    if hasattr(s, "aufgedeckt_matrizen"):
                        s.aufgedeckt_matrizen[spieler][row][col] = True
                
                elif msg.get("update") == "spielreihenfolge":
                    s.spielreihenfolge = msg["reihenfolge"]
                    s.scores = msg["scores"]
                    s.current_player = s.spielreihenfolge[0]
                    s.setup_phase = False
                    
                    current_player_name = s.player_data.get(s.current_player, f"Spieler{s.current_player}")
                    s.status_message = f"{current_player_name} ist am Zug"
                    
                    print(f"[DEBUG] Current player gesetzt auf: {s.current_player}")
                    reihenfolge_namen = [s.player_data.get(pid, f"Spieler{pid}") for pid in s.spielreihenfolge]
                    print("Spielreihenfolge (Namen):", reihenfolge_namen)
                    print(f"Startspieler: {s.player_data.get(s.current_player, f'Spieler{s.current_player}')}")
                
                elif msg.get("update") == "nachziehstapel_karte":
                    s.gezogene_karte = msg["karte"]
                    s.status_message = "Tausche mit Karte auf Spielfeld"
                
                elif msg.get("update") == "karten_getauscht":
                    spieler = msg["spieler"]
                    row = msg["karte"]["row"]
                    col = msg["karte"]["col"]
                    neue_karte = msg["neue_karte"]
                    ablagestapel = msg["ablagestapel"]
                    
                    layout = cP.player_cardlayouts.get(spieler)
                    if layout:
                        card = layout.cards[row][col]
                        card.value = neue_karte
                        card.front_image = pygame.transform.scale(pygame.image.load(f"Karten_png/card_{neue_karte}.png"), (s.CARD_WIDTH, s.CARD_HEIGHT))
                        card.is_face_up = True
                    
                    s.discard_card = ablagestapel
                
                elif msg.get("update") == "karte_abgelehnt":
                    spieler = msg["spieler"]
                    row = msg["aufgedeckte_karte"]["row"]
                    col = msg["aufgedeckte_karte"]["col"]
                    ablagestapel = msg["ablagestapel"]
                    
                    layout = cP.player_cardlayouts.get(spieler)
                    if layout:
                        card = layout.cards[row][col]
                        card.is_face_up = True
                    
                    s.discard_card = ablagestapel
                
                elif msg.get("update") == "naechster_spieler":
                    print(f"[DEBUG] WICHTIG! Nachricht 'naechster_spieler' empfangen: {msg}")
                    old_player = s.current_player
                    s.current_player = msg["spieler"]
                    s.zug_begonnen = False
                    
                    current_player_name = s.player_data.get(s.current_player, f"Spieler{s.current_player}")
                    s.status_message = f"{current_player_name} ist am Zug"
                    
                    print(f"[DEBUG] WICHTIG! Spielerwechsel von {old_player} zu {s.current_player}")
                
                elif msg.get("update") == "spalte_entfernt":
                    spieler = msg["spieler"]
                    entfernte_karten = msg["entfernte_karten"]
                    ablagestapel = msg["ablagestapel"]
                    
                    # Karten im lokalen Layout "entfernen"
                    layout = cP.player_cardlayouts.get(spieler)
                    if layout:
                        for karte in entfernte_karten:
                            row, col = karte["row"], karte["col"]
                            value = karte["value"]  # Originaler Wert der Karte
                            if row < len(layout.cards) and col < len(layout.cards[0]):
                                # Karte als "entfernt" markieren, aber Wert beibehalten
                                card = layout.cards[row][col]
                                card.is_removed = True  # Markieren als entfernt
    
                    # Ablagestapel aktualisieren
                    s.discard_card = ablagestapel
                
                elif "message" in msg:
                    s.status_message = msg["message"]
                
                elif msg.get("update") == "test":
                    print(f"[DEBUG] Test-Nachricht empfangen: {msg}")
                
                # Neue Nachrichten für Rundenende und -wechsel
                elif msg.get("update") == "round_end_started":
                    trigger_player = msg["trigger_player"]
                    trigger_name = s.player_data.get(trigger_player, f"Spieler {trigger_player}")
                    s.status_message = f"{trigger_name} hat alle Karten aufgedeckt! Letzter Zug für alle anderen Spieler."
                    
                    # Wichtig: Sicherstellen, dass der Rundenendzustand korrekt gesetzt wird
                    s.round_ending = True
                    s.round_end_trigger = trigger_player
                    
                    # Zurücksetzen von zug_begonnen für alle Spieler
                    s.zug_begonnen = False
                    if hasattr(s, "cards_flipped_this_turn"):
                        s.cards_flipped_this_turn = 0
                        
                    print(f"[DEBUG] Rundenende gestartet! Auslöser: {trigger_name}")

                elif msg.get("update") == "round_end":
                    final_scores = msg["final_scores"]
                    trigger_player = msg["trigger_player"]
                    doubled = msg["doubled"]
                    current_round = msg["current_round"]
                    total_rounds = msg["total_rounds"]
                    total_scores = msg["total_scores"]
                    round_scores = msg["round_scores"]
                    game_over = msg["game_over"]
                    
                    # Daten im Settings speichern
                    s.final_scores = final_scores
                    s.current_round = current_round
                    s.total_rounds = total_rounds
                    s.total_scores = total_scores
                    s.round_scores = round_scores
                    
                    # Status-Nachricht festlegen
                    trigger_name = s.player_data.get(trigger_player, f"Spieler {trigger_player}")
                    if doubled:
                        s.status_message = f"Rundenende! {trigger_name} hat nicht die niedrigste Punktzahl und bekommt doppelte Punkte!"
                    else:
                        s.status_message = f"Rundenende! {trigger_name} hat die niedrigste Punktzahl."
                    
                    # Spiel- oder Rundenende-Modus aktivieren
                    if game_over:
                        s.game_over = True
                        s.status_message = "Spiel beendet! Gesamtergebnis wird angezeigt."
                    else:
                        s.round_ending = False
                        s.between_rounds = True

                elif msg.get("update") == "new_round":
                    current_round = msg["current_round"]
                    total_rounds = msg["total_rounds"]
                    karten_matrizen = msg["karten_matrizen"]
                    aufgedeckt_matrizen = msg["aufgedeckt_matrizen"]
                    discard_card = msg["discard_card"]
                    current_player = msg["current_player"]
                    
                    # Daten im Settings speichern
                    s.current_round = current_round
                    s.total_rounds = total_rounds
                    s.karten_matrizen = karten_matrizen
                    s.aufgedeckt_matrizen = aufgedeckt_matrizen
                    s.discard_card = discard_card
                    s.current_player = current_player
                    
                    # Status-Nachricht festlegen
                    s.status_message = f"Neue Runde beginnt! (Runde {current_round}/{total_rounds})"
                    
                    # Spielerlayouts neu erstellen
                    cP.card_set_positions(screen)
                    
                    # Zwischen-Runden-Modus deaktivieren
                    s.between_rounds = False
                    s.cards_flipped_this_turn = 0
                
            except (BlockingIOError, ConnectionError):
                break
    finally:
        sock.setblocking(True)
