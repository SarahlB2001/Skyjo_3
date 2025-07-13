"""
Dieses Modul enthält die serverseitige Spiellogik für Skyjo.
Es verwaltet die Kartenmatrizen, Spielreihenfolge, Punkteberechnung und
Kommunikation mit den Clients, ohne pygame-Abhängigkeiten.
Enthalten sind Funktionen für das Erstellen und Verwalten der Karten,
Spieleraktionen, Rundenfortschritt und Triplet-Logik.
"""
import random
import time
import settings as s
from entities import triplet_logic
from entities.triplet_logic import berechne_punktzahl, calculate_scores  # Diese Funktionen importieren

def create_card_matrices(player_count, rows, cols):
    """Erzeugt die Kartenmatrizen für alle Spieler"""
    karten_matrizen = {}

    # Erstelle ein vollständiges Deck
    deck = create_deck()

    # Nachziehstapel in settings speichern
    s.draw_pile = deck

    for pid in range(1, player_count + 1):
        matrix = []
        for row in range(rows):
            row_cards = []
            for _ in range(cols):
                # Karte vom gemischten Deck nehmen
                if s.draw_pile:
                    row_cards.append(s.draw_pile.pop())
                else:
                    # Notfall: Falls das Deck leer sein sollte
                    row_cards.append(random.randint(-2, 12))
            matrix.append(row_cards)
        karten_matrizen[pid] = matrix

    # Erste Karte für Ablagestapel
    if s.draw_pile:
        s.discard_card = s.draw_pile.pop()
        s.discard_pile = [s.discard_card]
    else:
        s.discard_card = random.randint(-2, 12)
        s.discard_pile = [s.discard_card]

    return karten_matrizen

def create_flipped_matrices(player_count, rows, cols):
    """Erzeugt die Matrizen für aufgedeckte Karten"""
    aufgedeckt_matrizen = {}
    for pid in range(1, player_count + 1):
        aufgedeckt_matrizen[pid] = [[False for _ in range(cols)] for _ in range(rows)]
    return aufgedeckt_matrizen


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

    # Auf Dreierkombinationen prüfen
    triplet_logic.remove_column_triplets(spieler_id, connection, send_data)

    # Rundenende prüfen
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

    # Rundenende prüfen
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
    neue_karte = draw_card_from_deck()

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

    # Auf Dreierkombinationen prüfen
    hat_triplets, _ = triplet_logic.remove_column_triplets(spieler_id, connection, send_data)
    if hat_triplets:

        time.sleep(0.5)
    # Rundenende prüfen
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

    if getattr(s, "game_over", False):
        print("[DEBUG] Spiel ist vorbei (Flag), kein naechster_spieler mehr!")
        return s.current_player

    # Nächster Spieler ist dran
    s.current_player = get_next_player(spieler_id, s.spielreihenfolge)

    # Rundenende prüfen
    if s.round_end_triggered and s.current_player == s.round_end_trigger_player:
        # Rundenende wirklich durchführen!
        for v in connection:
            send_data(v, {
                "update": "round_ended"
            })
        print("[INFO] Runde beendet!")

        # 4 Sekunden Pause, damit die Nachricht sichtbar bleibt
        time.sleep(4)

        # Alle verdeckten Karten auf einmal aufdecken
        all_cards_to_reveal = {}
        for pid, aufgedeckt_matrix in s.aufgedeckt_matrizen.items():
            all_cards_to_reveal[pid] = []
            for row in range(len(aufgedeckt_matrix)):
                for col in range(len(aufgedeckt_matrix[row])):
                    entfernt = False
                    if hasattr(s, "removed_cards") and pid in s.removed_cards:
                        entfernt = any(card["row"] == row and card["col"] == col for card in s.removed_cards[pid])
                    if not entfernt and not aufgedeckt_matrix[row][col]:  # Nur nicht aufgedeckte Karten
                        # Markiere Karte als aufgedeckt
                        aufgedeckt_matrix[row][col] = True
                        # Füge zur Liste hinzu
                        all_cards_to_reveal[pid].append({"row": row, "col": col})

        # Sende eine einzige Nachricht mit allen Karten
        for v in connection:
            send_data(v, {
                "update": "reveal_all_cards",
                "all_cards": all_cards_to_reveal
            })
        print("[DEBUG] Alle verbleibenden Karten aufgedeckt!")

        # Warte kurz damit alle Clients die Nachricht verarbeiten können
        time.sleep(1.0)


        # Längere Wartezeit für die Verarbeitung
        pause = 2.5 + s.player_count * 1.5
        time.sleep(pause)


        # Trigger-Spieler explizit übergeben
        scores = calculate_scores(
            s.karten_matrizen,
            s.aufgedeckt_matrizen,
            ausloeser_id=s.round_end_trigger_player
        )

        # Allen Clients die finalen Punktzahlen mitteilen
        for v in connection:
            send_data(v, {
                "update": "punkte_aktualisiert",
                "scores": scores
            })

        # ...nach Punkteberechnung und Senden der Punktzahlen...
        if hasattr(s, "current_round") and hasattr(s, "round_count"):
            if s.current_round < s.round_count:
                s.current_round += 1
                reset_for_new_round()
                for v in connection:
                    send_data(v, {
                        "update": "new_round_starting",
                        "message": f"Runde {s.current_round} beginnt!",
                        "karten_matrizen": s.karten_matrizen,
                        "aufgedeckt_matrizen": s.aufgedeckt_matrizen,
                        "discard_card": s.discard_card,
                        "current_round": s.current_round,
                        "round_count": s.round_count
                    })
            else:
                for v in connection:
                    send_data(v, {
                        "update": "game_ended",
                        "message": "Alle Runden beendet. Spielende!"
                    })


            # Wenn das Spiel vorbei ist, KEIN "naechster_spieler" mehr senden!
                if hasattr(s, "current_round") and hasattr(s, "round_count") and s.current_round >= s.round_count:
                    s.game_over = True
                    print("[DEBUG] Spiel ist vorbei, kein naechster_spieler mehr!")
                    s.round_end_triggered = False
                    s.round_end_trigger_player = None
                    return None

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

