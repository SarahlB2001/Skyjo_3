import settings as s
from dictionaries import plaPosition as pl
from dictionaries import cardSetPosition as cP
# import server as serv
import pygame
pygame.init()
import layout as l


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

def calculate_gaps (size_x, size_y, cols, rows, card_width, card_height):
    gap_width = size_x // 5
    gap_height = (size_y - (rows * card_height)) / (rows + 1)
    s.gap_width = gap_width
    s.gap_height = gap_height
    # return gap_width, gap_height

calculate_gaps(pl.size['width'], pl.size['height'], s.COLS, s.ROWS, s.CARD_WIDTH, s.CARD_HEIGHT)
    

def player_place_position():
    for index, (spieler_id, name) in enumerate(s.player_daten.items()):
            if index < len(pl.player_pos[s.PL_ANZAHL]):
                x_pos, y_pos = pl.player_pos[s.PL_ANZAHL][index]
                name_text = PLAYER_FONT.render(name, True, s.PLAYER_FONT_COLOR)  # Text rendern
                WINDOW.blit(name_text, (x_pos, y_pos))

def calculate_gaps (size_x, size_y, cols, rows, card_width, card_height):
    gap_width = size_x // 4
    gap_height = (size_y - (rows * card_height)) / (rows + 1)
    s.gap_width = gap_width
    s.gap_height = gap_height
    # return gap_width, gap_height

calculate_gaps(pl.size['width'], pl.size['height'], s.COLS, s.ROWS, s.CARD_WIDTH, s.CARD_HEIGHT)

def draw():
    WINDOW.fill(s.WINDOW_COLOR)


    cP.card_set_positions()
    player_place_position()

    pygame.display.flip()
