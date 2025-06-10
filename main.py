''' This program simulates the card game Skyjo  '''
# author: Sarah B., Antonia  H., Diedan.S, Dieja S., Marit S.

import pygame
import sys
import functions.client as c
import server as serv
import layout as l
import settings as s


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

    # Hintergrundbild des Menüs
    background = pygame.image.load("Skyjo_Menü.png")

    # Buttons für Spieleranzahl (auf Höhe des Host-Buttons)
    player_count_buttons = [pygame.Rect(0, 420, 50, 50) for i in range(4)]
    # Buttons für Rundenzahl (auf Höhe des Host-Buttons)
    round_count_buttons = [pygame.Rect(0, 420, 50, 50) for i in range(5)]


    while s.running:

        screen.blit(background, (0, 0))
        layout = l.CardLayout(start_x=100, start_y=200)
        layout.draw(screen)
        # Zeige die IP-Adresse an, wenn Host ausgewählt wurde
        if s.game_mode == "host":
            ip_text = small_font.render(f"Deine IP: {c.get_local_ip()}", True, (0, 0, 0))
            screen.blit(ip_text, (10, 10))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                s.running = False







            if event.type == pygame.MOUSEBUTTONDOWN:
                if s.game_mode is None:
                    # Spielmodus wählen: Host oder Join
                    if host_button.collidepoint(event.pos):
                        s.game_mode = "host"
                        s.waiting_for_players = True
                        print("[DEBUG] Game mode set to 'host'")
                    elif join_button.collidepoint(event.pos):
                        s.game_mode = "join"
                        s.entering_ip = True  # IP wird jetzt eingegeben
                        print("[DEBUG] Game mode set to 'join'")

                elif s.waiting_for_players:
                    # Spieleranzahl wählen (Host)
                    for i, button in enumerate(player_count_buttons):
                        if button.collidepoint(event.pos):
                            s.player_count = i + 1
                            print(f"[DEBUG] Player count set to {s.player_count}")
                            s.sock, s.spieler_id = c.connect_to_server()
                            serv.send_data(s.sock, {"anzahl_spieler": s.player_count})
                            s.waiting_for_players = False
                            s.waiting_for_rounds = True
                            break

                elif s.waiting_for_rounds:
                    # Rundenzahl wählen (Host)
                    for i, button in enumerate(round_count_buttons):
                        if button.collidepoint(event.pos):
                            s.round_count = i + 1
                            print(f"[DEBUG] Round count set to {s.round_count}")
                            serv.send_data(s.sock, {"anzahl_runden": s.round_count})
                            s.waiting_for_rounds = False
                            s.waiting_for_name = True
                            break

                elif s.entering_ip:
                    # IP-Eingabefeld aktivieren/deaktivieren
                    if ip_input_box.collidepoint(event.pos):
                        s.active = True
                        print("[DEBUG] IP input box activated")
                    else:
                        s.active = False
                        print("[DEBUG] IP input box deactivated")

                elif s.waiting_for_name:
                    # Namenseingabefeld aktivieren/deaktivieren
                    if input_box.collidepoint(event.pos):
                        s.active = True
                        print("[DEBUG] Input box activated")
                    else:
                        s.active = False
                        print("[DEBUG] Input box deactivated")

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
                            print(f"[ERROR] Verbindung zum Server fehlgeschlagen: {e}")
                    elif event.key == pygame.K_BACKSPACE:
                        s.ip_input = s.ip_input[:-1]
                    else:
                        if len(ip_input) < 25:
                            ip_input += event.unicode

                elif s.waiting_for_name and s.active:
                    if event.key == pygame.K_RETURN:
                        # Name absenden
                        if s.sock:
                            serv.send_data(s.sock, {"name": s.text_input.strip()})
                            print(f"[DEBUG] Name sent: {s.text_input.strip()}")
                        s.active = False
                        s.text_input = ""
                        s.waiting_for_name = False  # Namen eingegeben, keine Eingabe mehr notwendig

                        # Status sofort setzen
                        s.status_message = "Warten auf andere Spieler..."
                        s.waiting_for_start = True

                        # Nachricht vom Server abwarten
                        msg = serv.recv_data(s.sock)
                        if msg and "message" in msg:
                            if "starten" in msg["message"].lower():
                                s.status_message = "Spiel startet"
                            else:
                                s.status_message = msg["message"]

                    elif event.key == pygame.K_BACKSPACE:
                        s.text_input = s.text_input[:-1]
                    else:
                        if len(s.text_input) < 12:  # Maximal 12 Zeichen erlauben
                            s.text_input += event.unicode

        # Menü: Spielmodi Auswahl
        if s.game_mode is None:
            pygame.draw.rect(screen, (0, 200, 0), host_button)
            pygame.draw.rect(screen, (200, 0, 0), join_button)

            host_text = font.render("Spiel Hosten", True, (255, 255, 255))
            join_text = font.render("Spiel Beitreten", True, (255, 255, 255))

            screen.blit(host_text, (host_button.x + 20, host_button.y + 10))
            screen.blit(join_text, (join_button.x + 20, join_button.y + 10))

        # Spieleranzahl auswählen (Host)
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
                player_text = small_font.render(f"{i+1}", True, (255, 255, 255))
                screen.blit(player_text, (button.x + button.width // 2 - player_text.get_width() // 2, button.y + 10))

        # Rundenzahl auswählen (Host)
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
                round_text = small_font.render(f"{i+1}", True, (255, 255, 255))
                screen.blit(round_text, (button.x + button.width // 2 - round_text.get_width() // 2, button.y + 10))

        # Namenseingabe
        if s.waiting_for_name:
            prompt_text = small_font.render(f"Bitte Namen eingeben:", True, (0, 0, 0))
            screen.blit(prompt_text, (500, 420))
            txt_surface = font.render(s.text_input, True, (0, 0, 0))
            screen.blit(txt_surface, (input_box.x + 5, input_box.y + 5))
            pygame.draw.rect(screen, (0, 0, 0), input_box, 2)

        # IP Eingabe beim Join
        if s.game_mode == "join" and s.entering_ip:
            prompt = small_font.render("Host-IP eingeben:", True, (0, 0, 0))
            screen.blit(prompt, (500, 420))
            ip_surface = font.render(s.ip_input, True, (0, 0, 0))
            screen.blit(ip_surface, (ip_input_box.x + 5, ip_input_box.y + 5))
            pygame.draw.rect(screen, (0, 0, 0), ip_input_box, 2)

        # Statusmeldung anzeigen
        if s.status_message:
            status_surface = font.render(s.status_message, True, (0, 0, 0))
            screen.blit(status_surface, (screen.get_width() // 2 - status_surface.get_width() // 2, 100))

        # Auf Startnachricht vom Server warten
        if s.waiting_for_start and s.sock:
            s.sock.setblocking(False)
            try:
                msg = serv.recv_data(s.sock)
                if msg and "message" in msg:
                    s.status_message = msg["message"]
                    if "startet" in s.status_message.lower():
                        s.waiting_for_start = False
            except BlockingIOError:
                # Kein neuer Input, einfach ignorieren
                pass
            except Exception as e:
                print(f"[FEHLER] Empfangsfehler: {e}")
                s.status_message = "Verbindungsfehler!"
                s.waiting_for_start = False
            finally:
                s.sock.setblocking(True)

        pygame.display.flip()
        clock.tick(30)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
