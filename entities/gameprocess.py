import pygame
import server as serv
import settings as s
from dictionaries import cardSetPosition as cP

# Karteninteraktion
def handle_card_click(sock, spieler_id, my_layout, row_idx, col_idx, card):
    """Verarbeitet Klicks auf Karten im Spielfeld"""
    print(f"[DEBUG] handle_card_click: spieler_id={spieler_id}, current_player={getattr(s, 'current_player', 'None')}")
    print(f"[DEBUG] setup_phase={getattr(s, 'setup_phase', False)}, cards_flipped={getattr(s, 'cards_flipped_this_turn', 0)}")
    
    # Im Setup-Modus oder ersten Zug bis zu 2 Karten aufdecken
    in_setup = hasattr(s, "setup_phase") and s.setup_phase
    
    if (in_setup or getattr(s, "cards_flipped_this_turn", 0) < 2) and not card.is_face_up:
        print(f"[DEBUG] Sende karte_aufdecken: Reihe {row_idx}, Spalte {col_idx}")
        
        # Nachricht an Server senden
        result = serv.send_data(sock, {
            "aktion": "karte_aufdecken",
            "spieler_id": spieler_id,
            "karte": {"row": row_idx, "col": col_idx}
        })
        
        if result:
            if not hasattr(s, "cards_flipped_this_turn"):
                s.cards_flipped_this_turn = 0
            s.cards_flipped_this_turn += 1
            print(f"[DEBUG] Karte aufgedeckt, neuer Zähler: {s.cards_flipped_this_turn}")
            return True
        
        return False
    
    # Nach Ablehnung einer Nachziehstapelkarte eine eigene Karte aufdecken
    elif s.muss_karte_aufdecken and not card.is_face_up:
        serv.send_data(sock, {
            "aktion": "nachziehstapel_ablehnen",
            "spieler_id": spieler_id,
            "aufzudeckende_karte": {"row": row_idx, "col": col_idx}
        })
        s.muss_karte_aufdecken = False
        s.warte_auf_entscheidung = False
        s.gezogene_karte = None
        s.status_message = ""
        return True
    
    # Eigene Karte angeklickt für Tausch mit Ablagestapel
    elif s.tausche_mit_ablagestapel:
        print(f"Tausche Karte ({row_idx}, {col_idx}) mit Ablagestapel")
        serv.send_data(sock, {
            "aktion": "nehme_ablagestapel",
            "spieler_id": spieler_id,
            "ziel_karte": {"row": row_idx, "col": col_idx}
        })
        s.tausche_mit_ablagestapel = False
        s.status_message = ""
        return True
    
    # Eigene Karte angeklickt für Tausch mit gezogener Karte
    elif s.warte_auf_entscheidung and s.gezogene_karte is not None:
        print(f"Tausche Karte ({row_idx}, {col_idx}) mit gezogener Karte")
        serv.send_data(sock, {
            "aktion": "nachziehstapel_tauschen",
            "spieler_id": spieler_id,
            "ziel_karte": {"row": row_idx, "col": col_idx}
        })
        s.warte_auf_entscheidung = False
        s.gezogene_karte = None
        s.status_message = ""
        return True
    
    return False

# Kartenstapel-Interaktion
def handle_draw_pile_click(sock, spieler_id):
    """Verarbeitet Klicks auf den Nachziehstapel"""
    if s.current_player == spieler_id and not s.zug_begonnen and not s.warte_auf_entscheidung:
        print("Kartenstapel wurde angeklickt!")
        serv.send_data(sock, {
            "aktion": "nehme_nachziehstapel",
            "spieler_id": spieler_id
        })
        s.warte_auf_entscheidung = True
        s.zug_begonnen = True
        return True
    return False

# Ablagestapel-Interaktion
def handle_discard_pile_click(sock, spieler_id):
    """Verarbeitet Klicks auf den Ablagestapel"""
    if s.current_player == spieler_id and not s.zug_begonnen and not s.tausche_mit_ablagestapel:
        print("Ablagestapel wurde angeklickt!")
        s.tausche_mit_ablagestapel = True
        s.status_message = "Wähle eine Karte auf deinem Spielfeld zum Tauschen"
        s.zug_begonnen = True
        return True
    return False

# Ablehnen-Button
def handle_reject_button(my_layout):
    """Verarbeitet Klicks auf den Ablehnen-Button"""
    if hasattr(s, "gezogene_karte") and s.gezogene_karte is not None:
        print("Ablehnen-Button wurde geklickt!")
        # Verdeckte Karten finden
        verdeckte_karten = []
        if my_layout:
            for row_idx, row in enumerate(my_layout.cards):
                for col_idx, card in enumerate(row):
                    if not card.is_face_up:
                        verdeckte_karten.append({"row": row_idx, "col": col_idx})

        print(f"[DEBUG] Gefundene verdeckte Karten: {len(verdeckte_karten)}")
        if len(verdeckte_karten) == 0:
            # Überprüfe, ob alle Karten bereits aufgedeckt sind
            all_cards = []
            for row_idx, row in enumerate(my_layout.cards):
                for col_idx, card in enumerate(row):
                    all_cards.append({"row": row_idx, "col": col_idx, "is_face_up": card.is_face_up})
            print(f"[DEBUG] Kartenstatus: {all_cards}")

        if verdeckte_karten:
            # Zustand für das Aufdecken einer Karte setzen
            s.muss_karte_aufdecken = True
            # Status-Nachricht anzeigen
            s.status_message = "WÄHLE JETZT EINE VERDECKTE KARTE ZUM AUFDECKEN!"
            return True
        else:
            # Keine verdeckten Karten mehr
            print("Keine verdeckten Karten zum Aufdecken übrig!")
    
    return False

# Punkte berechnen
def berechne_punktzahl(layout):
    """Berechnet die Punktzahl eines Layouts"""
    punkte = 0
    for row in layout.cards:
        for card in row:
            if card.is_face_up:
                punkte += card.value
    return punkte

def check_for_column_triplets(my_layout):
    """Prüft, ob im eigenen Layout drei gleiche Karten in einer Spalte sind"""
    if not my_layout or not my_layout.cards:
        return False
    
    # Für jede Spalte
    for col in range(len(my_layout.cards[0])):
        # Werte und Status in dieser Spalte sammeln
        column_values = []
        for row in range(len(my_layout.cards)):
            card = my_layout.cards[row][col]
            if card.is_face_up and not hasattr(card, 'is_removed') or not card.is_removed:
                column_values.append(card.value)
        
        # Wenn 3 aufgedeckte Karten und alle gleich sind
        if len(column_values) == 3 and len(set(column_values)) == 1:
            return True
    
    return False




