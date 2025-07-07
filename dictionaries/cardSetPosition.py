import settings as s
import surface as su
from dictionaries import plaPosition as pl
import pygame
import layout as l
import time  # <-- Diese Zeile hinzufügen, um das time-Modul zu importieren

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

    # Nur eine einzige Karte in der Mitte anzeigen (statt eines Stapels)
    x = deck_rect.x + deck_rect.width // 2 - s.CARD_WIDTH // 2
    y = deck_rect.y + deck_rect.height // 2 - s.CARD_HEIGHT // 2
    screen.blit(card_back, (x, y))

    # Rechteck für Klick-Erkennung aktualisieren
    s.card_stack_rect = pygame.Rect(x, y, s.CARD_WIDTH, s.CARD_HEIGHT)
    s.discard_stack_rect = discard_rect

    # Wenn eine Ablagestapelkarte existiert, zeige sie an
    if hasattr(s, "discard_card") and s.discard_card is not None:
        # Einfache Darstellung der obersten Karte
        discard_card_img = pygame.image.load(f"Karten_png/card_{s.discard_card}.png")
        discard_card_img = pygame.transform.scale(discard_card_img, (s.CARD_WIDTH, s.CARD_HEIGHT))
        
        # Position für die Karte
        discard_x = discard_rect.x + discard_rect.width // 2 - s.CARD_WIDTH // 2
        discard_y = discard_rect.y + discard_rect.height // 2 - s.CARD_HEIGHT // 2
        
        # Oberste Karte auf den Stapel zeichnen
        screen.blit(discard_card_img, (discard_x, discard_y))


def card_set_positions(screen, force_redraw=False):
    global player_cardlayouts
    if not player_cardlayouts or force_redraw:
        player_cardlayouts = {}
        fields = player_fields.get(s.player_count, [])
        for idx, f in enumerate(fields, 1):
            matrix = None
            if hasattr(s, "karten_matrizen"):
                if isinstance(list(s.karten_matrizen.keys())[0], int):
                    matrix = s.karten_matrizen.get(idx)
                else:
                    matrix = s.karten_matrizen.get(str(idx))
            if matrix is None:
                matrix = [[0 for _ in range(s.COLS)] for _ in range(s.ROWS)]
            player_cardlayouts[idx] = l.CardLayout(pl.field_pos[f]['x'], pl.field_pos[f]['y'], idx, matrix)
    # Zeichnen:
    for layout in player_cardlayouts.values():
        layout.draw(screen)

