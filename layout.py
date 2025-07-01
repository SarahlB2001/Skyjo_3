from entities.cards import Card
import settings as s
<<<<<<< Updated upstream
import random as r
import surface as sf
=======
import tkinter as tk 
from dictionaries import setcard as sc
import pygame 
import surface as su 
import CardLode as cl

def get_screen_resolution():
    root = tk.Tk()
    root.withdraw()

    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()


    root.destroy() # Zerstört das Root-Fenster nach dem Abrufen der Auflösung
    
    return screen_width, screen_height 

if __name__ == "__main__":
    width, height = get_screen_resolution()
    print(f"Bildschirmbreite: {width} Pixel")
    print(f"Bildschirmhöhe: {height} Pixel")
>>>>>>> Stashed changes


class CardLayout:
    def __init__( self, start_x, start_y, rows=s.ROWS, cols=s.COLS):
        self.cards = []
<<<<<<< Updated upstream
        for row in range (rows):
            row_cards = []
            for col in range (cols):
                x = start_x + col * (s.CARD_WIDTH + s.gap_width)
                y = start_y + row * (s.CARD_HEIGHT + s.gap_height)
                value = r.randint (-2, 12)
                card = Card(value, x, y, s.CARD_WIDTH, s.CARD_HEIGHT, is_face_up=False)
                row_cards.append(card)
            self.cards.append(row_cards)
=======
        for row in range(rows):
            row_cards = []
            for col in range(cols):
                x = start_x + col * (s.CARD_WIDTH + s.gap_width)
                y = start_y + row * (s.CARD_HEIGHT + s.gap_height)
                value = 0  # oder z.B. random.randint(-2, 12)
                card = Card(value, x, y, s.CARD_WIDTH, s.CARD_HEIGHT, is_face_up=False)
                row_cards.append(card)
            self.cards.append(row_cards) 
>>>>>>> Stashed changes

    def draw ( self, surface):
        for row in self.cards:
            for card in row:
                card.draw(surface)