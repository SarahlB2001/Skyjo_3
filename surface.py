import settings as s
from dictionaries import plaPosition as pl
# import server as serv
import pygame
pygame.init()


def first_draw():
    s.WINDOW.fill(s.WINDOW_COLOR)

    pygame.display.flip()

def card_place_position():
    if s.PL_ANZAHL == 2:
        pygame.draw.rect(s.WINDOW, s.BLACK, (pl.field_pos['1'] ['x'], pl.field_pos['1'] ['y'], pl.field_pos['size'] ['width'], pl.field_pos['size'] ['height']))
        pygame.draw.rect(s.WINDOW, s.BLACK, (pl.field_pos['3'] ['x'], pl.field_pos['3'] ['y'], pl.field_pos['size'] ['width'], pl.field_pos['size'] ['height']))
    elif s.PL_ANZAHL == 3:
        pygame.draw.rect(s.WINDOW, s.BLACK, (pl.field_pos['1'] ['x'], pl.field_pos['1'] ['y'], pl.field_pos['size'] ['width'], pl.field_pos['size'] ['height']))
        pygame.draw.rect(s.WINDOW, s.BLACK, (pl.field_pos['3'] ['x'], pl.field_pos['3'] ['y'], pl.field_pos['size'] ['width'], pl.field_pos['size'] ['height']))
        pygame.draw.rect(s.WINDOW, s.BLACK, (pl.field_pos['5'] ['x'], pl.field_pos['5'] ['y'], pl.field_pos['size'] ['width'], pl.field_pos['size'] ['height']))
    elif s.PL_ANZAHL == 4:
        pygame.draw.rect(s.WINDOW, s.BLACK, (pl.field_pos['1'] ['x'], pl.field_pos['1'] ['y'], pl.field_pos['size'] ['width'], pl.field_pos['size'] ['height']))
        pygame.draw.rect(s.WINDOW, s.BLACK, (pl.field_pos['3'] ['x'], pl.field_pos['3'] ['y'], pl.field_pos['size'] ['width'], pl.field_pos['size'] ['height']))
        pygame.draw.rect(s.WINDOW, s.BLACK, (pl.field_pos['4'] ['x'], pl.field_pos['4'] ['y'], pl.field_pos['size'] ['width'], pl.field_pos['size'] ['height']))
        pygame.draw.rect(s.WINDOW, s.BLACK, (pl.field_pos['6'] ['x'], pl.field_pos['6'] ['y'], pl.field_pos['size'] ['width'], pl.field_pos['size'] ['height']))
    elif s.PL_ANZAHL == 5:
        pygame.draw.rect(s.WINDOW, s.BLACK, (pl.field_pos['1'] ['x'], pl.field_pos['1'] ['y'], pl.field_pos['size'] ['width'], pl.field_pos['size'] ['height']))
        pygame.draw.rect(s.WINDOW, s.BLACK, (pl.field_pos['3'] ['x'], pl.field_pos['3'] ['y'], pl.field_pos['size'] ['width'], pl.field_pos['size'] ['height']))
        pygame.draw.rect(s.WINDOW, s.BLACK, (pl.field_pos['4'] ['x'], pl.field_pos['4'] ['y'], pl.field_pos['size'] ['width'], pl.field_pos['size'] ['height']))
        pygame.draw.rect(s.WINDOW, s.BLACK, (pl.field_pos['5'] ['x'], pl.field_pos['5'] ['y'], pl.field_pos['size'] ['width'], pl.field_pos['size'] ['height']))
        pygame.draw.rect(s.WINDOW, s.BLACK, (pl.field_pos['6'] ['x'], pl.field_pos['6'] ['y'], pl.field_pos['size'] ['width'], pl.field_pos['size'] ['height']))
    elif s.PL_ANZAHL == 6:
        pygame.draw.rect(s.WINDOW, s.BLACK, (pl.field_pos['1'] ['x'], pl.field_pos['1'] ['y'], pl.field_pos['size'] ['width'], pl.field_pos['size'] ['height']))
        pygame.draw.rect(s.WINDOW, s.BLACK, (pl.field_pos['2'] ['x'], pl.field_pos['2'] ['y'], pl.field_pos['size'] ['width'], pl.field_pos['size'] ['height']))
        pygame.draw.rect(s.WINDOW, s.BLACK, (pl.field_pos['3'] ['x'], pl.field_pos['3'] ['y'], pl.field_pos['size'] ['width'], pl.field_pos['size'] ['height']))
        pygame.draw.rect(s.WINDOW, s.BLACK, (pl.field_pos['4'] ['x'], pl.field_pos['4'] ['y'], pl.field_pos['size'] ['width'], pl.field_pos['size'] ['height']))
        pygame.draw.rect(s.WINDOW, s.BLACK, (pl.field_pos['6'] ['x'], pl.field_pos['6'] ['y'], pl.field_pos['size'] ['width'], pl.field_pos['size'] ['height']))
        pygame.draw.rect(s.WINDOW, s.BLACK, (pl.field_pos['5'] ['x'], pl.field_pos['5'] ['y'], pl.field_pos['size'] ['width'], pl.field_pos['size'] ['height']))

    pygame.draw.rect(s.WINDOW, s.BLACK, (pl.field_pos['carddeck'] ['x'], pl.field_pos['carddeck'] ['y'], pl.field_pos['carddeck'] ['width'], pl.field_pos['carddeck'] ['height']))


def player_place_position():
    for index, (spieler_id, name) in enumerate(s.player_daten.items()):
            if index < len(pl.player_pos[s.PL_ANZAHL]):
                x_pos, y_pos = pl.player_pos[s.PL_ANZAHL][index]
                name_text = s.PLAYER_FONT.render(name, True, s.PLAYER_FONT_COLOR)  # Text rendern
                s.WINDOW.blit(name_text, (x_pos, y_pos))


def draw():
    s.WINDOW.fill(s.WINDOW_COLOR)

    card_place_position()
    player_place_position()
    

    pygame.display.flip()
