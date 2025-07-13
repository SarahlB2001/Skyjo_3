'''Eine zentrale Datei für globale Einstellungen und Variablen.
Sie enthält Konstanten wie Fenstergrößen, Farben und Spielkonfiguration,
sowie gemeinsam genutzte Spielzustandsvariablen, die von verschiedenen Modulen verwendet werden.'''

import threading

# Fürs Fenster:
HEIGHT, WIDTH = 1200, 600


WINDOW_COLOR = "SILVER"


FPS = 60


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
PLAYER_FONT_COLOR = BLACK

# Variablen für den Server
player_data = {}
player_daten = {}


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
game_mode = None
waiting_for_name = False
waiting_for_players = False
waiting_for_rounds = False
waiting_for_start = False
status_message = ""
running = True
sock = None
spieler_id = None

ROWS = 3
COLS = 4

CARD_WIDTH = 40
CARD_HEIGHT = 70
gap_width = 45
gap_height = 3

cards_flipped_this_turn = 0
current_player = None
cards_flipped = {}

CARD_IMAGES= {
    i: f"img/card_{i}.png" for i in range ( -2, 13)
}

# Zustandsvariablen für Spielzüge
tausche_mit_ablagestapel = False
warte_auf_entscheidung = False
gezogene_karte = None
muss_karte_aufdecken = False
setup_phase = True  # Phase in der 2 Karten aufgedeckt werden
zug_begonnen = False

round_end_triggered = False
round_end_trigger_player = None

current_round = 1
round_count = 1  # Wird vom Host gesetzt
score_history = {}  # Für die Anzeige der Rundenpunkte
total_scores = {}

# Kartendeck
draw_pile = []  # Nachziehstapel
discard_pile = []  # Ablagestapel