import settings as s
import surface as su
from dictionaries import plaPosition as pl
import pygame
import layout as l

player_cardlayouts = {}

# Position von den Plätzen auf dem Spielfeld

def card_place_position():
    if s.PL_ANZAHL == 2:
        pygame.draw.rect(su.WINDOW, s.BLACK, (pl.field_pos['1'] ['x'], pl.field_pos['1'] ['y'], pl.field_pos['size'] ['width'], pl.field_pos['size'] ['height']))
        pygame.draw.rect(su.WINDOW, s.BLACK, (pl.field_pos['3'] ['x'], pl.field_pos['3'] ['y'], pl.field_pos['size'] ['width'], pl.field_pos['size'] ['height']))
    elif s.PL_ANZAHL == 3:
        pygame.draw.rect(su.WINDOW, s.BLACK, (pl.field_pos['1'] ['x'], pl.field_pos['1'] ['y'], pl.field_pos['size'] ['width'], pl.field_pos['size'] ['height']))
        pygame.draw.rect(su.WINDOW, s.BLACK, (pl.field_pos['3'] ['x'], pl.field_pos['3'] ['y'], pl.field_pos['size'] ['width'], pl.field_pos['size'] ['height']))
        pygame.draw.rect(su.WINDOW, s.BLACK, (pl.field_pos['5'] ['x'], pl.field_pos['5'] ['y'], pl.field_pos['size'] ['width'], pl.field_pos['size'] ['height']))
    elif s.PL_ANZAHL == 4:
        pygame.draw.rect(su.WINDOW, s.BLACK, (pl.field_pos['1'] ['x'], pl.field_pos['1'] ['y'], pl.field_pos['size'] ['width'], pl.field_pos['size'] ['height']))
        pygame.draw.rect(su.WINDOW, s.BLACK, (pl.field_pos['3'] ['x'], pl.field_pos['3'] ['y'], pl.field_pos['size'] ['width'], pl.field_pos['size'] ['height']))
        pygame.draw.rect(su.WINDOW, s.BLACK, (pl.field_pos['4'] ['x'], pl.field_pos['4'] ['y'], pl.field_pos['size'] ['width'], pl.field_pos['size'] ['height']))
        pygame.draw.rect(su.WINDOW, s.BLACK, (pl.field_pos['6'] ['x'], pl.field_pos['6'] ['y'], pl.field_pos['size'] ['width'], pl.field_pos['size'] ['height']))
    elif s.PL_ANZAHL == 5:
        pygame.draw.rect(su.WINDOW, s.BLACK, (pl.field_pos['1'] ['x'], pl.field_pos['1'] ['y'], pl.field_pos['size'] ['width'], pl.field_pos['size'] ['height']))
        pygame.draw.rect(su.WINDOW, s.BLACK, (pl.field_pos['3'] ['x'], pl.field_pos['3'] ['y'], pl.field_pos['size'] ['width'], pl.field_pos['size'] ['height']))
        pygame.draw.rect(su.WINDOW, s.BLACK, (pl.field_pos['4'] ['x'], pl.field_pos['4'] ['y'], pl.field_pos['size'] ['width'], pl.field_pos['size'] ['height']))
        pygame.draw.rect(su.WINDOW, s.BLACK, (pl.field_pos['5'] ['x'], pl.field_pos['5'] ['y'], pl.field_pos['size'] ['width'], pl.field_pos['size'] ['height']))
        pygame.draw.rect(su.WINDOW, s.BLACK, (pl.field_pos['6'] ['x'], pl.field_pos['6'] ['y'], pl.field_pos['size'] ['width'], pl.field_pos['size'] ['height']))
    elif s.PL_ANZAHL == 6:
        pygame.draw.rect(su.WINDOW, s.BLACK, (pl.field_pos['1'] ['x'], pl.field_pos['1'] ['y'], pl.field_pos['size'] ['width'], pl.field_pos['size'] ['height']))
        pygame.draw.rect(su.WINDOW, s.BLACK, (pl.field_pos['2'] ['x'], pl.field_pos['2'] ['y'], pl.field_pos['size'] ['width'], pl.field_pos['size'] ['height']))
        pygame.draw.rect(su.WINDOW, s.BLACK, (pl.field_pos['3'] ['x'], pl.field_pos['3'] ['y'], pl.field_pos['size'] ['width'], pl.field_pos['size'] ['height']))
        pygame.draw.rect(su.WINDOW, s.BLACK, (pl.field_pos['4'] ['x'], pl.field_pos['4'] ['y'], pl.field_pos['size'] ['width'], pl.field_pos['size'] ['height']))
        pygame.draw.rect(su.WINDOW, s.BLACK, (pl.field_pos['6'] ['x'], pl.field_pos['6'] ['y'], pl.field_pos['size'] ['width'], pl.field_pos['size'] ['height']))
        pygame.draw.rect(su.WINDOW, s.BLACK, (pl.field_pos['5'] ['x'], pl.field_pos['5'] ['y'], pl.field_pos['size'] ['width'], pl.field_pos['size'] ['height']))

    pygame.draw.rect(su.WINDOW, s.BLACK, (pl.field_pos['carddeck'] ['x'], pl.field_pos['carddeck'] ['y'], pl.field_pos['carddeck'] ['width'], pl.field_pos['carddeck'] ['height']))


