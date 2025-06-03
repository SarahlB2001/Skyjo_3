import settings as s
from dictionaries import plaPosition as pl
# from dictionaries import Spieler_Spielername as pln
# import server as serv
import pygame
pygame.init()


def first_draw():
    s.WINDOW.fill(s.WINDOW_COLOR)

    pygame.display.flip()


def draw(player_name):
    s.WINDOW.fill(s.WINDOW_COLOR)

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
        pygame.draw.rect(s.WINDOW, s.BLACK, (pl.field_pos['6'] ['x'], pl.field_pos['6'] ['y'], pl.field_pos['size'] ['width'], pl.field_pos['size'] ['height']))
        pygame.draw.rect(s.WINDOW, s.BLACK, (pl.field_pos['5'] ['x'], pl.field_pos['5'] ['y'], pl.field_pos['size'] ['width'], pl.field_pos['size'] ['height']))
    elif s.PL_ANZAHL == 6:
        pygame.draw.rect(s.WINDOW, s.BLACK, (pl.field_pos['1'] ['x'], pl.field_pos['1'] ['y'], pl.field_pos['size'] ['width'], pl.field_pos['size'] ['height']))
        pygame.draw.rect(s.WINDOW, s.BLACK, (pl.field_pos['2'] ['x'], pl.field_pos['2'] ['y'], pl.field_pos['size'] ['width'], pl.field_pos['size'] ['height']))
        pygame.draw.rect(s.WINDOW, s.BLACK, (pl.field_pos['3'] ['x'], pl.field_pos['3'] ['y'], pl.field_pos['size'] ['width'], pl.field_pos['size'] ['height']))
        pygame.draw.rect(s.WINDOW, s.BLACK, (pl.field_pos['4'] ['x'], pl.field_pos['4'] ['y'], pl.field_pos['size'] ['width'], pl.field_pos['size'] ['height']))
        pygame.draw.rect(s.WINDOW, s.BLACK, (pl.field_pos['6'] ['x'], pl.field_pos['6'] ['y'], pl.field_pos['size'] ['width'], pl.field_pos['size'] ['height']))
        pygame.draw.rect(s.WINDOW, s.BLACK, (pl.field_pos['5'] ['x'], pl.field_pos['5'] ['y'], pl.field_pos['size'] ['width'], pl.field_pos['size'] ['height']))

    pygame.draw.rect(s.WINDOW, s.BLACK, (pl.field_pos['carddeck'] ['x'], pl.field_pos['carddeck'] ['y'], pl.field_pos['carddeck'] ['width'], pl.field_pos['carddeck'] ['height']))

    player_text = s.PLAYER_FONT.render(player_name, 1, s.PLAYER_FONT_COLOR)
    s.WINDOW.blit(player_text, (s.PLAYER_X_POSITION, s.PLAYER_Y_POSITION))

    pygame.display.flip()
