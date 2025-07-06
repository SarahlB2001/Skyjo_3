import settings as s
import pygame
import sys
import surface as su

# Pygame initialisieren
pygame.init()

clock = pygame.time.Clock()

def get_player_name(window):
    """
    Zeigt ein Eingabefeld an, in dem der Spieler seinen Namen eingeben kann.
    :param window: Das Pygame-Fenster, in dem die Eingabe angezeigt wird.
    :return: Der eingegebene Spielername.
    """
    font_input = pygame.font.SysFont(None, 55)
    player_name = ""
    input_active = True

    while input_active:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:  # Enter-Taste
                    input_active = False
                elif event.key == pygame.K_BACKSPACE:  # Backspace-Taste
                    player_name = player_name[:-1]
                else:
                    player_name += event.unicode  # Zeichen zur Eingabe hinzufügen

        # Eingabetext aktualisieren
        window.fill(s.BLACK)
        input_text = font_input.render("Enter your name:", True, s.WHITE)
        window.blit(input_text, (s.WIDTH // 2 - input_text.get_width() // 2, s.HEIGHT // 2 - 50))
        name_text = font_input.render(player_name, True, s.WHITE)
        window.blit(name_text, (s.WIDTH // 2 - name_text.get_width() // 2, s.HEIGHT // 2 + 10))
        pygame.display.update()

    return player_name
    

def main():
    running = True

    # Zeichnen
    su.first_draw()

    # Spielernamen abfragen
    player_name = get_player_name(su.screen)
    print(f"Spielername: {player_name}")

    while running:
        clock.tick(s.FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Spiellogik und Zeichnen
        su.draw()


    pygame.quit()
    sys.exit()

main()
print(s.gap_width)