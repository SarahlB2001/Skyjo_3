import settings as s
from dictionaries import plaPosition as pl
from dictionaries import cardSetPosition as cP
import pygame
import layout as l
import time

player_fields = {
    2: ['1', '3'],
    3: ['1', '3', '5'],
    4: ['1', '3', '4', '5', '6'],
    5: ['1', '3', '4', '5', '6'],
    6: ['1', '2', '3', '4', '5', '6']
}

# Move these global variables to initialization function
WINDOW = None
PLAYER_FONT = None
BACKGROUND_IMAGE = None

# Add initialization function
def initialize():
    global WINDOW, PLAYER_FONT, BACKGROUND_IMAGE
    WINDOW = pygame.display.set_mode((s.HEIGHT, s.WIDTH))
    PLAYER_FONT = pygame.font.SysFont("comicsans", s.PLAYER_SIZE)
    BACKGROUND_IMAGE = pygame.image.load("sky.jpg")
    BACKGROUND_IMAGE = pygame.transform.scale(BACKGROUND_IMAGE, (s.HEIGHT, s.WIDTH))

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
    screen.blit(BACKGROUND_IMAGE, (0, 0))
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
            
            # Farbe bestimmen
            name_color = (0, 0, 255) if (idx + 1) == s.spieler_id else s.PLAYER_FONT_COLOR
            name_text = PLAYER_FONT.render(name, True, name_color)
            score_text = PLAYER_FONT.render(f"   Score: {punkte}", True, s.PLAYER_FONT_COLOR)
            
            # Position berechnen
            name_rect = name_text.get_rect()
            score_rect = score_text.get_rect()
            total_width = name_rect.width + 30 + score_rect.width
            x_start = rect['x'] + pl.field_pos['size']['width']//2 - total_width//2
            y_pos = rect['y'] - 28
            
            # Grüner Punkt für aktuellen Spieler
          #  print(f"[DEBUG] Prüfe current_player: {getattr(s, 'current_player', 'NICHT GESETZT')}")
            if hasattr(s, 'current_player') and s.current_player == (idx + 1):
              #  print(f"[DEBUG] Zeichne grünen Punkt für Spieler {s.current_player} an Position ({x_start - 20}, {y_pos + 10})")
                pygame.draw.circle(screen, (0, 255, 0), (x_start - 20, y_pos + 10), 8)  # Grüner Punkt
            
            screen.blit(name_text, (x_start, y_pos))
            screen.blit(score_text, (x_start + name_rect.width + 30, y_pos))

    for layout in cP.player_cardlayouts.values():
        layout.draw(screen)

    # Gezogene Karte anzeigen, wenn vorhanden
    if hasattr(s, "gezogene_karte") and s.gezogene_karte is not None:
        card_img = pygame.image.load(f"Karten_png/card_{s.gezogene_karte}.png")
        card_img = pygame.transform.scale(card_img, (s.CARD_WIDTH * 1.5, s.CARD_HEIGHT * 1.5))
        x = screen.get_width() // 2 - card_img.get_width() // 2
        y = screen.get_height() // 2 - card_img.get_height() // 2
        screen.blit(card_img, (x, y))
        
        # Ablehnen-Button über den Stapeln
        button_width = 120
        button_height = 40
        button_x = screen.get_width() // 2 - button_width // 2
        button_y = pl.field_pos['carddeck']['y'] - button_height - 10  # 10px Abstand über den Stapeln
        
        # Button-Rechteck zeichnen
        ablehnen_button = pygame.Rect(button_x, button_y, button_width, button_height)
        pygame.draw.rect(screen, (255, 0, 0), ablehnen_button)  # Roter Button
        
        # Button-Text
        font = pygame.font.SysFont(None, 30)
        button_text = font.render("Ablehnen", True, (255, 255, 255))  # Weißer Text
        screen.blit(button_text, (button_x + button_width // 2 - button_text.get_width() // 2, 
                                 button_y + button_height // 2 - button_text.get_height() // 2))
        
        # Button-Rechteck in settings speichern für Klick-Erkennung
        s.ablehnen_button_rect = ablehnen_button
        
        # Tauschoption anzeigen
        font = pygame.font.SysFont(None, 22)  
        text = font.render("Klicke auf eine Karte zum Tauschen oder auf 'Ablehnen'", True, (0, 0, 0))
        screen.blit(text, (screen.get_width() // 2 - text.get_width() // 2, button_y - 30))

    # Statusnachricht nur für nicht-aktive Spieler anzeigen
    if s.status_message and s.current_player != s.spieler_id:
        font = pygame.font.SysFont(None, 22)  # Kleinere Schriftgröße (war 30)
        text = font.render(s.status_message, True, (0, 0, 0))
        screen.blit(text, (screen.get_width() // 2 - text.get_width() // 2, 10))

    # Spielanweisungen für den aktiven Spieler oder Karte aufdecken
    if s.current_player == s.spieler_id:
        font = pygame.font.SysFont(None, 22)  # Konsistente Schriftgröße
        
        if hasattr(s, "muss_karte_aufdecken") and s.muss_karte_aufdecken:
            # Aufdecken-Nachricht hat Priorität über andere Anweisungen
            text = font.render("WÄHLE EINE VERDECKTE KARTE ZUM AUFDECKEN", True, (255, 0, 0))
        elif hasattr(s, "tausche_mit_ablagestapel") and s.tausche_mit_ablagestapel:
            # Nachricht für Tausch mit Ablagestapel
            text = font.render("Wähle eine Karte auf deinem Spielfeld zum Tauschen", True, (0, 0, 0))
        elif not s.zug_begonnen:
            # Standard-Spielanweisung
            text = font.render("WÄHLE: Entweder Karte vom Ablagestapel ODER vom Nachziehstapel", True, (0, 0, 0))
        else:
            # Kein Text, wenn der Zug bereits begonnen hat
            text = None
        
        if text:
            screen.blit(text, (screen.get_width() // 2 - text.get_width() // 2, 10))
            
    # Anzeige für Dreierkombinationen (temporäre Meldung)
    if hasattr(s, "triplet_removal_time") and time.time() - s.triplet_removal_time < 3:
        # Text im gleichen Format wie andere Nachrichten
        font = pygame.font.SysFont(None, 22)
        text = font.render(s.triplet_message, True, (0, 0, 0))
        
        # An der gleichen Position wie andere Nachrichten
        screen.blit(text, (screen.get_width() // 2 - text.get_width() // 2, 10))
        
        # Benachrichtigung nach Ablauf der Zeit entfernen
        if time.time() - s.triplet_removal_time >= 2.0:
            try:
                # Debug-Ausgabe hinzufügen
                print("[DEBUG] Entferne Triplet-Benachrichtigung")
                # Attribute explizit auf None setzen und dann entfernen
                s.triplet_removal_time = None
                s.triplet_message = None
                delattr(s, "triplet_removal_time")
                delattr(s, "triplet_message")
            except Exception as e:
                print(f"[ERROR] Fehler beim Entfernen der Triplet-Attribute: {e}")
