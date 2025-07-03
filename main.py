''' This program simulates the card game Skyjo  '''
# author: Sarah B., Antonia  H., Diedan.S, Dieja S., Marit S.

import pygame
import sys
import functions.client as c
import server as serv
import layout as l
import settings as s
import surface as su
import time
from dictionaries import cardSetPosition as cP


def main():
    pygame.init()
    screen = pygame.display.set_mode((s.HEIGHT, s.WIDTH))
    pygame.display.set_caption("Mehrspieler Spiel")

    font = pygame.font.SysFont(None, 36)
    small_font = pygame.font.SysFont(None, 28)

    clock = pygame.time.Clock()

    host_button = pygame.Rect(500, 420, 200, 50)
    join_button = pygame.Rect(500, 490, 200, 50)

    input_box = pygame.Rect(450, 470, 300, 50)
    ip_input_box = pygame.Rect(450, 470, 300, 50)

    background = pygame.image.load("Skyjo_Menü.png")

    player_count_buttons = [pygame.Rect(0, 420, 50, 50) for _ in range(4)]
    round_count_buttons = [pygame.Rect(0, 420, 50, 50) for _ in range(5)]

    while s.running:
        if (
            s.game_mode is None
            or s.waiting_for_players
            or s.waiting_for_rounds
            or s.waiting_for_name
            or s.entering_ip
            or s.waiting_for_start
        ):
            screen.blit(background, (0, 0))

            if s.game_mode == "host":
                ip_text = small_font.render(f"Deine IP: {c.get_local_ip()}", True, (0, 0, 0))
                screen.blit(ip_text, (10, 10))

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    s.running = False

                if event.type == pygame.MOUSEBUTTONDOWN:
                    if s.game_mode is None:
                        if host_button.collidepoint(event.pos):
                            s.game_mode = "host"
                            s.waiting_for_players = True
                        elif join_button.collidepoint(event.pos):
                            s.game_mode = "join"
                            s.entering_ip = True

                    elif s.waiting_for_players:
                        for i, button in enumerate(player_count_buttons):
                            if button.collidepoint(event.pos):
                                s.player_count = i + 1
                                s.PL_ANZAHL = s.player_count  # <--- HIER hinzufügen!
                                s.sock, s.spieler_id = c.connect_to_server()
                                serv.send_data(s.sock, {"anzahl_spieler": s.player_count})
                                s.waiting_for_players = False
                                s.waiting_for_rounds = True
                                break

                    elif s.waiting_for_rounds:
                        for i, button in enumerate(round_count_buttons):
                            if button.collidepoint(event.pos):
                                s.round_count = i + 1
                                serv.send_data(s.sock, {"anzahl_runden": s.round_count})
                                s.waiting_for_rounds = False
                                s.waiting_for_name = True
                                break

                    elif s.entering_ip:
                        if ip_input_box.collidepoint(event.pos):
                            s.active = True
                        else:
                            s.active = False

                    elif s.waiting_for_name:
                        if input_box.collidepoint(event.pos):
                            s.active = True
                        else:
                            s.active = False

                if event.type == pygame.KEYDOWN:
                    if s.entering_ip and s.active:
                        if event.key == pygame.K_RETURN:
                            SERVER_IP = s.ip_input.strip()
                            try:
                                s.sock, s.spieler_id = c.connect_to_server(SERVER_IP)
                                s.entering_ip = False
                                s.waiting_for_name = True
                                s.ip_input = ""
                            except Exception as e:
                                s.status_message = f"Verbindung fehlgeschlagen: {e}"
                        elif event.key == pygame.K_BACKSPACE:
                            s.ip_input = s.ip_input[:-1]
                        else:
                            s.ip_input += event.unicode

                    elif s.waiting_for_name and s.active:
                        if event.key == pygame.K_RETURN:
                            if s.sock:
                                serv.send_data(s.sock, {"name": s.text_input.strip()})
                            s.active = False
                            s.text_input = ""
                            s.waiting_for_name = False
                            s.status_message = "Warten auf andere Spieler..."
                            s.waiting_for_start = True
                        elif event.key == pygame.K_BACKSPACE:
                            s.text_input = s.text_input[:-1]
                        else:
                            if len(s.text_input) < 12:
                                s.text_input += event.unicode

            # Menü-UI
            if s.game_mode is None:
                pygame.draw.rect(screen, (0, 200, 0), host_button)
                pygame.draw.rect(screen, (200, 0, 0), join_button)
                screen.blit(font.render("Spiel Hosten", True, (255, 255, 255)), (host_button.x + 20, host_button.y + 10))
                screen.blit(font.render("Spiel Beitreten", True, (255, 255, 255)), (join_button.x + 20, join_button.y + 10))

            if s.waiting_for_players:
                headline = font.render("Spieleranzahl wählen", True, (0, 0, 0))
                screen.blit(headline, (screen.get_width() // 2 - headline.get_width() // 2, 420))
                total_width = len(player_count_buttons) * 60 - 10
                start_x = screen.get_width() // 2 - total_width // 2
                y = 480
                for i, button in enumerate(player_count_buttons):
                    button.x = start_x + i * 60
                    button.y = y
                    pygame.draw.rect(screen, (0, 0, 255), button)
                    text = small_font.render(f"{i+1}", True, (255, 255, 255))
                    screen.blit(text, (button.x + button.width // 2 - text.get_width() // 2, button.y + 10))

            if s.waiting_for_rounds:
                headline = font.render("Rundenanzahl wählen", True, (0, 0, 0))
                screen.blit(headline, (screen.get_width() // 2 - headline.get_width() // 2, 420))
                total_width = len(round_count_buttons) * 60 - 10
                start_x = screen.get_width() // 2 - total_width // 2
                y = 480
                for i, button in enumerate(round_count_buttons):
                    button.x = start_x + i * 60
                    button.y = y
                    pygame.draw.rect(screen, (255, 140, 0), button)
                    text = small_font.render(f"{i+1}", True, (255, 255, 255))
                    screen.blit(text, (button.x + button.width // 2 - text.get_width() // 2, button.y + 10))

            if s.waiting_for_name:
                screen.blit(small_font.render("Bitte Namen eingeben:", True, (0, 0, 0)), (500, 420))
                txt_surface = font.render(s.text_input, True, (0, 0, 0))
                screen.blit(txt_surface, (input_box.x + 5, input_box.y + 5))
                pygame.draw.rect(screen, (0, 0, 0), input_box, 2)

            if s.game_mode == "join" and s.entering_ip:
                screen.blit(small_font.render("Host-IP eingeben:", True, (0, 0, 0)), (500, 420))
                ip_surface = font.render(s.ip_input, True, (0, 0, 0))
                screen.blit(ip_surface, (ip_input_box.x + 5, ip_input_box.y + 5))
                pygame.draw.rect(screen, (0, 0, 0), ip_input_box, 2)

            if s.status_message:
                status_surface = font.render(s.status_message, True, (0, 0, 0))
                screen.blit(status_surface, (screen.get_width() // 2 - status_surface.get_width() // 2, 100))

            if s.waiting_for_start and s.sock:
                s.sock.setblocking(False)
                try:
                    msg = serv.recv_data(s.sock)
                    if msg and "message" in msg:
                        s.status_message = msg["message"]
                        # HIER Spielernamen speichern:
                        if "spielernamen" in msg:
                            # Keys in int umwandeln!
                            s.player_data = {int(k): v for k, v in msg["spielernamen"].items()}
                        if "anzahl_spieler" in msg:
                            s.player_count = int(msg["anzahl_spieler"])
                        if "startet" in s.status_message.lower() or "starten" in s.status_message.lower():
                            cP.card_set_positions(screen)
                            s.waiting_for_start = False
                            s.game_started = True
                except BlockingIOError:
                    pass
                except Exception as e:
                    print(f"[FEHLER] Empfangsfehler: {e}")
                    s.status_message = "Verbindungsfehler!"
                    s.waiting_for_start = False
                finally:
                    s.sock.setblocking(True)

        else:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    s.running = False

            su.draw(screen)

        pygame.display.flip()
        clock.tick(30)

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
