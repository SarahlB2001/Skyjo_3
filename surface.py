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

    pygame.display.flip()
