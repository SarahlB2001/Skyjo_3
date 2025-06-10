import pygame
import cards as card
import stack as st
import settings as s
#__________________________________________________
# Erste Runde

def erste_runde(spieler_anzahl):
    stapel = st.create_stack()    # Kartenstapel erstellen
    
    # Karten verteilen
    spieler_karten = {}
    for spieler in range(spieler_anzahl):
        spieler_karten[spieler] = stapel[:12]  # Ziehe die ersten 12 Karten
        del stapel[:12]  # Entferne die gezogenen Karten aus dem Stapel
        
    # Oberste Karte des Stapels aufdecken
    offene_karte = stapel.pop()
    
    # Spieler wählen 2 Karten aus
    #ERST MÖGLICH WENN WIR WISSEN WO wELCHE kARTE LIEGT 
    # Variablen Name für die zwei aufgedeckten karten jedes Spielers: "offene_karten"
    offene_karten = {}
    for spieler in range(spieler_anzahl):
        offene_karten[spieler] = [spieler_karten[spieler][0], spieler_karten[spieler][1]]
    

    # Beginner auswählen: Spieler mit der höchsten Punktzahl
    punkte = {spieler: card.calculate_points(offene_karten[spieler]) for spieler in offene_karten}
    beginner = max(punkte, key=punkte.get)
    print(f"Spieler {beginner} beginnt mit der höchsten Punktzahl: {punkte[beginner]}")

    return spieler_karten, offene_karte, stapel, beginner,offene_karten

#_____________________________________________________
# Hauptschleife (Loop 1!)

# Immer der Spieler, der aktuell dran ist : Loop 1.2 (in Loop 1)

    # Karte von stapel oder offene Karte ziehen (Wählen mit Stapel)

    # Auswählen: Karte nicht behalten oder Tauschen + Auswahl der Tauschkarte/Aufdeckkarte

    # Überprüfen ob in einer Spalte 3 Gleiche -> reihe verschwindet

# Überprüfen ob ein Spieler alle Karten aufgedeckt hat, wenn ja noch 1 runde, dann end loop


#________________________________________________________
# Ergebnis

# Karten Punkte zusammenzählen

# gewinner ermitteln

# Punktestand anzeigen

# Überprüfen ob Rundenanzahl erreicht, wenn ja Endstand Tabelle, wenn nein runde neu Starten. Beginner auswahl: derjenige der Aufgedeckt hat
# Loop 1 neu starten
