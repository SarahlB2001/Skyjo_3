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

screen = pygame.display.set_mode((s.HEIGHT, s.WIDTH))
PLAYER_FONT = pygame.font.SysFont("comicsans", s.PLAYER_SIZE)

BACKGROUND_IMAGE = pygame.image.load("sky.jpg")
BACKGROUND_IMAGE = pygame.transform.scale(BACKGROUND_IMAGE, (s.HEIGHT, s.WIDTH))

def first_draw():
    screen.fill(s.WINDOW_COLOR)

    pygame.display.flip()

def draw_player_names():
    fields = player_fields.get(s.player_count, [])
    for idx, (spieler_id, name) in enumerate(s.player_data.items()):
        if idx < len(fields):
            f = fields[idx]
            x = pl.field_pos[f]['x']
            y = pl.field_pos[f]['y']
            name_text = PLAYER_FONT.render(name, True, s.PLAYER_FONT_COLOR)
            text_rect = name_text.get_rect(center=(x + pl.field_pos['size']['width'] // 2, y - 25))
            screen.blit(name_text, text_rect)

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
            screen.blit(name_text, (x_pos, y_pos))


def draw():
    screen.blit(BACKGROUND_IMAGE, (0, 0))
    cP.card_place_position(screen)

    for layout in cP.player_cardlayouts.values():
        layout.draw(screen)

    # Punktzahlen mit vorherigen Rundenpunkten anzeigen
    fields = cP.player_fields.get(s.player_count, [])
    for idx, f in enumerate(fields):
        rect = pl.field_pos[f]
        player_id = idx + 1
        if idx < len(s.player_data):
            name = s.player_data.get(player_id, f"Spieler{player_id}")
            layout = cP.player_cardlayouts.get(player_id)
            punkte = 0
            if layout:
                # NUR aufgedeckte Karten zählen, die nicht entfernt wurden
                punkte = sum(card.value for row in layout.cards for card in row
                             if card.is_face_up and (not hasattr(card, 'is_removed') or not card.is_removed))

            # Farbe bestimmen
            name_color = (0, 0, 255) if player_id == s.spieler_id else s.PLAYER_FONT_COLOR

            # Spielername und aktuelle Punktzahl
            name_text = PLAYER_FONT.render(name, True, name_color)
            score_text = PLAYER_FONT.render(f"Score: {punkte}", True, s.PLAYER_FONT_COLOR)

            # Vorherige Rundenpunkte in lila anzeigen (für Runden > 1)
            prev_score_text = None
            if hasattr(s, "round_scores") and s.current_round > 1:
                prev_rounds_sum = 0
                for round_num in range(1, s.current_round):
                    if round_num in s.round_scores and player_id in s.round_scores[round_num]:
                        prev_rounds_sum += s.round_scores[round_num][player_id]

                if prev_rounds_sum > 0:
                    prev_score_text = PLAYER_FONT.render(f" ({prev_rounds_sum})", True, (128, 0, 128))  # Lila Farbe

            # Position berechnen
            name_rect = name_text.get_rect()
            score_rect = score_text.get_rect()
            total_width = name_rect.width + 30 + score_rect.width
            if prev_score_text:
                total_width += prev_score_text.get_width()

            x_start = rect['x'] + pl.field_pos['size']['width']//2 - total_width//2
            y_pos = rect['y'] - 28

            # Grüner Punkt für aktuellen Spieler
            if hasattr(s, 'current_player') and s.current_player == player_id:
                pygame.draw.circle(screen, (0, 255, 0), (x_start - 20, y_pos + 10), 8)

            # Zeichnen
            screen.blit(name_text, (x_start, y_pos))
            screen.blit(score_text, (x_start + name_rect.width + 30, y_pos))
            if prev_score_text:
                screen.blit(prev_score_text, (x_start + name_rect.width + 10 + score_rect.width, y_pos))

    # Zwischen Runden-Anzeige
    if hasattr(s, "between_rounds") and s.between_rounds:
        # Halbdurchsichtiger Hintergrund
        overlay = pygame.Surface((screen.get_width(), screen.get_height()))
        overlay.set_alpha(180)  # Transparenz (0-255)
        overlay.fill((240, 240, 240))  # Hellgrau
        screen.blit(overlay, (0, 0))

        font_large = pygame.font.SysFont(None, 48)
        font_medium = pygame.font.SysFont(None, 36)
        font_small = pygame.font.SysFont(None, 28)

        # Überschrift
        title = font_large.render(f"Ende der Runde {s.current_round}", True, (0, 0, 0))
        screen.blit(title, (screen.get_width()//2 - title.get_width()//2, 100))

        # Ergebnisse anzeigen
        y_pos = 180
        header = font_medium.render("Spieler             Rundenpunkte     Gesamtpunkte", True, (0, 0, 0))
        screen.blit(header, (screen.get_width()//2 - header.get_width()//2, y_pos))
        y_pos += 40

        # Sortieren nach Gesamtpunkten (niedrigste zuerst)
        sorted_players = sorted(s.total_scores.keys(), key=lambda pid: s.total_scores[pid])

        for pid in sorted_players:
            name = s.player_data.get(pid, f"Spieler {pid}")
            round_score = s.final_scores.get(pid, 0)
            total_score = s.total_scores.get(pid, 0)

            # Markierung für Rundenauslöser
            if pid == s.round_end_trigger:
                name = f"{name} *"

            player_text = font_small.render(f"{name}", True, (0, 0, 0))
            round_text = font_small.render(f"{round_score}", True, (0, 0, 0))
            total_text = font_small.render(f"{total_score}", True, (0, 0, 0))

            center_x = screen.get_width()//2
            screen.blit(player_text, (center_x - 200, y_pos))
            screen.blit(round_text, (center_x, y_pos))
            screen.blit(total_text, (center_x + 150, y_pos))

            y_pos += 30

        # Hinweis für Rundenauslöser
        if hasattr(s, "round_end_trigger"):
            trigger_name = s.player_data.get(s.round_end_trigger, f"Spieler {s.round_end_trigger}")
            if hasattr(s, "final_scores") and s.round_end_trigger in s.final_scores:
                doubled = False
                min_score = min(s.final_scores.values())
                if s.final_scores[s.round_end_trigger] > min_score:
                    doubled = True

                if doubled:
                    note = font_small.render(f"* {trigger_name} hat das Rundenende ausgelöst, aber nicht die niedrigste Punktzahl und erhält doppelte Punkte.",
                                           True, (255, 0, 0))
                else:
                    note = font_small.render(f"* {trigger_name} hat das Rundenende ausgelöst und hat die niedrigste Punktzahl.",
                                           True, (0, 150, 0))

                screen.blit(note, (screen.get_width()//2 - note.get_width()//2, y_pos + 20))

        # Weiter-Button
        button_width = 200
        button_height = 50
        button_x = screen.get_width()//2 - button_width//2
        button_y = screen.get_height() - 120

        pygame.draw.rect(screen, (0, 150, 0), (button_x, button_y, button_width, button_height))

        if hasattr(s, "current_round") and hasattr(s, "total_rounds") and s.current_round < s.total_rounds:
            button_text = font_medium.render("Nächste Runde", True, (255, 255, 255))
        else:
            button_text = font_medium.render("Spiel beenden", True, (255, 255, 255))

        screen.blit(button_text, (button_x + button_width//2 - button_text.get_width()//2,
                                 button_y + button_height//2 - button_text.get_height()//2))

        # Button-Rechteck speichern für Klick-Erkennung
        s.next_round_button = pygame.Rect(button_x, button_y, button_width, button_height)

    # Spielende-Anzeige
    if hasattr(s, "game_over") and s.game_over:
        # Halbdurchsichtiger Hintergrund
        overlay = pygame.Surface((screen.get_width(), screen.get_height()))
        overlay.set_alpha(200)  # Transparenz (0-255)
        overlay.fill((240, 240, 240))  # Hellgrau
        screen.blit(overlay, (0, 0))

        font_large = pygame.font.SysFont(None, 64)
        font_medium = pygame.font.SysFont(None, 36)
        font_small = pygame.font.SysFont(None, 28)

        # Überschrift
        title = font_large.render("Spielende", True, (0, 0, 0))
        screen.blit(title, (screen.get_width()//2 - title.get_width()//2, 100))

        # Ergebnisse anzeigen
        y_pos = 180
        header = font_medium.render("Platz     Spieler             Gesamtpunkte", True, (0, 0, 0))
        screen.blit(header, (screen.get_width()//2 - header.get_width()//2, y_pos))
        y_pos += 40

        # Sortieren nach Gesamtpunkten (niedrigste zuerst)
        sorted_players = sorted(s.total_scores.keys(), key=lambda pid: s.total_scores[pid])

        for place, pid in enumerate(sorted_players, 1):
            name = s.player_data.get(pid, f"Spieler {pid}")
            total_score = s.total_scores.get(pid, 0)

            # Gold/Silber/Bronze Farben für die ersten drei Plätze
            if place == 1:
                color = (212, 175, 55)  # Gold
            elif place == 2:
                color = (192, 192, 192)  # Silber
            elif place == 3:
                color = (205, 127, 50)  # Bronze
            else:
                color = (0, 0, 0)  # Schwarz

            place_text = font_small.render(f"{place}.", True, color)
            player_text = font_small.render(f"{name}", True, color)
            total_text = font_small.render(f"{total_score}", True, color)

            center_x = screen.get_width()//2
            screen.blit(place_text, (center_x - 150, y_pos))
            screen.blit(player_text, (center_x - 100, y_pos))
            screen.blit(total_text, (center_x + 150, y_pos))

            y_pos += 30

        # Button zum Hauptmenü zurückkehren
        button_width = 300
        button_height = 50
        button_x = screen.get_width()//2 - button_width//2
        button_y = screen.get_height() - 120

        pygame.draw.rect(screen, (0, 100, 200), (button_x, button_y, button_width, button_height))
        button_text = font_medium.render("Zurück zum Hauptmenü", True, (255, 255, 255))
        screen.blit(button_text, (button_x + button_width//2 - button_text.get_width()//2,
                                 button_y + button_height//2 - button_text.get_height()//2))

        # Button-Rechteck speichern für Klick-Erkennung
        s.main_menu_button = pygame.Rect(button_x, button_y, button_width, button_height)

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

    # Status-Nachricht anzeigen
    if hasattr(s, "status_message") and s.status_message:
        status_font = pygame.font.SysFont(None, 24)
        status_text = status_font.render(s.status_message, True, (0, 0, 0))
        screen.blit(status_text, (screen.get_width() // 2 - status_text.get_width() // 2, 30))

    # Temporäre Meldungen anzeigen (z.B. "3 gleiche Karten entfernt!")
    if hasattr(s, "temp_message") and s.temp_message:
        current_time = pygame.time.get_ticks()
        # Meldung für 3 Sekunden anzeigen
        if current_time - s.temp_message_time < 3000:
            font = pygame.font.SysFont(None, 30)
            text = font.render(s.temp_message, True, (255, 0, 0))  # Rote Schrift
            screen.blit(text, (screen.get_width() // 2 - text.get_width() // 2, 40))
        else:
            # Nach 3 Sekunden löschen
            s.temp_message = ""
