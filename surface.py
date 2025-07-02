import settings as s
from dictionaries import plaPosition as pl
from dictionaries import cardSetPosition as cP
# import server as serv
import pygame
pygame.init()
import layout as l

player_fields = {
    2: ['1', '3'],
    3: ['1', '3', '5'],
    4: ['1', '3', '4', '6'],
    5: ['1', '3', '4', '5', '6'],
    6: ['1', '2', '3', '4', '5', '6']
}

WINDOW = pygame.display.set_mode((s.HEIGHT, s.WIDTH)) ################################################
PLAYER_FONT = pygame.font.SysFont("comicsans", s.PLAYER_SIZE)


def first_draw():
    WINDOW.fill(s.WINDOW_COLOR)

    pygame.display.flip()


def player_place_position():
    for index, (spieler_id, name) in enumerate(s.player_daten.items()):
        if index < len(pl.player_pos[s.player_count]):
            x_pos, y_pos = pl.player_pos[s.player_count][index]
            name_text = PLAYER_FONT.render(name, True, s.PLAYER_FONT_COLOR)
            WINDOW.blit(name_text, (x_pos, y_pos))

def draw_player_names():
    fields = player_fields.get(s.player_count, [])
    for idx, (spieler_id, name) in enumerate(s.player_data.items()):
        if idx < len(fields):
            f = fields[idx]
            x = pl.field_pos[f]['x']
            y = pl.field_pos[f]['y']
            name_text = PLAYER_FONT.render(name, True, s.PLAYER_FONT_COLOR)
            text_rect = name_text.get_rect(center=(x + pl.field_pos['size']['width'] // 2, y - 25))
            WINDOW.blit(name_text, text_rect)


def calculate_gaps (size_x, size_y, cols, rows, card_width, card_height):
    gap_width = size_x // 5
    gap_height = (size_y - (rows * card_height)) / (rows + 1)
    s.gap_width = gap_width
    s.gap_height = gap_height
    # return gap_width, gap_height

calculate_gaps(pl.size['width'], pl.size['height'], s.COLS, s.ROWS, s.CARD_WIDTH, s.CARD_HEIGHT)


def player_place_position():
    for index, (spieler_id, name) in enumerate(s.player_daten.items()):
        if index < len(pl.player_pos[s.player_count]):
            x_pos, y_pos = pl.player_pos[s.player_count][index]
            name_text = PLAYER_FONT.render(name, True, s.PLAYER_FONT_COLOR)
            WINDOW.blit(name_text, (x_pos, y_pos))

def calculate_gaps (size_x, size_y, cols, rows, card_width, card_height):
    gap_width = size_x // 4
    gap_height = (size_y - (rows * card_height)) / (rows + 1)
    s.gap_width = gap_width
    s.gap_height = gap_height
    # return gap_width, gap_height

calculate_gaps(pl.size['width'], pl.size['height'], s.COLS, s.ROWS, s.CARD_WIDTH, s.CARD_HEIGHT)

def draw(screen):
    screen.fill(s.WINDOW_COLOR)
    cP.card_place_position(screen)

    # Spielerfelder und Namen zeichnen
    fields = cP.player_fields.get(s.player_count, [])
    # Sortiere Namen nach Spieler-ID (int!)
    namen = [s.player_data.get(i, f"Spieler{i}") for i in range(1, s.player_count + 1)]

    for idx, f in enumerate(fields):
        rect = pl.field_pos[f]
        if idx < len(namen):
            name = namen[idx]
            name_text = PLAYER_FONT.render(name, True, s.PLAYER_FONT_COLOR)
            text_rect = name_text.get_rect(center=(rect['x'] + pl.field_pos['size']['width']//2, rect['y'] - 20))
            screen.blit(name_text, text_rect)

    for layout in cP.player_cardlayouts.values():
        layout.draw(screen)
    pygame.display.flip()
