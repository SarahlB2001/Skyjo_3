''' Diese Datei enthält Funktionen zum Zeichnen der Spiel-Oberfläche für Skyjo.
Sie beinhaltet die Darstellung von Spielerfeldern, Namen, Karten, Punkteständen und das Endpodium. '''

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


WINDOW = None
PLAYER_FONT = None
BACKGROUND_IMAGE = None


def initialize():
    global WINDOW, PLAYER_FONT, BACKGROUND_IMAGE
    WINDOW = pygame.display.set_mode((s.HEIGHT, s.WIDTH))
    PLAYER_FONT = pygame.font.SysFont("comicsans", s.PLAYER_SIZE)
    BACKGROUND_IMAGE = pygame.image.load("sky.jpg")
    BACKGROUND_IMAGE = pygame.transform.scale(BACKGROUND_IMAGE, (s.HEIGHT, s.WIDTH))

def first_draw():
    WINDOW.fill(s.WINDOW_COLOR)

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
            WINDOW.blit(name_text, text_rect)

def player_place_position():
    for index, (spieler_id, name) in enumerate(s.player_daten.items()):
        if index < len(pl.player_pos[s.player_count]):
            x_pos, y_pos = pl.player_pos[s.player_count][index]
            name_text = PLAYER_FONT.render(name, True, s.PLAYER_FONT_COLOR)
            WINDOW.blit(name_text, (x_pos, y_pos))