def reset_for_new_round():
    s.karten_matrizen = create_card_matrices(s.player_count, s.ROWS, s.COLS)
    s.aufgedeckt_matrizen = create_flipped_matrices(s.player_count, s.ROWS, s.COLS)
    s.removed_cards = {}
    s.cards_flipped = {}
    s.round_end_triggered = False
    s.round_end_trigger_player = None
    s.discard_card = draw_card_from_deck()
    s.cards_flipped_this_turn = 0
    s.setup_phase = True
    s.waiting_for_start = False
    s.zug_begonnen = False
    s.current_player = None

def create_deck():
    """Erstellt ein vollständiges Skyjo-Kartendeck mit korrekten Häufigkeiten"""
    deck = []

    # Skyjo-Karten nach offiziellem Spiel:
    deck.extend([-2] * 5)      # 5× -2
    deck.extend([-1] * 10)     # 10× -1
    deck.extend([0] * 15)      # 15× 0

    for i in range(1, 13):
        deck.extend([i] * 10)  # je 10× Karten von 1-12

    # Mischen des Decks
    random.shuffle(deck)
    return deck

def draw_card_from_deck():
    """Zieht eine Karte vom Nachziehstapel"""
    # Wenn Nachziehstapel leer ist, Ablagestapel mischen und als neuen Nachziehstapel verwenden
    if not hasattr(s, "draw_pile") or not s.draw_pile:
        s.draw_pile = []

        # Falls Ablagestapel existiert, diesen verwenden
        if hasattr(s, "discard_pile") and len(s.discard_pile) > 1:
            # Oberste Karte behalten
            top_card = s.discard_pile.pop()

            # Rest mischen und als Nachziehstapel verwenden
            s.draw_pile = s.discard_pile[:]
            random.shuffle(s.draw_pile)

            # Ablagestapel nur mit oberster Karte neu initialisieren
            s.discard_pile = [top_card]
            s.discard_card = top_card

        # Falls kein Nachziehstapel und Ablagestapel, neues Deck erstellen
        if not s.draw_pile:
            s.draw_pile = create_deck()
            random.shuffle(s.draw_pile)

    # Karte vom Stapel nehmen
    return s.draw_pile.pop()