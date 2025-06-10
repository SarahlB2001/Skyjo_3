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

def main_loop

# Immer der player, der aktuell dran ist : Loop 1.2 (in Loop 1)

    # Karte von deck oder offene Karte ziehen (Wählen mit deck)

    # Auswählen: Karte nicht behalten oder Tauschen + Auswahl der Tauschkarte/Aufdeckkarte

    # Überprüfen ob in einer Spalte 3 Gleiche -> reihe verschwindet

# Überprüfen ob ein player alle Karten aufgedeckt hat, wenn ja noch 1 runde, dann end loop


#________________________________________________________
# Ergebnis

# Karten Punkte zusammenzählen

# gewinner ermitteln

# Punktestand anzeigen

# Überprüfen ob Rundenanzahl erreicht, wenn ja Endstand Tabelle, wenn nein runde neu Starten. Beginner auswahl: derjenige der Aufgedeckt hat
# Loop 1 neu starten
