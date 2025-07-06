"""
Server-side game logic without pygame dependencies
This avoids UI-related imports and window creation
"""
import random
import time
import settings as s
from entities import triplet_logic  # Neuer Import

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

    # NEUE ZEILE: Auf Dreierkombinationen prüfen
    triplet_logic.remove_column_triplets(spieler_id, connection, send_data)

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

    # Karte aus der Spielerhand nehmen
    row, col = ziel_karte["row"], ziel_karte["col"]
    alte_karte = s.karten_matrizen[spieler_id][row][col]

    # Karten tauschen
    s.karten_matrizen[spieler_id][row][col] = discard_value
    s.aufgedeckt_matrizen[spieler_id][row][col] = True  # Karte ist immer offen

    # Ablagestapel aktualisieren
    if not hasattr(s, "discard_pile"):
        s.discard_pile = []
        # Wenn es bereits eine discard_card gibt, aber noch keinen discard_pile
        if s.discard_card is not None:
            s.discard_pile.append(s.discard_card)

    # Die oberste Karte vom Stapel entfernen
    if len(s.discard_pile) > 0:
        s.discard_pile.pop()

    # Alte Karte auf den Ablagestapel legen
    s.discard_pile.append(alte_karte)
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

    # Auf Dreierkombinationen prüfen
    triplet_logic.remove_column_triplets(spieler_id, connection, send_data)

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

    # NEUE ZEILE: Auf Dreierkombinationen prüfen
    hat_triplets, _ = triplet_logic.remove_column_triplets(spieler_id, connection, send_data)

    # Wenn eine Dreierkombination gefunden wurde, kurz warten
    if hat_triplets:
        import time
        time.sleep(2.0)  # Warten, damit die Triplet-Nachricht verarbeitet wird

    # Nächster Spieler
    next_player = update_next_player(spieler_id, connection, send_data)

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

# Die bestehende check_if_all_cards_revealed Funktion ersetzen
def check_if_all_cards_revealed(spieler_id):
    """Prüft, ob ein Spieler alle seine Karten aufgedeckt hat"""
    return triplet_logic.check_if_all_cards_revealed_with_triplets(spieler_id)

def remove_column_triplets(spieler_id, connection, send_data):
    """Entfernt Dreierkombinationen in den Spalten (delegiert an triplet_logic)"""
    # Einfach die Funktion aus dem triplet_logic Modul aufrufen
    return triplet_logic.remove_column_triplets(spieler_id, connection, send_data)

def handle_round_end(connection, send_data):
    """Verarbeitet das Rundenende, wenn ein Spieler alle Karten aufgedeckt hat"""
    print("[DEBUG] Rundenende wird eingeleitet...")

    # Prüfen, ob bereits ein Rundenende im Gang ist
    if hasattr(s, "round_ending") and s.round_ending:
        print("[DEBUG] Rundenende bereits im Gang - Spieler für letzte Züge:", s.last_turn_players)
        return False

    # Flag setzen, dass Rundenende im Gang ist
    s.round_ending = True

    trigger_player = int(s.current_player)
    s.round_end_trigger = trigger_player  # Spieler, der das Rundenende ausgelöst hat

    # Spieler, die noch einen letzten Zug haben (alle außer dem Auslöser)
    s.last_turn_players = [p for p in s.spielreihenfolge if int(p) != s.round_end_trigger]
    print(f"[DEBUG] Spieler für letzte Züge: {s.last_turn_players}")

    # Allen Clients mitteilen, dass das Rundenende begonnen hat
    for v in connection:
        send_data(v, {
            "update": "round_end_started",
            "trigger_player": s.round_end_trigger,
            "last_turn_players": s.last_turn_players
        })

    # FIXED: Direkt den ersten Spieler aus last_turn_players als nächsten Spieler setzen
    # statt find_next_last_turn_player zu verwenden
    if s.last_turn_players:
        s.current_player = s.last_turn_players[0]
        print(f"[DEBUG] Erster Spieler für letzten Zug: {s.current_player}")

        # Allen Clients den nächsten Spieler mitteilen
        for v in connection:
            send_data(v, {
                "update": "naechster_spieler",
                "spieler": s.current_player
            })
    else:
        # Wenn keine weiteren Spieler vorhanden sind, Runde beenden
        finalize_round(connection, send_data)

    return True

def find_next_last_turn_player(current_player):
    """Findet den nächsten Spieler, der seinen letzten Zug machen muss"""
    if not hasattr(s, "last_turn_players") or not s.last_turn_players:
        print("[DEBUG] Keine weiteren Spieler für letzten Zug")
        return None

    # FIXED: Sicherstellen, dass wir nicht denselben Spieler nochmal wählen
    for player in s.last_turn_players:
        if player != current_player:
            print(f"[DEBUG] Nächster Spieler für letzten Zug: {player} (aus Liste: {s.last_turn_players})")
            return player

    # Wenn kein anderer Spieler gefunden wird (unwahrscheinlich), ersten nehmen
    next_player = s.last_turn_players[0]
    print(f"[DEBUG] Nächster Spieler für letzten Zug: {next_player} (aus Liste: {s.last_turn_players})")
    return next_player

def finalize_round(connection, send_data):
    """Beendet die Runde und deckt alle Karten auf"""
    print("[DEBUG] Runde wird beendet...")

    # Alle verbleibenden Karten aufdecken
    for pid in range(1, s.player_count + 1):
        for row in range(len(s.aufgedeckt_matrizen[pid])):
            for col in range(len(s.aufgedeckt_matrizen[pid][row])):
                s.aufgedeckt_matrizen[pid][row][col] = True

    # Punktzahlen berechnen
    scores = calculate_scores(s.karten_matrizen, s.aufgedeckt_matrizen)

    # Prüfen, ob der Auslöser die niedrigste Punktzahl hat
    min_score = min(scores.values())
    min_players = [pid for pid, score in scores.items() if score == min_score]

    # Bei Gleichstand zählt der Auslöser nicht als niedrigste Punktzahl
    if s.round_end_trigger not in min_players or len(min_players) > 1:
        print(f"[DEBUG] Auslöser {s.round_end_trigger} hat nicht die niedrigste Punktzahl. Punkte werden verdoppelt!")
        scores[s.round_end_trigger] *= 2

    # Allen Clients das Rundenende mitteilen
    for v in connection:
        send_data(v, {
            "update": "round_end",
            "final_scores": scores,
            "trigger_player": s.round_end_trigger,
            "aufgedeckt_matrizen": s.aufgedeckt_matrizen
        })