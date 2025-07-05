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

def check_column_for_triplets(matrix, aufgedeckt_matrix):
    """Prüft, ob drei gleiche aufgedeckte Karten in einer Spalte sind"""
    cols = len(matrix[0])
    rows = len(matrix)
    columns_to_remove = []
    
    for col in range(cols):
        # Nur aufgedeckte Karten in dieser Spalte sammeln
        column_values = []
        for row in range(rows):
            if aufgedeckt_matrix[row][col]:
                column_values.append(matrix[row][col])
        
        # Wenn 3 aufgedeckte Karten und alle gleich sind
        if len(column_values) == 3 and len(set(column_values)) == 1:
            columns_to_remove.append(col)
    
    return columns_to_remove

def remove_column_triplets(spieler_id, connection, send_data):
    """Entfernt Spalten mit drei gleichen Karten und legt sie auf den Ablagestapel"""
    matrix = s.karten_matrizen[spieler_id]
    aufgedeckt_matrix = s.aufgedeckt_matrizen[spieler_id]
    
    # Spalten mit Dreierkombinationen finden
    columns_to_remove = check_column_for_triplets(matrix, aufgedeckt_matrix)
    
    if not columns_to_remove:
        return False, None  # Keine Dreierkombinationen gefunden
    
    removed_cards = []
    for col in columns_to_remove:
        # Karten aus der Spalte sammeln und auf den Ablagestapel legen
        for row in range(len(matrix)):
            if aufgedeckt_matrix[row][col]:
                # Wert speichern und auf Ablagestapel legen
                card_value = matrix[row][col]
                removed_cards.append({"row": row, "col": col, "value": card_value})
                
                # Ablagestapel aktualisieren
                s.discard_card = card_value
                
                # Markiere die Karte als "entfernt", behalte aber den Wert bei
                # ÄNDERUNG: Setze einen zusätzlichen Eintrag im Matrix-Dictionary
                # anstatt den Wert zu überschreiben
                if not hasattr(s, "removed_cards"):
                    s.removed_cards = {}
                if spieler_id not in s.removed_cards:
                    s.removed_cards[spieler_id] = []
                
                s.removed_cards[spieler_id].append({"row": row, "col": col})
                
    # Allen Clients mitteilen
    if removed_cards:
        for v in connection:
            send_data(v, {
                "update": "spalte_entfernt",
                "spieler": spieler_id,
                "entfernte_karten": removed_cards,
                "ablagestapel": s.discard_card
            })
    
    return True, removed_cards

def check_if_all_cards_revealed(spieler_id):
    """Prüft, ob ein Spieler alle seine Karten aufgedeckt hat"""
    if not hasattr(s, "aufgedeckt_matrizen") or spieler_id not in s.aufgedeckt_matrizen:
        print(f"[DEBUG] Keine aufgedeckt_matrizen für Spieler {spieler_id}")
        return False
    
    # Wichtiger Fix: Stelle sicher, dass spieler_id wirklich ein Integer ist
    if isinstance(spieler_id, str):
        spieler_id = int(spieler_id)
        
    aufgedeckt_matrix = s.aufgedeckt_matrizen[spieler_id]
    
    # Sammle entfernte Kartenpositionen
    removed_positions = []
    if hasattr(s, "removed_cards") and spieler_id in s.removed_cards:
        removed_positions = [(card["row"], card["col"]) for card in s.removed_cards[spieler_id]]
    
    # Prüfen, ob alle Karten aufgedeckt sind
    verdeckte_karten = []
    for row_idx, row in enumerate(aufgedeckt_matrix):
        for col_idx, is_flipped in enumerate(row):
            # Eine Karte gilt als "aufgedeckt", wenn sie wirklich aufgedeckt oder entfernt ist
            if not is_flipped and (row_idx, col_idx) not in removed_positions:
                verdeckte_karten.append((row_idx, col_idx))
    
    if verdeckte_karten:
        print(f"[DEBUG] Spieler {spieler_id} hat noch {len(verdeckte_karten)} verdeckte Karten: {verdeckte_karten}")
        return False
    
    print(f"[DEBUG] WICHTIG: Spieler {spieler_id} hat alle Karten aufgedeckt oder entfernt!")
    return True

def handle_round_end(connection, send_data):
    """Verarbeitet das Rundenende"""
    # Speichern, wer das Rundenende ausgelöst hat
    if not hasattr(s, "round_end_trigger"):
        s.round_end_trigger = s.current_player
    
    # Prüfen, ob bereits ein Rundenende im Gang ist
    if hasattr(s, "round_ending") and s.round_ending:
        print("[DEBUG] Rundenende bereits im Gang, ignoriere erneute Auslösung")
        return False
    
    # Flag setzen, dass Rundenende im Gang ist
    s.round_ending = True

    # Allen Clients mitteilen, dass das Rundenende begonnen hat
    for v in connection:
        send_data(v, {
            "update": "round_end_started",
            "trigger_player": s.round_end_trigger
        })
    
    # Spieler, die noch einen letzten Zug haben
    if not hasattr(s, "last_turn_players"):
        s.last_turn_players = set(range(1, s.player_count + 1))
        s.last_turn_players.remove(s.round_end_trigger)
    
    # WICHTIG: Wenn keine Spieler mehr für den letzten Zug übrig sind, beende die Runde
    if not s.last_turn_players:
        return finalize_round(connection, send_data)
    
    # Zum nächsten Spieler wechseln, der seinen letzten Zug noch nicht gemacht hat
    next_player = find_next_last_turn_player(s.current_player)
    if next_player:
        s.current_player = next_player
        # Allen Clients den nächsten Spieler mitteilen
        for v in connection:
            send_data(v, {
                "update": "naechster_spieler",
                "spieler": s.current_player
            })
        print(f"[DEBUG] Nächster Spieler für letzten Zug: {s.current_player}")
    
    return True

