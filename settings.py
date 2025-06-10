# Datei für die Settings (Konstanten, Globale Variablen etc.)
import server as serv
import pygame
pygame.init()

# Fürs Fenster:

HEIGHT, WIDTH = 800, 800

WINDOW = pygame.display.set_mode((HEIGHT, WIDTH))
# pygame.display.set_caption(" ")
WINDOW_COLOR = "SILVER"

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
PLAYER_FONT_COLOR = WHITE

PL_ANZAHL = serv.anzahl_spieler

# PL_ANZAHL = 2

# vom Server
spieler_daten = serv.spieler_daten

'''
player_daten = {'Spieler 1': 'eins',
                'Spieler 2': 'zwei',
                'Spieler 3': 'drei',
                'Spieler 4': 'vier',
                'Spieler 5': 'funf',
                'Spieler 6': 'sechs'}
'''
