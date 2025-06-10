import settings as s
from dictionaries import plaPosition as pl
from dictionaries import cardSetPosition as cP
# import server as serv
import pygame
pygame.init()

WINDOW = pygame.display.set_mode((s.HEIGHT, s.WIDTH))
PLAYER_FONT = pygame.font.SysFont("comicsans", s.PLAYER_SIZE)


def first_draw():
    WINDOW.fill(s.WINDOW_COLOR)

    pygame.display.flip()


def player_place_position():
    for index, (spieler_id, name) in enumerate(s.player_daten.items()):
            if index < len(pl.player_pos[s.PL_ANZAHL]):
                x_pos, y_pos = pl.player_pos[s.PL_ANZAHL][index]
                name_text = PLAYER_FONT.render(name, True, s.PLAYER_FONT_COLOR)  # Text rendern
                WINDOW.blit(name_text, (x_pos, y_pos))


def draw():
    WINDOW.fill(s.WINDOW_COLOR)

    cP.card_set_positions()
    player_place_position()
    

    pygame.display.flip()
