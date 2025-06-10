import pygame
import cards as card
import stack as st
import settings as s
#__________________________________________________
# Erste Runde

def first_round(player_anzahl):
    deck = st.create_stack()    # Kartendeck erstellen
    
    # Karten verteilen
    player_cards = {}
    for player in range(player_anzahl):
        player_cards[player] = deck[:12]  # Ziehe die ersten 12 Karten
        del deck[:12]  # Entferne die gezogenen Karten aus dem deck
        
    # Oberste Karte des decks aufdecken
    open_card = deck.pop()
    
    # player wählen 2 Karten aus
    #ERST MÖGLICH WENN WIR WISSEN WO wELCHE kARTE LIEGT 
    # Variablen Name für die zwei aufgedeckten karten jedes players: "open_cards"
    open_cards = {}
    for player in range(player_anzahl):
        open_cards[player] = [player_cards[player][0], player_cards[player][1]]
    

    # Beginner auswählen: player mit der höchsten Punktzahl
    points = {player: card.calculate_points(open_cards[player]) for player in open_cards}
    beginner = max(points, key=points.get)
    print(f"player {beginner} beginnt mit der höchsten Punktzahl: {points[beginner]}")

    return player_cards, open_card, deck, beginner,open_cards

#_____________________________________________________
# Hauptschleife (Loop 1!)

def main_loop(player_cards, open_card, deck, beginner, open_cards):
    player_anzahl = len(player_cards)
    current_player = beginner  # Start mit dem Spieler, der begonnen hat

    while True:  # aktuell Endlosschleif... 
        print(f"Player {current_player} ist am Zug.")
        
        # Spieler wählt eine Karte aus dem Deck oder die offene Karte
        selected_card = st.select_card(deck, open_card)  
        # Funktion zum Auswählen der Karte einfügen!
        
        # Spieler entscheidet, ob er die Karte behalten oder tauschen möchte
        if st.wants_to_swap(selected_card):  # Funktion zur Abfrage der Entscheidung
            swap_card = st.select_swap_card(open_cards[current_player])  # Auswahl der Tauschkarte
            open_cards[current_player].remove(swap_card)  # Entferne die Tauschkarte aus den offenen Karten
            open_cards[current_player].append(selected_card)  # Füge die ausgewählte Karte hinzu
        else:
            print(f"Player {current_player} behält die Karte {selected_card}.")
        
        # Überprüfen, ob in einer Spalte drei gleiche Karten sind
        if st.check_for_three_in_column(open_cards[current_player]):
            print(f"Player {current_player} hat drei gleiche Karten in einer Spalte! Diese Reihe verschwindet.")
            st.remove_three_in_column(open_cards[current_player])  # Entferne die drei gleichen Karten
        
        # Überprüfen, ob ein Spieler alle Karten aufgedeckt hat
        if not final_round and st.check_all_cards_face_up(open_cards[current_player]):
            print(f"Player {current_player} hat alle Karten aufgedeckt!")
            final_round = True
            final_round_counter = player_count - 1  # Alle anderen Spieler dürfen noch einmal

        elif final_round:
            final_round_counter -= 1
            if final_round_counter == 0:
                print("Letzte Runde beendet!")
                break  # Beende die Runde

        # Nächster Spieler ist am Zug
        current_player = (current_player + 1) % player_count  # Nächster Spieler

#________________________________________________________
#Logik für Rundenende und Neustart und Ergebnis

def game_loop(player_count, max_rounds):
    total_scores = {player: 0 for player in range(player_count)}
    round_number = 1 # Rundenzählung beginnt bei 1
    beginner = 0  # Startspieler der ersten Runde
    game_over = False

    while round_number <= max_rounds and not game_over:
        print(f"\n--- Runde {round_number} ---")
        player_cards, open_card, deck, beginner, open_cards = first_round(player_count)
        main_loop(player_cards, open_card, deck, beginner, open_cards) # Hauptschleife wird für die Runde gestartet

        # Karten Punkte jedes Spielers zusammenzählen
        scores = {}
        for player in range(player_count):
            scores[player] = card.calculate_points(open_cards[player])
            total_scores[player] += scores[player]
            print(f"Spieler {player} Punkte in dieser Runde: {scores[player]} (Gesamt: {total_scores[player]})")
            # Überprüfen, ob ein Spieler 100 oder mehr Punkte erreicht hat
            if total_scores[player] >= 100:
                print(f"\nSpieler {player} Hat 100 oder mehr Punkte erreicht. Spiel beendet!")
                game_over = True
        # Gewinner der Runde
        winner = min(scores, key=scores.get)
        print(f"\nGewinner der Runde {round_number}: Spieler {winner} mit {scores[winner]} Punkten!")
         # Beginner der nächsten Runde ist der, der alle Karten aufgedeckt hat (hier: winner)
        beginner = winner

        round_number += 1

    # Endstand Tabelle
    print("\n=== Endstand ===")
    for player, score in total_scores.items():
        print(f"Spieler {player}: {score} Punkte")
    overall_winner = min(total_scores, key=total_scores.get)
    print(f"\nGesamtsieger ist Spieler {overall_winner} mit {total_scores[overall_winner]} Punkten!")




