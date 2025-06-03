# Datei für die Settings (Konstanten, Globale Variablen etc.)
import pygame
import threading

pygame.init()

# Fürs Fenster:
HEIGHT, WIDTH = 600, 400
screen = pygame.display.set_mode((HEIGHT, WIDTH))


# FPS
FPS = 60

# Uhr
clock = pygame.time.Clock()

# Farben
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
ORANGE = (255, 165, 0)

# Spieler
PLAYER_X_POSITION = 10
PLAYER_Y_POSITION = 10

PLAYER_SIZE = 20
PLAYER_FONT = pygame.font.SysFont("comicsans", PLAYER_SIZE)
PLAYER_FONT_COLOR = BLACK

PL_ANZAHL = 6

# Variablen für den Server
spieler_daten = {}
verbindungen = []
anzahl_spieler = None
anzahl_spieler_event = threading.Event()
lock = threading.Lock()

# Variablen für den Main
font = pygame.font.SysFont(None, 36)
small_font = pygame.font.SysFont(None, 28)
host_button = pygame.Rect(200, 250, 200, 50)
join_button = pygame.Rect(200, 320, 200, 50)
input_box = pygame.Rect(150, 300, 300, 50)
text_input = ""
active = False
ip_input_box = pygame.Rect(150, 270, 300, 50)
ip_input = ""
entering_ip = False

# Auswahl Buttons für die Anzahl der Spieler (nur für den Host sichtbar)
player_count_buttons = [pygame.Rect(50 + 60 * i, 350, 50, 50) for i in range(4)]
player_count = None  # Spieleranzahl, wird nach der Namensangabe festgelegt

# Auswahl Buttons für die Anzahl der Runden (nur für den Host sichtbar)
round_count_buttons = [pygame.Rect(50 + 60 * i, 470, 50, 50) for i in range(5)]
round_count = None  # Rundenanzahl, wird nach der Spieleranzahl festgelegt

game_mode = None  # None -> keine Auswahl, 'host' -> hosten, 'join' -> beitreten
waiting_for_name = False  # Flag für Namen eingeben
waiting_for_players = False  # Flag für die Auswahl der Spieleranzahl (nur für den Host)
waiting_for_rounds = False  # Flag für die Auswahl der Rundenanzahl (nur für den Host)
waiting_for_start = False  # Flag, dass wir auf Startnachricht warten
status_message = ""
running = True
sock = None
spieler_id = None