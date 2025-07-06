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
        # Wichtig: Höheres Timeout für bessere Nachrichtenverarbeitung
        sock.settimeout(0.1)  # 100ms Timeout statt non-blocking
        
        # Mehrere Nachrichten in einer Schleife verarbeiten!
        while True:
            try:
                msg = serv.recv_data(sock)
                if not msg:
                    break
                
                # WICHTIG: Detailliertere Debug-Ausgabe
                print(f"[DEBUG] Client empfängt Nachricht vom Typ: {msg.get('update', 'unknown')}")
                if msg.get('update') == "triplet_removed":
                    print(f"[DEBUG] !! TRIPLET NACHRICHT EMPFANGEN !!: {msg}")
                
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
                    print("[DEBUG] Spiel gestartet!")
                    s.status_message = "Decke zwei Karten auf"
                
                # Andere Nachrichten behandeln
                elif msg.get("update") == "karte_aufgedeckt":
                    spieler = msg["spieler"]
                    row = msg["karte"]["row"]
                    col = msg["karte"]["col"]
                    layout = cP.player_cardlayouts.get(spieler)
                    if layout:
                        card = layout.cards[row][col]
                        card.flip()
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
                    
                    # Ablagestapel aktualisieren
                    s.discard_card = ablagestapel
                    
                    # NEUE ZEILEN: Ablagestapel-Array korrekt aktualisieren
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
                
                elif "message" in msg:
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
                    layout = cP.player_cardlayouts.get(spieler)
                    if layout:
                        for row in range(len(layout.cards)):
                            if row < len(layout.cards) and col < len(layout.cards[row]):
                                card = layout.cards[row][col]
                                card.removed = True
                                card.is_face_up = True
                                print(f"[DEBUG] Karte ({row},{col}) als entfernt markiert")
                    
                    # Keine UI-Anzeige mehr
                    print(f"[DEBUG] Dreierkombination entfernt: Spieler {spieler}, Spalte {col}")
                    
            except (BlockingIOError, ConnectionError, TimeoutError):
                break
    finally:
        sock.setblocking(True)
