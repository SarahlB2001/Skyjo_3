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
    # Kartenstapel immer zeichnen
    pygame.draw.rect(
        screen, s.BLACK,
        (pl.field_pos['carddeck']['x'], pl.field_pos['carddeck']['y'],
         pl.field_pos['carddeck']['width'], pl.field_pos['carddeck']['height'])
    )


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
