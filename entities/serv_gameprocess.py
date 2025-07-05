"""
Server-side game logic without pygame dependencies
This avoids UI-related imports and window creation
"""
import random
import time
import settings as s

def create_card_matrices(player_count, rows, cols):
    """Erzeugt die Kartenmatrizen für alle Spieler"""
    karten_matrizen = {}
    for pid in range(1, player_count + 1):
        matrix = []
        for row in range(rows):
            matrix.append([random.randint(-2, 12) for _ in range(cols)])
        karten_matrizen[pid] = matrix
    return karten_matrizen

def create_flipped_matrices(player_count, rows, cols):
    """Erzeugt die Matrizen für aufgedeckte Karten"""
    aufgedeckt_matrizen = {}
    for pid in range(1, player_count + 1):
        aufgedeckt_matrizen[pid] = [[False for _ in range(cols)] for _ in range(rows)]
    return aufgedeckt_matrizen

def generate_random_card():
    """Generiert eine zufällige Karte für den Nachziehstapel"""
    return random.randint(-2, 12)

def berechne_punktzahl(matrix, aufgedeckt_matrix):
    """Berechnet die Punktzahl für einen Spieler"""
    punkte = 0
    for row in range(len(matrix)):
        for col in range(len(matrix[0])):
            if aufgedeckt_matrix[row][col]:
                punkte += matrix[row][col]
    return punkte

def calculate_scores(karten_matrizen, aufgedeckt_matrizen):
    """Berechnet die Punktzahl für alle Spieler"""
    scores = {}
    for pid in karten_matrizen.keys():
        matrix = karten_matrizen[pid]
        aufgedeckt_matrix = aufgedeckt_matrizen[pid]
        scores[pid] = berechne_punktzahl(matrix, aufgedeckt_matrix)
    return scores

def determine_starting_player(scores):
    """Bestimmt den Startspieler basierend auf den Punktzahlen"""
    return max(scores, key=scores.get)

def calculate_player_order(starting_player, player_count):
    """Berechnet die Spielreihenfolge"""
    sitzordnung = list(range(1, player_count + 1))
    start_idx = sitzordnung.index(starting_player)
    reihenfolge = sitzordnung[start_idx:] + sitzordnung[:start_idx]
    return reihenfolge

def get_next_player(current_player, spielreihenfolge):
    """Bestimmt den nächsten Spieler in der Reihenfolge"""
    next_idx = (spielreihenfolge.index(current_player) + 1) % len(spielreihenfolge)
    return spielreihenfolge[next_idx]

def handle_card_flip(daten, connection, send_data):
    """Verarbeitet das Aufdecken einer Karte"""
    spieler_id = daten["spieler_id"]
    karte = daten["karte"]
    s.aufgedeckt_matrizen[spieler_id][karte["row"]][karte["col"]] = True
    
    # Allen Clients mitteilen
    for v in connection:
        send_data(v, {
            "update": "karte_aufgedeckt",
            "spieler": spieler_id,
            "karte": karte
        })
    
    # Zähler aktualisieren
    if not hasattr(s, "cards_flipped"):
        s.cards_flipped = {}
    s.cards_flipped[spieler_id] = s.cards_flipped.get(spieler_id, 0) + 1
    
    return spieler_id, karte

def check_if_setup_complete(player_count, cards_flipped, connection, send_data):
    """Prüft, ob alle Spieler ihre ersten 2 Karten aufgedeckt haben"""
    if all(cards_flipped.get(pid, 0) >= 2 for pid in range(1, player_count + 1)):
        # Punktzahlen berechnen
        scores = calculate_scores(s.karten_matrizen, s.aufgedeckt_matrizen)
        
        # Startspieler bestimmen
        startspieler = determine_starting_player(scores)
        
        # Spielreihenfolge berechnen
        reihenfolge = calculate_player_order(startspieler, player_count)
        
        # Spielreihenfolge speichern
        s.spielreihenfolge = reihenfolge
        
        # Allen Clients mitteilen (mit Wiederholung für Sicherheit)
        for v in connection:
            success = send_data(v, {"update": "spielreihenfolge", "reihenfolge": reihenfolge, "scores": scores})
            time.sleep(0.05)
            send_data(v, {"update": "spielreihenfolge", "reihenfolge": reihenfolge, "scores": scores})
        
        return True
    return False