def card_set_positions():
    global player_cardlayouts
    player_cardlayouts = {}  # immer neu anlegen

    if s.PL_ANZAHL == 2:
        player_cardlayouts[1] = l.CardLayout(pl.field_pos['1']['x'], pl.field_pos['1']['y'])
        player_cardlayouts[2] = l.CardLayout(pl.field_pos['3']['x'], pl.field_pos['3']['y'])
    elif s.PL_ANZAHL == 3:
        player_cardlayouts[1] = l.CardLayout(pl.field_pos['1']['x'], pl.field_pos['1']['y'])
        player_cardlayouts[2] = l.CardLayout(pl.field_pos['3']['x'], pl.field_pos['3']['y'])
        player_cardlayouts[3] = l.CardLayout(pl.field_pos['5']['x'], pl.field_pos['5']['y'])
    elif s.PL_ANZAHL == 4:
        player_cardlayouts[1] = l.CardLayout(pl.field_pos['1']['x'], pl.field_pos['1']['y'])
        player_cardlayouts[2] = l.CardLayout(pl.field_pos['3']['x'], pl.field_pos['3']['y'])
        player_cardlayouts[3] = l.CardLayout(pl.field_pos['4']['x'], pl.field_pos['4']['y'])
        player_cardlayouts[4] = l.CardLayout(pl.field_pos['6']['x'], pl.field_pos['6']['y'])
    elif s.PL_ANZAHL == 5:
        player_cardlayouts[1] = l.CardLayout(pl.field_pos['1']['x'], pl.field_pos['1']['y'])
        player_cardlayouts[2] = l.CardLayout(pl.field_pos['3']['x'], pl.field_pos['3']['y'])
        player_cardlayouts[3] = l.CardLayout(pl.field_pos['4']['x'], pl.field_pos['4']['y'])
        player_cardlayouts[4] = l.CardLayout(pl.field_pos['5']['x'], pl.field_pos['5']['y'])
        player_cardlayouts[5] = l.CardLayout(pl.field_pos['6']['x'], pl.field_pos['6']['y'])
    elif s.PL_ANZAHL == 6:
        player_cardlayouts[1] = l.CardLayout(pl.field_pos['1']['x'], pl.field_pos['1']['y'])
        player_cardlayouts[2] = l.CardLayout(pl.field_pos['2']['x'], pl.field_pos['2']['y'])
        player_cardlayouts[3] = l.CardLayout(pl.field_pos['3']['x'], pl.field_pos['3']['y'])
        player_cardlayouts[4] = l.CardLayout(pl.field_pos['4']['x'], pl.field_pos['4']['y'])
        player_cardlayouts[5] = l.CardLayout(pl.field_pos['6']['x'], pl.field_pos['6']['y'])
        player_cardlayouts[6] = l.CardLayout(pl.field_pos['5']['x'], pl.field_pos['5']['y'])

    pygame.draw.rect(su.WINDOW, s.BLACK, (pl.field_pos['carddeck'] ['x'], pl.field_pos['carddeck'] ['y'], pl.field_pos['carddeck'] ['width'], pl.field_pos['carddeck'] ['height']))

    for layout in player_cardlayouts.values():
        layout.draw(su.WINDOW)