def draw(screen):
    # Spiel-verlassen-Nachricht hat höchste Priorität!
    # if getattr(s, "game_over", False) and s.status_message:
    #     font = pygame.font.SysFont(None, 36)
    #     text = font.render(s.status_message, True, (255, 0, 0))
    #     screen.blit(text, (screen.get_width() // 2 - text.get_width() // 2, 80))
    #     return  # Keine weiteren Hinweise anzeigen

    screen.blit(BACKGROUND_IMAGE, (0, 0))
    cP.card_place_position(screen)
    display_other_messages = True
    # Spielerfelder und Namen zeichnen
    fields = cP.player_fields.get(s.player_count, [])
    namen = [s.player_data.get(i, f"Spieler{i}") for i in range(1, s.player_count + 1)]

    for idx, f in enumerate(fields):
        rect = pl.field_pos[f]
        if idx < len(namen):
            name = namen[idx]
            layout = s.player_cardlayouts.get(idx + 1)
            punkte = 0
            if layout:
                punkte = sum(
    card.value
    for row in layout.cards
    for card in row
    if card.is_face_up and not getattr(card, "removed", False)
)

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
            if hasattr(s, 'current_player') and s.current_player == (idx + 1):
                pygame.draw.circle(screen, (0, 255, 0), (x_start - 20, y_pos + 10), 8)  # Grüner Punkt

            screen.blit(name_text, (x_start, y_pos))
            screen.blit(score_text, (x_start + name_rect.width + 30, y_pos))

            # Score-Historie (lila) anzeigen - NUR wenn Rundenergebnisse vorhanden
            if hasattr(s, "total_scores") and (idx + 1) in s.total_scores:
                # Hole den Score, egal ob Key int oder str ist

                total_score = s.total_scores[idx + 1]
                score_hist_text = PLAYER_FONT.render(f"({total_score})", True, (128, 0, 128))
                screen.blit(score_hist_text, (x_start + name_rect.width + 30 + score_rect.width + 10, y_pos))


    for layout in s.player_cardlayouts.values():
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

       

    # Zeige die Runden-Ende-Nachricht, wenn sie in status_message steht
    if s.status_message and "Runde beendet" in s.status_message:
        font = pygame.font.SysFont(None, 36)
        text = font.render(s.status_message, True, (0, 128, 0))
        screen.blit(text, (screen.get_width() // 2 - text.get_width() // 2, 80))

    # Zeige die Rundenende-Nachricht für 2 Sekunden für ALLE Spieler
    if getattr(s, "round_end_triggered", False) and hasattr(s, "round_end_triggered_time"):
        now = pygame.time.get_ticks()
        if now - s.round_end_triggered_time < 2000:  # 2 Sekunden
            font = pygame.font.SysFont(None, 30)
            text = font.render("Rundenende ausgelöst. Restliche Spieler haben noch einen Zug!", True, (255, 0, 0))
            screen.blit(text, (screen.get_width() // 2 - text.get_width() // 2, 50))
        else:
            s.round_end_triggered = False

    # Zeige "Runde beendet!" für 4 Sekunden nach Rundenende
    if hasattr(s, "round_ended_time"):
        now = pygame.time.get_ticks()
        if now - s.round_ended_time < 4000:
            font = pygame.font.SysFont(None, 36)
            text = font.render("Runde beendet!", True, (0, 128, 0))
            screen.blit(text, (screen.get_width() // 2 - text.get_width() // 2, 80))
            # Andere Status-Nachrichten unterdrücken ohne return zu verwenden
            display_other_messages = False

    else:
        display_other_messages = True

    if display_other_messages:
        # Zeige "Alle Karten wurden aufgedeckt..." für 3 Sekunden nach Punkteberechnung

                 ''' Restliche Statusanzeigen überspringen '''
    # Nur wenn keine spezielle Statusmeldung aktiv ist UND der Spieler NICHT am Zug ist
    if display_other_messages and s.status_message and s.current_player != s.spieler_id:
        if not (hasattr(s, "player_left_message") and s.status_message == s.player_left_message):
            font = pygame.font.SysFont(None, 22)
            text = font.render(s.status_message, True, (0, 0, 0))
            screen.blit(text, (screen.get_width() // 2 - text.get_width() // 2, 10))

    # Rundenanzeige links unten
    if hasattr(s, "current_round") and hasattr(s, "round_count"):
        font = pygame.font.SysFont(None, 28)
        text = font.render(f"Runde {s.current_round}/{s.round_count}", True, (128, 0, 128))
        screen.blit(text, (10, screen.get_height() - 40))

    # --- PODIUM/GEWINNER-ANZEIGE nach der letzten Runde ---
    if hasattr(s, "total_scores") and len(s.total_scores) > 0 and getattr(s, "game_over", False):
        # Podium-Hintergrundbild laden (nur einmal)
        if not hasattr(s, "podium_bg"):
            s.podium_bg = pygame.image.load("podium.jpg")
            s.podium_bg = pygame.transform.scale(s.podium_bg, (600, 350))
        podium_rect = pygame.Rect(screen.get_width()//2 - 300, 120, 600, 350)
        screen.blit(s.podium_bg, podium_rect.topleft)

        # Lila Rahmen
        pygame.draw.rect(screen, (128, 0, 128), podium_rect, 4, border_radius=18)

        # Überschrift
        font = pygame.font.SysFont(None, 54, bold=True)
        headline = font.render("Endstand / Podium ", True, (128, 0, 128))
        screen.blit(headline, (screen.get_width() // 2 - headline.get_width() // 2, 140))

        # Plätze anzeigen
        font = pygame.font.SysFont(None, 38)
        y = 210
        podium = sorted(s.total_scores.items(), key=lambda x: x[1])
        for platz, (pid, punkte) in enumerate(podium, 1):
            name = s.player_data.get(pid, f"Spieler{pid}")
            color = (0, 0, 139)  # Dunkelblau für alle Plätze
            platz_text = f"{platz}."
            text = font.render(f"{platz_text} {name}:  ({punkte} Punkte)", True, color)
            screen.blit(text, (screen.get_width() // 2 - text.get_width() // 2, y))
            y += 45

        # Gewinner-Text
        winner_name = s.player_data.get(podium[0][0], f"Spieler{podium[0][0]}")
        winner_font = pygame.font.SysFont(None, 40, bold=True)
        winner_text = winner_font.render(f"Gewinner: {winner_name}! ", True, (0, 128, 0))
        screen.blit(winner_text, (screen.get_width() // 2 - winner_text.get_width() // 2, y + 20))

        s.podium_shown = True
        # KEIN return hier!

    # Am Ende der Funktion:
    if hasattr(s, "player_left_message") and s.player_left_message:
        font = pygame.font.SysFont(None, 32)
        leave_text = font.render(s.player_left_message, True, (255, 0, 0))  # Rot
        y_pos = screen.get_height() - leave_text.get_height() - 20
        screen.blit(leave_text, (screen.get_width() // 2 - leave_text.get_width() // 2, y_pos))

    # --- Podium/Statusanzeige ---
    # Zeige die Statusnachricht zentriert und prominent, aber NICHT wenn es die player_left_message ist!
    if getattr(s, "game_over", False) and s.status_message and (
        not (hasattr(s, "player_left_message") and s.status_message == s.player_left_message)
    ):
        font = pygame.font.SysFont(None, 36)
        text = font.render(s.status_message, True, (255, 0, 0))
        screen.blit(text, (screen.get_width() // 2 - text.get_width() // 2, 80))
        # return  # ENTFERNEN!
