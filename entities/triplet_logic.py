"""
Diese Datei enthält die Logik für die Erkennung und Verarbeitung von Dreierkombinationen in Skyjo.
Eine Dreierkombination besteht aus drei Karten mit gleichem Wert in einer Spalte.
Wenn eine solche Kombination erkannt wird, werden die Karten automatisch entfernt
und auf den Ablagestapel gelegt.
"""
import settings as s
import time

def berechne_punktzahl(matrix, aufgedeckt_matrix, spieler_id):
    """Berechnet die Punktzahl für einen Spieler, entfernt Triplets korrekt"""
    punkte = 0
    removed = []
    if hasattr(s, "removed_cards") and spieler_id in s.removed_cards:
        removed = [(card["row"], card["col"]) for card in s.removed_cards[spieler_id]]
    for row in range(len(matrix)):
        for col in range(len(matrix[0])):
            if aufgedeckt_matrix[row][col] and (row, col) not in removed:
                punkte += matrix[row][col]
    # Triplets abziehen (jede entfernte Spalte = 3 Karten)
    if hasattr(s, "removed_cards") and spieler_id in s.removed_cards:
        removed_cols = [card["col"] for card in s.removed_cards[spieler_id]]
        for col in set(removed_cols):
            triplet_value = matrix[0][col]
            punkte -= 3 * triplet_value  # <-- KORREKT: 3 mal Wert abziehen!
    return punkte

def calculate_scores(karten_matrizen, aufgedeckt_matrizen, ausloeser_id=None):
    """Berechnet die Scores für alle Spieler. Beim Auslöser ggf. Verdopplung."""
    scores = {}
    for pid in karten_matrizen.keys():
        matrix = karten_matrizen[pid]
        aufgedeckt_matrix = aufgedeckt_matrizen[pid]
        scores[pid] = berechne_punktzahl(matrix, aufgedeckt_matrix, pid)

    # Skyjo-Regel: Wenn Auslöser nicht den niedrigsten Score hat, wird sein Score verdoppelt
    if ausloeser_id is not None:
        ausloeser_score = scores[ausloeser_id]
        min_score = min(scores.values())
        if any(pid != ausloeser_id and score <= ausloeser_score for pid, score in scores.items()):
            scores[ausloeser_id] = ausloeser_score * 2

    return scores

