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
    display_other_messages = True  ######
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
          #  print(f"[DEBUG] Prüfe current_player: {getattr(s, 'current_player', 'NICHT GESETZT')}")
            if hasattr(s, 'current_player') and s.current_player == (idx + 1):
              #  print(f"[DEBUG] Zeichne grünen Punkt für Spieler {s.current_player} an Position ({x_start - 20}, {y_pos + 10})")
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

    # Statusnachricht nur für nicht-aktive Spieler anzeigen
    '''if s.status_message and s.current_player != s.spieler_id:
        font = pygame.font.SysFont(None, 22)  # Kleinere Schriftgröße (war 30)
        text = font.render(s.status_message, True, (0, 0, 0))
        screen.blit(text, (screen.get_width() // 2 - text.get_width() // 2, 10))'''

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
        '''if hasattr(s, "points_calculated_time"):
            now = pygame.time.get_ticks()
            if now - s.points_calculated_time < 6000:
                font = pygame.font.SysFont(None, 30)
                text = font.render("Alle Karten wurden aufgedeckt. Punkte wurden berechnet!", True, (0, 0, 255))
                screen.blit(text, (screen.get_width() // 2 - text.get_width() // 2, 120))
                # Endgültige Punktzahlen anzeigen UNTER der Meldung
                if hasattr(cP, "player_cardlayouts"):
                    # Lokale Punkte berechnen
                    punkte_dict = {}
                    for pid, layout in cP.player_cardlayouts.items():
                        punkte = sum(
                            card.value
                            for row in layout.cards
                            for card in row
                            if card.is_face_up and not getattr(card, "removed", False)
                        )
                        punkte_dict[pid] = punkte

                    # Auslöser-ID holen und ggf. verdoppeln
                    ausloeser_id = getattr(s, "round_end_trigger_player", None)
                    if ausloeser_id is not None and ausloeser_id in punkte_dict:
                        ausloeser_score = punkte_dict[ausloeser_id]
                        min_score = min(punkte_dict.values())
                        if ausloeser_score > min_score:
                            punkte_dict[ausloeser_id] = ausloeser_score * 2

                  
                    y = 160
                    font = pygame.font.SysFont(None, 28)
                    for pid, punkte in punkte_dict.items():
                        name = s.player_data.get(pid, f"Spieler{pid}")
                        text = font.render(f"{name}: {punkte} Punkte", True, (0, 0, 0))
                        screen.blit(text, (screen.get_width() // 2 - text.get_width() // 2, y))
                        y += 30
                        print(f"{name}: {punkte} Punkte") '''
                #display_other_messages = False ''' # Restliche Statusanzeigen überspringen 

    # Nur wenn keine spezielle Statusmeldung aktiv ist, zeige normale Statusmeldungen
    # Nur wenn keine spezielle Statusmeldung aktiv ist UND der Spieler NICHT am Zug ist
    if display_other_messages and s.status_message and s.current_player != s.spieler_id:
        font = pygame.font.SysFont(None, 22)
        text = font.render(s.status_message, True, (0, 0, 0))
        screen.blit(text, (screen.get_width() // 2 - text.get_width() // 2, 10))

     
    # Rundenanzeige links unten
    if hasattr(s, "current_round") and hasattr(s, "round_count"):
        font = pygame.font.SysFont(None, 28)
        text = font.render(f"Runde {s.current_round}/{s.round_count}", True, (128, 0, 128))
        screen.blit(text, (10, screen.get_height() - 40))
    '''
    # Zeige für die Endpunktzahl die offiziellen Werte vom Server
    if hasattr(s, "final_round_scores"):
        y = 160
        font = pygame.font.SysFont(None, 28)
        for pid, punkte in s.final_round_scores.items():
            name = s.player_data.get(pid, f"Spieler{pid}")
            text = font.render(f"{name}: {punkte} Punkte", True, (0, 0, 0))
            screen.blit(text, (screen.get_width() // 2 - text.get_width() // 2, y))
            y += 30 '''

    # --- PODIUM/GEWINNER-ANZEIGE nach der letzten Runde ---
    # Zeige das Podium, wenn das Spiel vorbei ist
    #if hasattr(s, "total_scores") and hasattr(s, "game_ended_time") and len(s.total_scores) > 0:
    if hasattr(s, "total_scores") and len(s.total_scores) > 0 and getattr(s, "game_over", False):
        screen.fill((255, 255, 255))
        
            # Prüfe, ob das Spiel wirklich vorbei ist (z.B. nach game_ended)
        
        # Sortiere Spieler nach Punktzahl (aufsteigend = Gewinner zuerst)
        podium = sorted(s.total_scores.items(), key=lambda x: x[1])
        font = pygame.font.SysFont(None, 48)
        headline = font.render("Endstand / Podium", True, (0, 0, 0))
        screen.blit(headline, (screen.get_width() // 2 - headline.get_width() // 2, 180))

                # Zeige die Plätze
        font = pygame.font.SysFont(None, 36)
        y = 250
        for platz, (pid, punkte) in enumerate(podium, 1):
            name = s.player_data.get(pid, f"Spieler{pid}")
            color = (218, 165, 32) if platz == 1 else (128, 128, 128) if platz == 2 else (205, 127, 50) if platz == 3 else (0, 0, 0)
            text = font.render(f"{platz}. {name}  ({punkte} Punkte)", True, color)
            screen.blit(text, (screen.get_width() // 2 - text.get_width() // 2, y))
            y += 45

        # Optional: Gewinner-Text
        winner_name = s.player_data.get(podium[0][0], f"Spieler{podium[0][0]}")
        winner_text = font.render(f"Gewinner: {winner_name}!", True, (0, 128, 0))
        screen.blit(winner_text, (screen.get_width() // 2 - winner_text.get_width() // 2, y + 20))

        # Merke, dass das Podium gezeigt wurde (damit es nicht mehrfach erscheint)
        s.podium_shown = True

        return  # Alles andere ausblenden, solange das Podium angezeigt wird

    # --- PODIUM/GEWINNER-ANZEIGE nach der letzten Runde ---
    if hasattr(s, "total_scores") and len(s.total_scores) > 0 and getattr(s, "game_over", False):
        # Hintergrundbox (halbtransparent)
        podium_rect = pygame.Rect(screen.get_width()//2 - 300, 120, 600, 350)
        podium_surface = pygame.Surface((600, 350), pygame.SRCALPHA)
        podium_surface.fill((255, 255, 255, 230))  # Weiß, leicht transparent
        screen.blit(podium_surface, podium_rect.topleft)
        pygame.draw.rect(screen, (128, 0, 128), podium_rect, 4, border_radius=18)  # Lila Rahmen

        # Überschrift
        font = pygame.font.SysFont(None, 54, bold=True)
        headline = font.render("🏆 Endstand / Podium 🏆", True, (128, 0, 128))
        screen.blit(headline, (screen.get_width() // 2 - headline.get_width() // 2, 140))

        # Plätze anzeigen
        font = pygame.font.SysFont(None, 38)
        y = 210
        podium = sorted(s.total_scores.items(), key=lambda x: x[1])
        for platz, (pid, punkte) in enumerate(podium, 1):
            name = s.player_data.get(pid, f"Spieler{pid}")
            if platz == 1:
                color = (218, 165, 32)  # Gold
                platz_icon = "🥇"
            elif platz == 2:
                color = (192, 192, 192)  # Silber
                platz_icon = "🥈"
            elif platz == 3:
                color = (205, 127, 50)   # Bronze
                platz_icon = "🥉"
            else:
                color = (80, 80, 80)
                platz_icon = f"{platz}."
            text = font.render(f"{platz_icon} {name}  ({punkte} Punkte)", True, color)
            screen.blit(text, (screen.get_width() // 2 - text.get_width() // 2, y))
            y += 45

        # Gewinner-Text
        winner_name = s.player_data.get(podium[0][0], f"Spieler{podium[0][0]}")
        winner_font = pygame.font.SysFont(None, 40, bold=True)
        winner_text = winner_font.render(f"🎉 Gewinner: {winner_name}! 🎉", True, (0, 128, 0))
        screen.blit(winner_text, (screen.get_width() // 2 - winner_text.get_width() // 2, y + 20))

        s.podium_shown = True
        return