def handle_take_discard_pile(daten, connection, send_data):
    """Verarbeitet das Nehmen einer Karte vom Ablagestapel"""
    spieler_id = daten["spieler_id"]
    ziel_karte = daten["ziel_karte"]
    
    # Aktuelle Karte vom Ablagestapel holen
    discard_value = s.discard_card
    
    # Karte aus der Spielerhand nehmen und auf Ablagestapel legen
    row, col = ziel_karte["row"], ziel_karte["col"]
    alte_karte = s.karten_matrizen[spieler_id][row][col]
    
    # Karten tauschen
    s.karten_matrizen[spieler_id][row][col] = discard_value
    s.aufgedeckt_matrizen[spieler_id][row][col] = True  # Karte ist immer offen
    s.discard_card = alte_karte
    
    # Allen Clients mitteilen
    for v in connection:
        send_data(v, {
            "update": "karten_getauscht",
            "spieler": spieler_id,
            "karte": {"row": row, "col": col},
            "neue_karte": discard_value,
            "ablagestapel": alte_karte
        })
    
    return spieler_id, s.discard_card

def handle_take_draw_pile(daten, connection, send_data):
    """Verarbeitet das Nehmen einer Karte vom Nachziehstapel"""
    spieler_id = daten["spieler_id"]
    
    # Neue zufällige Karte generieren
    neue_karte = generate_random_card()
    
    # Nur dem Spieler mitteilen, der die Karte gezogen hat
    for v in connection:
        if connection.index(v) == spieler_id - 1:  # Spieler-ID beginnt bei 1, Index bei 0
            send_data(v, {
                "update": "nachziehstapel_karte",
                "karte": neue_karte
            })
    
    # Karte in temporärem Speicher halten
    s.gezogene_karte = neue_karte
    
    return spieler_id, neue_karte

def handle_swap_with_draw_pile(daten, connection, send_data):
    """Verarbeitet den Tausch mit einer Karte vom Nachziehstapel"""
    spieler_id = daten["spieler_id"]
    ziel_karte = daten["ziel_karte"]
    
    # Karte aus der Spielerhand nehmen und auf Ablagestapel legen
    row, col = ziel_karte["row"], ziel_karte["col"]
    alte_karte = s.karten_matrizen[spieler_id][row][col]
    
    # Karten tauschen
    s.karten_matrizen[spieler_id][row][col] = s.gezogene_karte
    s.aufgedeckt_matrizen[spieler_id][row][col] = True  # Karte ist immer offen
    s.discard_card = alte_karte
    
    # Allen Clients mitteilen
    for v in connection:
        send_data(v, {
            "update": "karten_getauscht",
            "spieler": spieler_id,
            "karte": {"row": row, "col": col},
            "neue_karte": s.gezogene_karte,
            "ablagestapel": alte_karte
        })
    
    return spieler_id, alte_karte

def handle_reject_draw_pile(daten, connection, send_data):
    """Verarbeitet das Ablehnen einer Karte vom Nachziehstapel"""
    spieler_id = daten["spieler_id"]
    aufzudeckende_karte = daten["aufzudeckende_karte"]
    
    # Abgelehnte Karte auf den Ablagestapel
    s.discard_card = s.gezogene_karte
    
    # Karte des Spielers aufdecken
    row, col = aufzudeckende_karte["row"], aufzudeckende_karte["col"]
    s.aufgedeckt_matrizen[spieler_id][row][col] = True
    
    # Allen Clients mitteilen
    for v in connection:
        send_data(v, {
            "update": "karte_abgelehnt",
            "spieler": spieler_id,
            "ablagestapel": s.gezogene_karte,
            "aufgedeckte_karte": {"row": row, "col": col}
        })
    
    return spieler_id

def update_next_player(spieler_id, connection, send_data):
    """Aktualisiert den nächsten Spieler"""
    # Nächster Spieler ist dran
    s.current_player = get_next_player(spieler_id, s.spielreihenfolge)
    
    # Allen Clients den nächsten Spieler mitteilen
    for v in connection:
        send_data(v, {
            "update": "naechster_spieler",
            "spieler": s.current_player
        })
    
    return s.current_player