''' This program simulates the card game Skyjo  '''
# author: Sarah B., Antonia  H., Diedan.S, Dieja S., Marit S. 

import pygame
import sys
import settings as s
import server as serv
from functions import login as log

pygame.init()

pygame.display.set_caption("Multiplayer Spiel")


def main():
    running = True

    # Verbindung zum Server herstellen
    sock, spieler_id = serv.connect_to_server()

    # Wenn Spieler 1 → Spieleranzahl eingeben
    if spieler_id == 1:
        player_count = log.get_player_count(s.WINDOW)
        serv.send_data(sock, {"anzahl_spieler": player_count})

    # Spielernamen eingeben
    player_name = log.get_player_name(s.WINDOW)
    print(f"[INFO] Spielername: {player_name}")

    # Namen an Server senden
    serv.send_data(sock, {"name": player_name})

    while running:
        s.clock.tick(s.FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        s.WINDOW.fill(s.BLACK)
        pygame.display.update()

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()

# keine Begrenzung der Buchstaben 
# Klasse Spielstart erstellen