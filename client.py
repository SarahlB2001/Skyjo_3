import socket
import pickle
import pygame
import sys
import threading

# Verbindung zum Server herstellen
def connect_to_server(SERVER_IP="127.0.0.1"):
    PORT = 65432
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((SERVER_IP, PORT))

    # Empfang erste Daten (spieler_id)
    data = recv_data(sock)
    if data and "error" in data:
        print("[SERVER]:", data["error"])
        sock.close()
        sys.exit()

    spieler_id = data["spieler_id"]
    print(f"[INFO] Verbunden als Spieler {spieler_id}")
    return sock, spieler_id

def recv_data(conn):
    """Hilfsfunktion für sicheres Empfangen von Daten"""
    try:
        data = conn.recv(4096)
        if data:
            return pickle.loads(data)
    except (EOFError, pickle.UnpicklingError, ConnectionResetError):
        return None
    return None

def send_data(conn, data):
    """Hilfsfunktion für das Senden von Daten"""
    try:
        conn.sendall(pickle.dumps(data))
    except:
        pass

def get_local_ip():
    """Ermittelt die lokale IP-Adresse des Hosts."""
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        # Verbindung zu einer beliebigen Adresse (wird nicht gesendet)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
    except Exception:
        ip = "127.0.0.1"
    finally:
        s.close()
    return ip