def find_next_last_turn_player(current_player):
    """Findet den nächsten Spieler, der seinen letzten Zug machen muss"""
    # Wenn keine Spieler mehr übrig sind
    if not hasattr(s, "last_turn_players") or not s.last_turn_players:
        return None
    
    # Die Spielreihenfolge verwenden, um den nächsten Spieler zu finden
    player_order = s.spielreihenfolge
    current_idx = player_order.index(current_player) if current_player in player_order else -1
    
    # Suche vom nächsten Spieler aus
    for i in range(1, len(player_order) + 1):
        next_idx = (current_idx + i) % len(player_order)
        next_player = player_order[next_idx]
        
        # WICHTIGER FIX: Wenn wir wieder beim Auslöser ankommen, beende die Runde
        if next_player == s.round_end_trigger:
            print(f"[DEBUG] Nächster Spieler wäre der Auslöser {next_player} - Runde wird beendet")
            # Leere die last_turn_players Liste, um die Runde zu beenden
            s.last_turn_players.clear()
            return None
        
        if next_player in s.last_turn_players:
            return next_player
    
    # Wenn kein Spieler gefunden wurde, nehme den ersten aus last_turn_players
    return next(iter(s.last_turn_players))

def finalize_round(connection, send_data):
    """Beendet die Runde und berechnet die finalen Punktzahlen"""
    # Finale Punktzahlen berechnen
    final_scores = calculate_final_round_scores()
    
    # Punktzahl des Auslösers verdoppeln, wenn er nicht die niedrigste Punktzahl hat
    min_score = min(final_scores.values())
    min_players = [pid for pid, score in final_scores.items() if score == min_score]
    
    if s.round_end_trigger not in min_players:
        final_scores[s.round_end_trigger] *= 2
        doubled = True
    else:
        doubled = False
    
    # Runden-Nummer aktualisieren
    if not hasattr(s, "current_round"):
        s.current_round = 1
    else:
        s.current_round += 1
    
    # Gesamtpunktzahlen aktualisieren
    if not hasattr(s, "total_scores"):
        s.total_scores = {pid: 0 for pid in range(1, s.player_count + 1)}
        s.round_scores = {}
    
    # Rundenstand speichern
    s.round_scores[s.current_round] = final_scores.copy()
    
    # Gesamtpunktzahl aktualisieren
    for pid, score in final_scores.items():
        s.total_scores[pid] += score
    
    # Prüfen, ob alle Runden gespielt wurden
    game_over = s.current_round >= s.round_count
    
    # Allen Clients das Rundenende mitteilen
    for v in connection:
        send_data(v, {
            "update": "round_end",
            "final_scores": final_scores,
            "trigger_player": s.round_end_trigger,
            "doubled": doubled,
            "current_round": s.current_round,
            "total_rounds": s.round_count,
            "total_scores": s.total_scores,
            "round_scores": s.round_scores,
            "game_over": game_over
        })
    
    # Runde zurücksetzen wenn das Spiel noch nicht vorbei ist
    if not game_over:
        reset_round(connection, send_data)
    
    return True

def calculate_final_round_scores():
    """Berechnet die finalen Punktzahlen für diese Runde"""
    final_scores = {}
    
    for pid in range(1, s.player_count + 1):
        matrix = s.karten_matrizen[pid]
        punkte = 0
        
        # Prüfe, ob entfernte Karten für diesen Spieler existieren
        removed_positions = []
        if hasattr(s, "removed_cards") and pid in s.removed_cards:
            removed_positions = [(card["row"], card["col"]) for card in s.removed_cards[pid]]
        
        for row in range(len(matrix)):
            for col in range(len(matrix[0])):
                # Zähle Karten, die nicht entfernt wurden
                if (row, col) not in removed_positions:
                    punkte += matrix[row][col]
        
        final_scores[pid] = punkte
    
    return final_scores

def reset_round(connection, send_data):
    """Setzt die Spielumgebung für eine neue Runde zurück"""
    # Neue Karten erzeugen
    karten_matrizen = create_card_matrices(s.player_count, s.ROWS, s.COLS)
    s.karten_matrizen = karten_matrizen
    
    # Neue Aufgedeckt-Matrizen
    aufgedeckt_matrizen = create_flipped_matrices(s.player_count, s.ROWS, s.COLS)
    s.aufgedeckt_matrizen = aufgedeckt_matrizen
    
    # Neue Ablagestapelkarte
    discard_card_value = generate_random_card()
    s.discard_card = discard_card_value
    
    # Zähler zurücksetzen
    if hasattr(s, "cards_flipped"):
        s.cards_flipped = {}
    
    # Spieler, der das Ende ausgelöst hat, beginnt die neue Runde
    s.current_player = s.round_end_trigger
    
    # Runden-Auslöser zurücksetzen
    if hasattr(s, "round_end_trigger"):
        delattr(s, "round_end_trigger")
    
    if hasattr(s, "last_turn_players"):
        delattr(s, "last_turn_players")
    
    # Allen Clients die neue Runde mitteilen
    for v in connection:
        send_data(v, {
            "update": "new_round",
            "current_round": s.current_round,
            "total_rounds": s.round_count,
            "karten_matrizen": karten_matrizen,
            "aufgedeckt_matrizen": aufgedeckt_matrizen,
            "discard_card": discard_card_value,
            "current_player": s.current_player
        })
    
    return True