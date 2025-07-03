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

WINDOW = pygame.display.set_mode((s.HEIGHT, s.WIDTH)) 
PLAYER_FONT = pygame.font.SysFont("comicsans", s.PLAYER_SIZE)


def first_draw():
    WINDOW.fill(s.WINDOW_COLOR)

    pygame.display.flip()

''''
def player_place_position():
    for index, (spieler_id, name) in enumerate(s.player_daten.items()):
        if index < len(pl.player_pos[s.player_count]):
            x_pos, y_pos = pl.player_pos[s.player_count][index]
            name_text = PLAYER_FONT.render(name, True, s.PLAYER_FONT_COLOR)
            WINDOW.blit(name_text, (x_pos, y_pos))

        '''

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

'''''
def calculate_gaps (size_x, size_y, cols, rows, card_width, card_height):
    gap_width = (size_x - (cols * card_width)) / (cols + 1) ##################################
    gap_height = (size_y - (rows * card_height)) / (rows + 1)
    s.gap_width = gap_width
    s.gap_height = gap_height
    # return gap_width, gap_height

calculate_gaps(pl.size['width'], pl.size['height'], s.COLS, s.ROWS, s.CARD_WIDTH, s.CARD_HEIGHT)

'''
def player_place_position():
    for index, (spieler_id, name) in enumerate(s.player_daten.items()):
        if index < len(pl.player_pos[s.player_count]):
            x_pos, y_pos = pl.player_pos[s.player_count][index]
            name_text = PLAYER_FONT.render(name, True, s.PLAYER_FONT_COLOR)
            WINDOW.blit(name_text, (x_pos, y_pos))


def draw(screen):
    screen.fill(s.WINDOW_COLOR)
    cP.card_place_position(screen)

    # Spielerfelder und Namen zeichnen
    fields = cP.player_fields.get(s.player_count, [])
    namen = [s.player_data.get(i, f"Spieler{i}") for i in range(1, s.player_count + 1)]

    for idx, f in enumerate(fields):
        rect = pl.field_pos[f]
        if idx < len(namen):
            name = namen[idx]
            layout = cP.player_cardlayouts.get(idx + 1)
            punkte = 0
            if layout:
                punkte = sum(card.value for row in layout.cards for card in row if card.is_face_up)
            # Abstand zwischen Name und Score
            name_color = (0, 0, 255) if (idx + 1) == s.spieler_id else s.PLAYER_FONT_COLOR
            name_text = PLAYER_FONT.render(name, True, name_color)
            score_text = PLAYER_FONT.render(f"   Score: {punkte}", True, s.PLAYER_FONT_COLOR)
            # Name und Score nebeneinander mit Abstand
            name_rect = name_text.get_rect()
            score_rect = score_text.get_rect()
            total_width = name_rect.width + 30 + score_rect.width  # 30px Abstand
            x_start = rect['x'] + pl.field_pos['size']['width']//2 - total_width//2
            y_pos = rect['y'] - 28 
            screen.blit(name_text, (x_start, y_pos))
            screen.blit(score_text, (x_start + name_rect.width + 30, y_pos))

    for layout in cP.player_cardlayouts.values():
        layout.draw(screen)
    pygame.display.flip()
