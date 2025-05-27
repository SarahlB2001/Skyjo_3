import settings as s
# from dictionaries import Spieler_Spielername as pln
# import server as serv
import pygame
pygame.init()


def first_draw():
    s.WINDOW.fill(s.WINDOW_COLOR)

    pygame.display.flip()


def draw(player_name):
    s.WINDOW.fill(s.WINDOW_COLOR)

    player_text = s.PLAYER_FONT.render(player_name, 1, s.PLAYER_FONT_COLOR)
    s.WINDOW.blit(player_text, (s.PLAYER_X_POSITION, s.PLAYER_Y_POSITION))

    # Obere Zeile Rechtecke
    pygame.draw.rect(s.WINDOW, s.BLACK, (s.WIDTH // 16, s.HEIGHT // 16, s.WIDTH // 4, s.HEIGHT // 4))
    pygame.draw.rect(s.WINDOW, s.BLACK, (s.WIDTH // 16 + s.WIDTH // 4 + s.WIDTH // 16, s.HEIGHT // 16, s.WIDTH // 4, s.HEIGHT // 4))
    pygame.draw.rect(s.WINDOW, s.BLACK, (s.WIDTH // 16 + s.WIDTH // 4 + s.WIDTH // 16 + s.WIDTH // 4 + s.WIDTH // 16, s.HEIGHT // 16, s.WIDTH // 4, s.HEIGHT // 4))

    # Untere Zeile Rechtecke
    pygame.draw.rect(s.WINDOW, s.BLACK, (s.WIDTH // 16, s.HEIGHT - s.HEIGHT//4 - s.HEIGHT//16, s.WIDTH // 4, s.HEIGHT // 4))
    pygame.draw.rect(s.WINDOW, s.BLACK, (s.WIDTH // 16 + s.WIDTH // 4 + s.WIDTH // 16, s.HEIGHT - s.HEIGHT//4 - s.HEIGHT//16, s.WIDTH // 4, s.HEIGHT // 4))
    pygame.draw.rect(s.WINDOW, s.BLACK, (s.WIDTH // 16 + s.WIDTH // 4 + s.WIDTH // 16 + s.WIDTH // 4 + s.WIDTH // 16, s.HEIGHT - s.HEIGHT//4 - s.HEIGHT//16, s.WIDTH // 4, s.HEIGHT // 4))

    # Karteneck, Nachziehstapel, Ablagestapel
    pygame.draw.rect(s.WINDOW, s.BLACK, (s.WIDTH // 2 - (s.WIDTH // 16 + s.WIDTH // 4 + s.WIDTH // 16) // 2, s.HEIGHT // 2 - (s.HEIGHT // 4) // 2, s.WIDTH // 16 + s.WIDTH // 4 + s.WIDTH // 16, s.HEIGHT // 4))

    pygame.display.flip()