# Pygame GUI
def main():
    pygame.init()
    screen = pygame.display.set_mode((600, 400))
    pygame.display.set_caption("Mehrspieler Spiel")

    font = pygame.font.SysFont(None, 36)
    small_font = pygame.font.SysFont(None, 28)

    clock = pygame.time.Clock()

    host_button = pygame.Rect(200, 100, 200, 50)
    join_button = pygame.Rect(200, 200, 200, 50)

    input_box = pygame.Rect(150, 300, 300, 50)
    text_input = ""
    active = False

    ip_input_box = pygame.Rect(150, 270, 300, 50)
    ip_input = ""
    entering_ip = False

    # Auswahl Buttons für die Anzahl der Spieler (nur für den Host sichtbar)
    player_count_buttons = [pygame.Rect(50 + 60 * i, 350, 50, 50) for i in range(8)]
    player_count = None  # Spieleranzahl, wird nach der Namensangabe festgelegt

    # Auswahl Buttons für die Anzahl der Runden (nur für den Host sichtbar)
    round_count_buttons = [pygame.Rect(50 + 60 * i, 470, 50, 50) for i in range(5)]
    round_count = None  # Rundenanzahl, wird nach der Spieleranzahl festgelegt

    game_mode = None  # None -> keine Auswahl, 'host' -> hosten, 'join' -> beitreten
    waiting_for_name = False  # Flag für Namen eingeben
    waiting_for_players = False  # Flag für die Auswahl der Spieleranzahl (nur für den Host)
    waiting_for_rounds = False  # Flag für die Auswahl der Rundenanzahl (nur für den Host)

    running = True
    sock = None
    spieler_id = None
    while running:
        screen.fill((255, 255, 255))

        # Zeige die IP-Adresse an, wenn Host ausgewählt wurde
        if game_mode == "host":
            ip_text = small_font.render(f"Deine IP: {get_local_ip()}", True, (0, 0, 0))
            screen.blit(ip_text, (10, 10))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                if game_mode is None:
                    # Verarbeite Spielmodi-Buttons
                    if host_button.collidepoint(event.pos):
                        game_mode = "host"
                        waiting_for_players = True
                        print("[DEBUG] Game mode set to 'host'")
                    elif join_button.collidepoint(event.pos):
                        game_mode = "join"
                        entering_ip = True  # Jetzt IP eingeben
                        print("[DEBUG] Game mode set to 'join'")
                elif waiting_for_players:
                    # Spieleranzahl wählen
                    for i, button in enumerate(player_count_buttons):
                        if button.collidepoint(event.pos):
                            player_count = i + 1
                            print(f"[DEBUG] Player count set to {player_count}")
                            # Verbindung erst jetzt aufbauen!
                            sock, spieler_id = connect_to_server()
                            send_data(sock, {"anzahl_spieler": player_count})
                            waiting_for_players = False
                            waiting_for_rounds = True  # Jetzt Rundenanzahl wählen
                            break
                elif waiting_for_rounds:
                    # Rundenzahl wählen
                    for i, button in enumerate(round_count_buttons):
                        if button.collidepoint(event.pos):
                            round_count = i + 1
                            print(f"[DEBUG] Round count set to {round_count}")
                            send_data(sock, {"anzahl_runden": round_count})
                            waiting_for_rounds = False
                            waiting_for_name = True  # Jetzt Name eingeben
                            break
                elif entering_ip:
                    if ip_input_box.collidepoint(event.pos):
                        active = True
                        print("[DEBUG] IP input box activated")
                    else:
                        active = False
                        print("[DEBUG] IP input box deactivated")
                elif waiting_for_name:
                    # Überprüfe, ob das Eingabefeld angeklickt wurde
                    if input_box.collidepoint(event.pos):
                        active = True
                        print("[DEBUG] Input box activated")
                    else:
                        active = False
                        print("[DEBUG] Input box deactivated")

            if event.type == pygame.KEYDOWN:
                if entering_ip and active:
                    if event.key == pygame.K_RETURN:
                        SERVER_IP = ip_input  # IP übernehmen
                        sock, spieler_id = connect_to_server(SERVER_IP)
                        entering_ip = False
                        waiting_for_name = True
                        ip_input = ""
                    elif event.key == pygame.K_BACKSPACE:
                        ip_input = ip_input[:-1]
                    else:
                        ip_input += event.unicode
                elif waiting_for_name and active:
                    if event.key == pygame.K_RETURN:
                        # Nach Eingabe des Namens, sende Name an Server
                        if game_mode == "host":
                            send_data(sock, {"name": text_input})
                        elif game_mode == "join":
                            send_data(sock, {"name": text_input})

                        print(f"[DEBUG] Name sent: {text_input}")
                        active = False
                        text_input = ""
                        waiting_for_name = False  # Namen eingegeben, keine Eingabe mehr notwendig

                        # Nachricht vom Server warten:
                        msg = recv_data(sock)
                        if msg and "message" in msg:
                            print(msg["message"])

                    elif event.key == pygame.K_BACKSPACE:
                        text_input = text_input[:-1]
                    else:
                        text_input += event.unicode

        # GUI für die Auswahl der Spielmodi
        pygame.draw.rect(screen, (0, 200, 0), host_button)
        pygame.draw.rect(screen, (200, 0, 0), join_button)

        host_text = font.render("Spiel Hosten", True, (255, 255, 255))
        join_text = font.render("Spiel Beitreten", True, (255, 255, 255))

        screen.blit(host_text, (host_button.x + 20, host_button.y + 10))
        screen.blit(join_text, (join_button.x + 20, join_button.y + 10))

        # Spieleranzahl-Buttons anzeigen, wenn der Host die Spieleranzahl wählen soll
        if waiting_for_players:
            headline = font.render("Spieleranzahl wählen", True, (0, 0, 0))
            screen.blit(headline, (50, 310))
            for i, button in enumerate(player_count_buttons):
                pygame.draw.rect(screen, (0, 0, 255), button)
                player_text = small_font.render(f"{i+1}", True, (255, 255, 255))
                screen.blit(player_text, (button.x + 15, button.y + 10))

        # Rundenzahl-Buttons anzeigen, wenn der Host die Rundenzahl wählen soll
        if waiting_for_rounds:
            headline = font.render("Rundenanzahl wählen", True, (0, 0, 0))
            screen.blit(headline, (50, 270))  # <-- y-Wert von 380 auf 250 geändert
            for i, button in enumerate(round_count_buttons):
                button.y = 290  # <-- y-Wert der Buttons z.B. auf 290 setzen
                pygame.draw.rect(screen, (255, 140, 0), button)
                round_text = small_font.render(f"{i+1}", True, (255, 255, 255))
                screen.blit(round_text, (button.x + 15, button.y + 10))

        # Eingabefeld für den Namen anzeigen, wenn der Benutzer seinen Namen eingeben soll
        if waiting_for_name:
            prompt_text = small_font.render(f"Bitte Namen eingeben:", True, (0, 0, 0))
            screen.blit(prompt_text, (150, 270))
            txt_surface = font.render(text_input, True, (0, 0, 0))
            screen.blit(txt_surface, (input_box.x + 5, input_box.y + 5))
            pygame.draw.rect(screen, (0, 0, 0), input_box, 2)

        if game_mode == "join" and entering_ip:
            prompt = small_font.render("Host-IP eingeben:", True, (0, 0, 0))
            screen.blit(prompt, (150, 330))
            ip_surface = font.render(ip_input, True, (0, 0, 0))
            screen.blit(ip_surface, (ip_input_box.x + 5, ip_input_box.y + 5))
            pygame.draw.rect(screen, (0, 0, 0), ip_input_box, 2)

        pygame.display.flip()
        clock.tick(30)


    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
