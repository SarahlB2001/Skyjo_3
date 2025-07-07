"""
Server-side game logic without pygame dependencies
This avoids UI-related imports and window creation
"""
import random
import time
import settings as s
from entities import triplet_logic  # Neuer Import
from entities.triplet_logic import berechne_punktzahl, calculate_scores  # Diese Funktionen importieren

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

    # NEU: Rundenende prüfen
    if not s.round_end_triggered and all_cards_visible_or_removed(spieler_id):
        s.round_end_triggered = True
        s.round_end_trigger_player = spieler_id
        for v in connection:
            send_data(v, {
                "update": "round_end_triggered",
                "spieler": spieler_id
            })
        print(f"[INFO] Rundenende ausgelöst von Spieler {spieler_id}!")
        time.sleep(0.2)  # Kleine Pause
        # Wiederhole die Nachricht für alle Clients
        for v in connection:
            send_data(v, {
                "update": "round_end_triggered",
                "spieler": spieler_id
            })
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

    # Nach dem Tausch:
    triplet_logic.remove_column_triplets(spieler_id, connection, send_data)

    # NEU: Rundenende prüfen
    if not s.round_end_triggered and all_cards_visible_or_removed(spieler_id):
        s.round_end_triggered = True
        s.round_end_trigger_player = spieler_id
        for v in connection:
            send_data(v, {
                "update": "round_end_triggered",
                "spieler": spieler_id
            })
        print(f"[INFO] Rundenende ausgelöst von Spieler {spieler_id}!")
        time.sleep(0.2)  # Kleine Pause
        # Wiederhole die Nachricht für alle Clients
        for v in connection:
            send_data(v, {
                "update": "round_end_triggered",
                "spieler": spieler_id
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

    # NEUE ZEILE: Auf Dreierkombinationen prüfen
    hat_triplets, _ = triplet_logic.remove_column_triplets(spieler_id, connection, send_data)
    if hat_triplets:
        #import time
        time.sleep(0.5) ############################war 2
    # NEU: Rundenende prüfen
    if not s.round_end_triggered and all_cards_visible_or_removed(spieler_id):
        s.round_end_triggered = True
        s.round_end_trigger_player = spieler_id
        for v in connection:
            send_data(v, {
                "update": "round_end_triggered",
                "spieler": spieler_id
            })
        print(f"[INFO] Rundenende ausgelöst von Spieler {spieler_id}!")
        time.sleep(0.2)  # Kleine Pause
        # Wiederhole die Nachricht für alle Clients
        for v in connection:
            send_data(v, {
                "update": "round_end_triggered",
                "spieler": spieler_id
            })
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

    triplet_logic.remove_column_triplets(spieler_id, connection, send_data)

    return spieler_id

def update_next_player(spieler_id, connection, send_data):
    """Aktualisiert den nächsten Spieler"""
    # Nächster Spieler ist dran
    s.current_player = get_next_player(spieler_id, s.spielreihenfolge)

    # NEU: Rundenende prüfen
    if s.round_end_triggered and s.current_player == s.round_end_trigger_player:
        # Rundenende wirklich durchführen!
        for v in connection:
            send_data(v, {
                "update": "round_ended"
            })
        print("[INFO] Runde beendet!")

        # 4 Sekunden Pause, damit die Nachricht sichtbar bleibt
        time.sleep(3) #############war 3

        # Alle verdeckten Karten aufdecken
        for pid, aufgedeckt_matrix in s.aufgedeckt_matrizen.items():
            for row in range(len(aufgedeckt_matrix)):
                for col in range(len(aufgedeckt_matrix[row])):
                    entfernt = False
                    if hasattr(s, "removed_cards") and pid in s.removed_cards:
                        entfernt = any(card["row"] == row and card["col"] == col for card in s.removed_cards[pid])
                    if not entfernt:
                        aufgedeckt_matrix[row][col] = True
                        for v in connection:
                            send_data(v, {
                                "update": "karte_aufgedeckt",
                                "spieler": pid,
                                "karte": {"row": row, "col": col}
                            })
                        time.sleep(0.05)  # Sehr kurze Pause reicht!

        # KORREKTUR: Längere Wartezeit für die Verarbeitung
        time.sleep(2)  # 3 Sekunden statt nur 1 ###########################

        # KORREKTUR: Trigger-Spieler explizit übergeben
        scores = calculate_scores(
            s.karten_matrizen,
            s.aufgedeckt_matrizen,
            ausloeser_id=s.round_end_trigger_player  # Diese wichtige Parameter fehlte!
        )

        # Allen Clients die finalen Punktzahlen mitteilen
        for v in connection:
            send_data(v, {
                "update": "punkte_aktualisiert",
                "scores": scores
            })

        s.round_end_triggered = False
        s.round_end_trigger_player = None
        return s.current_player

    # Normal weitermachen
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

def all_cards_visible_or_removed(spieler_id):
    """True, wenn alle Karten aufgedeckt oder entfernt sind."""
    aufgedeckt = s.aufgedeckt_matrizen[spieler_id]
    removed = set()
    if hasattr(s, "removed_cards") and spieler_id in s.removed_cards:
        removed = {(c["row"], c["col"]) for c in s.removed_cards[spieler_id]}
    for r, row in enumerate(aufgedeckt):
        for c, is_up in enumerate(row):
            if not is_up and (r, c) not in removed:
                return False
    return True

def remove_column_triplets(spieler_id, connection, send_data):
    """Entfernt Dreierkombinationen in den Spalten (delegiert an triplet_logic)"""
    # Einfach die Funktion aus dem triplet_logic Modul aufrufen
    return triplet_logic.remove_column_triplets(spieler_id, connection, send_data)