def check_column_for_triplets(matrix, aufgedeckt_matrix, spieler_id):
    """
    Prüft, ob drei gleiche aufgedeckte Karten in einer Spalte sind.
    
    Args:
        matrix: Die Kartenmatrix eines Spielers
        aufgedeckt_matrix: Die Matrix, die angibt, welche Karten aufgedeckt sind
        
    Returns:
        list: Liste der Spaltenindizes, die Dreierkombinationen enthalten
    """
    cols = len(matrix[0])
    rows = len(matrix)
    columns_to_remove = []
    
    # Überprüfen, ob Spalten bereits entfernt wurden, 
    # aber NUR für den aktuellen Spieler!
    removed_columns = set()
    if hasattr(s, "removed_cards") and spieler_id in s.removed_cards:
        for card in s.removed_cards[spieler_id]:  # Nur die Karten des aktuellen Spielers
            removed_columns.add(card["col"])
    
    for col in range(cols):
        # Spalte überspringen, wenn sie bereits für DIESEN Spieler entfernt wurde
        if col in removed_columns:
            print(f"[DEBUG] Spalte {col} wurde bereits bei Spieler {spieler_id} entfernt, überspringe")
            continue
            
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
    """
    Entfernt Spalten mit drei gleichen Karten und legt sie auf den Ablagestapel.
    
    Args:
        spieler_id: ID des Spielers
        connection: Liste der Client-Verbindungen
        send_data: Funktion zum Senden von Daten an Clients
        
    Returns:
        tuple: (hat_triplets, entfernte_spalten) - hat_triplets ist ein Boolean,
               entfernte_spalten ist eine Liste von entfernten Spaltenindizes
    """
    matrix = s.karten_matrizen[spieler_id]
    aufgedeckt_matrix = s.aufgedeckt_matrizen[spieler_id]
    
    # Spalten mit Dreierkombinationen finden
    columns_to_remove = check_column_for_triplets(matrix, aufgedeckt_matrix, spieler_id)  # spieler_id als Parameter übergeben
    
    if not columns_to_remove:
        return False, None  # Keine Dreierkombinationen gefunden
    
    removed_cards = []
    for col in columns_to_remove:
        # Spalte enthält eine Dreierkombination
        print(f"[DEBUG] Dreierkombination in Spalte {col} bei Spieler {spieler_id} gefunden! Wert: {matrix[0][col]}")
        
        # Karten aus der Spalte sammeln und auf den Ablagestapel legen
        for row in range(len(matrix)):
            if aufgedeckt_matrix[row][col]:
                # Wert speichern und auf Ablagestapel legen
                card_value = matrix[row][col]
                removed_cards.append({"row": row, "col": col, "value": card_value})
                
                # Nur EINE Karte auf den Ablagestapel legen (die oberste)
                s.discard_card = matrix[0][col]
                
                # Ablagestapel aktualisieren
                if not hasattr(s, "discard_pile"):
                    s.discard_pile = []
                
                # Nur eine Karte auf den Ablagestapel legen
                s.discard_pile.append(s.discard_card)
                
                # Markiere die Karte als "entfernt", behalte aber den Wert bei
                if not hasattr(s, "removed_cards"):
                    s.removed_cards = {}
                if spieler_id not in s.removed_cards:
                    s.removed_cards[spieler_id] = []
                
                s.removed_cards[spieler_id].append({"row": row, "col": col})
    
    # Allen Clients mitteilen
    if removed_cards:
        # WICHTIG: Erst eine Pause, damit vorherige Nachrichten verarbeitet werden
        #import time
        time.sleep(0.5)  # Pause vor dem Senden
        
        for v in connection:
            message = {
                "update": "triplet_removed",
                "spieler": spieler_id,
                "col": columns_to_remove[0],
                "card_values": [matrix[0][columns_to_remove[0]]] * 3,
                "discard_value": s.discard_card
            }
            print(f"[DEBUG] Sende Nachricht an Client: {message}")
            
            success = send_data(v, message)
            print(f"[DEBUG] Triplet-Nachricht gesendet an Client: Erfolg={success}")
            
        # WICHTIG: Zusätzliche Pause nach dem Senden, bevor weitere Nachrichten gesendet werden
        time.sleep(2.0)  # Längere Pause, damit die Nachricht komplett angezeigt wird
    
    # Nach dem Entfernen:
    from entities.serv_gameprocess import all_cards_visible_or_removed
    if not s.round_end_triggered and all_cards_visible_or_removed(spieler_id):
        s.round_end_triggered = True
        s.round_end_trigger_player = spieler_id
        for v in connection:
            send_data(v, {
                "update": "round_end_triggered",
                "spieler": spieler_id
            })
        print(f"[INFO] Rundenende ausgelöst von Spieler {spieler_id}!")
    
    # Punkte nach dem Entfernen eines Triplets aktualisieren
    scores = calculate_scores(s.karten_matrizen, s.aufgedeckt_matrizen)
    for v in connection:
        send_data(v, {
            "update": "triplet_punkte_aktualisiert",  # NEUER Nachrichtentyp!
            "scores": scores
        })
    
    return True, columns_to_remove

def is_affected_by_triplet_removal(spieler_id, row, col):
    """
    Prüft, ob eine bestimmte Kartenposition durch Dreierkombinationen entfernt wurde.
    
    Args:
        spieler_id: ID des Spielers
        row: Zeilenindex der Karte
        col: Spaltenindex der Karte
        
    Returns:
        bool: True wenn die Karte entfernt wurde, sonst False
    """
    if not hasattr(s, "removed_cards") or spieler_id not in s.removed_cards:
        return False
    
    for card in s.removed_cards[spieler_id]:
        if card["row"] == row and card["col"] == col:
            return True
    
    return False

def check_if_all_cards_revealed_with_triplets(spieler_id):
    """
    Prüft, ob ein Spieler alle seine Karten aufgedeckt hat,
    unter Berücksichtigung entfernter Triplets.
    
    Args:
        spieler_id: ID des Spielers
        
    Returns:
        bool: True wenn alle Karten aufgedeckt oder entfernt sind, sonst False
    """
    if not hasattr(s, "aufgedeckt_matrizen") or spieler_id not in s.aufgedeckt_matrizen:
        return False
    
    aufgedeckt_matrix = s.aufgedeckt_matrizen[spieler_id]
    
    # Sammle entfernte Kartenpositionen
    removed_positions = []
    if hasattr(s, "removed_cards") and spieler_id in s.removed_cards:
        removed_positions = [(card["row"], card["col"]) for card in s.removed_cards[spieler_id]]
    
    # Prüfen, ob alle Karten aufgedeckt sind
    for row_idx, row in enumerate(aufgedeckt_matrix):
        for col_idx, is_flipped in enumerate(row):
            # Eine Karte gilt als "aufgedeckt", wenn sie wirklich aufgedeckt oder entfernt ist
            if not is_flipped and (row_idx, col_idx) not in removed_positions:
                return False  # Es gibt noch verdeckte Karten
    
    return True  # Alle Karten sind aufgedeckt oder entfernt