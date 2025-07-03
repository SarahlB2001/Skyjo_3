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
        feld_x = pl.field_pos[f]['x']
        feld_y = pl.field_pos[f]['y']
        feld_breite = pl.field_pos['size']['width']
        # Dynamische Höhe: 3 Karten + 2 Abstände
        feld_hoehe = s.ROWS * s.CARD_HEIGHT + (s.ROWS - 1) * s.gap_height
        pygame.draw.rect(
            screen, s.BLACK,
            (feld_x, feld_y, feld_breite, feld_hoehe), 2  # 2 = Rahmenstärke, kannst du anpassen
        )
    # Kartenstapel-Rechteck zeichnen
    deck_rect = pygame.Rect(
        pl.field_pos['carddeck']['x'],
        pl.field_pos['carddeck']['y'],
        pl.field_pos['carddeck']['width'],
        pl.field_pos['carddeck']['height']
    )
    pygame.draw.rect(screen, s.BLACK, deck_rect, 2)

    # Ablagestapel-Rechteck zeichnen (nur leer)
    discard_rect = pygame.Rect(
        pl.field_pos['discarddeck']['x'],
        pl.field_pos['discarddeck']['y'],
        pl.field_pos['discarddeck']['width'],
        pl.field_pos['discarddeck']['height']
    )
    pygame.draw.rect(screen, (150, 0, 0), discard_rect, 2)  # z.B. rot umrandet

    # Kartenrücken nur auf den Kartenstapel legen
    card_back = pygame.image.load("Karten_png/card_back.png")
    card_back = pygame.transform.scale(card_back, (s.CARD_WIDTH, s.CARD_HEIGHT))
    num_stack = 5
    overlap = 8
    for i in range(num_stack):
        x = deck_rect.x + deck_rect.width // 2 - s.CARD_WIDTH // 2 + i * overlap
        y = deck_rect.y + deck_rect.height // 2 - s.CARD_HEIGHT // 2 + i * overlap
        screen.blit(card_back, (x, y))

    # KEINE Karte auf den Ablagestapel legen!

    s.card_stack_rect = pygame.Rect(
        deck_rect.x + (num_stack - 1) * overlap,
        deck_rect.y + (num_stack - 1) * overlap,
        s.CARD_WIDTH, s.CARD_HEIGHT
    )
    s.discard_stack_rect = discard_rect


def card_set_positions(screen):
    print("[DEBUG] card_set_positions wurde aufgerufen")
    global player_cardlayouts
    player_cardlayouts = {}

    fields = player_fields.get(s.player_count, [])
    for idx, f in enumerate(fields, 1):
        # Matrix vom Server verwenden!
        matrix = None
        if hasattr(s, "karten_matrizen"):
            # Keys können int oder str sein
            if isinstance(list(s.karten_matrizen.keys())[0], int):
                matrix = s.karten_matrizen.get(idx)
            else:
                matrix = s.karten_matrizen.get(str(idx))
        if matrix is None:
            # Fallback: Dummy-Matrix falls noch keine Daten da sind
            matrix = [[0 for _ in range(s.COLS)] for _ in range(s.ROWS)]
        player_cardlayouts[idx] = l.CardLayout(pl.field_pos[f]['x'], pl.field_pos[f]['y'], idx, matrix)

    # Kartenstapel zeichnen
    pygame.draw.rect(
        screen, s.BLACK,
        (pl.field_pos['carddeck']['x'], pl.field_pos['carddeck']['y'],
         pl.field_pos['carddeck']['width'], pl.field_pos['carddeck']['height'])
    )

    for layout in player_cardlayouts.values():
        layout.draw(screen)

