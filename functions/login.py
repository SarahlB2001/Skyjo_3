# Anmeldung der Spieler
import pygame
import sys
import settings as s


def get_player_count(window):
    """Fragt Spieleranzahl (2-4) im Fenster ab"""
    font_input = pygame.font.SysFont(None, 55)
    player_count = ""
    input_active = True

    while input_active:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    if player_count.isdigit() and 2 <= int(player_count) <= 4:
                        input_active = False
                    else:
                        player_count = ""  # Ungültig → zurücksetzen
                elif event.key == pygame.K_BACKSPACE:
                    player_count = player_count[:-1]
                else:
                    player_count += event.unicode

        window.fill(s.BLACK)
        text = font_input.render("Enter number of players (2-4):", True, s.WHITE)
        window.blit(text, (s.WIDTH // 2 - text.get_width() // 2, s.HEIGHT // 2 - 50))
        count_text = font_input.render(player_count, True, s.WHITE)
        window.blit(count_text, (s.WIDTH // 2 - count_text.get_width() // 2, s.HEIGHT // 2 + 10))
        pygame.display.update()

    return int(player_count)

def get_player_name(window):
    """Fragt Spielernamen im Fenster ab"""
    font_input = pygame.font.SysFont(None, 55)
    player_name = ""
    input_active = True

    while input_active:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    if player_name != "":
                        input_active = False
                elif event.key == pygame.K_BACKSPACE:
                    player_name = player_name[:-1]
                else:
                    player_name += event.unicode

        window.fill(s.BLACK)
        input_text = font_input.render("Enter your name:", True, s.WHITE)
        window.blit(input_text, (s.WIDTH // 2 - input_text.get_width() // 2, s.HEIGHT // 2 - 50))
        name_text = font_input.render(player_name, True, s.WHITE)
        window.blit(name_text, (s.WIDTH // 2 - name_text.get_width() // 2, s.HEIGHT // 2 + 10))
        pygame.display.update()

    return player_name