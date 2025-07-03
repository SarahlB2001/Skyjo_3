import settings as s
import surface as su
from dictionaries import plaPosition as pl
import pygame
import layout as l

player_fields = {
    2: ['1', '3'],
    3: ['1', '3', '5'],
    4: ['1', '3', '4', '6'],
    5: ['1', '3', '4', '5', '6'],
    6: ['1', '2', '3', '4', '5', '6']
}

player_cardlayouts = {}

# Position von den Plätzen auf dem Spielfeld

def card_place_position(screen):
    fields = player_fields.get(s.player_count, [])
    for f in fields:
        pygame.draw.rect(
            screen, s.BLACK,
            (pl.field_pos[f]['x'], pl.field_pos[f]['y'],
             pl.field_pos['size']['width'], pl.field_pos['size']['height'])
        )
    # Kartenstapel-Rechteck zeichnen
    deck_rect = pygame.Rect(
        pl.field_pos['carddeck']['x'],
        pl.field_pos['carddeck']['y'],
        pl.field_pos['carddeck']['width'],
        pl.field_pos['carddeck']['height']
    )
    pygame.draw.rect(screen, s.BLACK, deck_rect, 2)

    # Mehrere Kartenrücken überlappend zeichnen
    card_back = pygame.image.load("Karten_png/card_back.png")
    card_back = pygame.transform.scale(card_back, (s.CARD_WIDTH, s.CARD_HEIGHT))
    num_stack = 5  # Anzahl Karten im Stapel
    overlap = 8    # Wie stark die Karten überlappen (Pixel)
    stack_rects = []
    for i in range(num_stack):
        x = deck_rect.x + deck_rect.width // 2 - s.CARD_WIDTH // 2 + i * overlap
        y = deck_rect.y + deck_rect.height // 2 - s.CARD_HEIGHT // 2 + i * overlap
        screen.blit(card_back, (x, y))
        stack_rects.append(pygame.Rect(x, y, s.CARD_WIDTH, s.CARD_HEIGHT))
    # Den vordersten Kartenrücken (oberste Karte) als "anklickbar" merken:
    s.card_stack_rect = stack_rects[-1]


def card_set_positions(screen):
    print("[DEBUG] card_set_positions wurde aufgerufen")
    global player_cardlayouts
    player_cardlayouts = {}  # immer neu anlegen

    fields = player_fields.get(s.player_count, [])
    for idx, f in enumerate(fields, 1):
        player_cardlayouts[idx] = l.CardLayout(pl.field_pos[f]['x'], pl.field_pos[f]['y'])

    # Kartenstapel zeichnen
    pygame.draw.rect(
        screen, s.BLACK,
        (pl.field_pos['carddeck']['x'], pl.field_pos['carddeck']['y'],
         pl.field_pos['carddeck']['width'], pl.field_pos['carddeck']['height'])
    )

    for layout in player_cardlayouts.values():
        layout.draw(screen)
