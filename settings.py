# Datei für die Settings (Konstanten, Globale Variablen etc.)
import pygame
import server as serv
import threading

# Fürs Fenster:
HEIGHT, WIDTH = 1200, 600

# pygame.display.set_caption(" ")
WINDOW_COLOR = "SILVER"

# FPS
FPS = 60

# Uhr
#clock = pygame.time.Clock()

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
PL_NAME_POS = 1.3 * PLAYER_SIZE
#PLAYER_FONT = pygame.font.SysFont("comicsans", PLAYER_SIZE)
PLAYER_FONT_COLOR = BLACK

PL_ANZAHL = 6
# PL_ANZAHL = serv.anzahl_spieler

# Variablen für den Server
player_data = {}

player_daten = {'Spieler 1': 'eins',
                'Spieler 2': 'zwei',
                'Spieler 3': 'drei',
                'Spieler 4': 'vier',
                'Spieler 5': 'funf',
                'Spieler 6': 'sechs'}

connection = []
player_count = None
player_count_event = threading.Event()
lock = threading.Lock()

# Variablen für den Main
text_input = ""
active = False
ip_input = ""
entering_ip = False
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

ROWS = 3
COLS = 4

CARD_WIDTH = 50
CARD_HEIGHT = 90
gap_width = 10
gap_height = 10



CARD_IMAGES= {
    i: f"img/card_{i}.png" for i in range ( -2, 13)
}
