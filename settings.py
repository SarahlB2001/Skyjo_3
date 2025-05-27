# Datei für die Settings (Konstanten, Globale Variablen etc.)
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
PLAYER_X_POSITION = 1
PLAYER_Y_POSITION = 1

POSITION_X_LEFT = 1
POSITION_X_MID = WIDTH//2
POSITION_X_RIGHT = WIDTH - 100

POSITION_Y_TOP = 1
POSITION_Y_MID = HEIGHT//2
POSITION_Y_BOT = HEIGHT - 100

PLAYER_SIZE = 20
PLAYER_FONT = pygame.font.SysFont("comicsans", PLAYER_SIZE)
PLAYER_FONT_COLOR = BLACK