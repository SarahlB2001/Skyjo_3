from entities.cards import Card
import settings as s
import random as r
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

''''
class CardLayout:
    def __init__( self, start_x, start_y, rows=s.ROWS, cols=s.COLS):
        pygame.draw.rect(su.WINDOW, s.BLACK, (start_x + sc.card1 ["x"], start_y + sc.card1 ["y"], sc.card_width, sc.card_height))
        pygame.draw.rect(su.WINDOW, s.BLACK, (start_x + sc.card2 ["x"], start_y + sc.card2 ["y"], sc.card_width, sc.card_height))
        pygame.draw.rect(su.WINDOW, s.BLACK, (start_x + sc.card3 ["x"], start_y + sc.card3 ["y"], sc.card_width, sc.card_height))
        pygame.draw.rect(su.WINDOW, s.BLACK, (start_x + sc.card4 ["x"], start_y + sc.card4 ["y"], sc.card_width, sc.card_height))
        pygame.draw.rect(su.WINDOW, s.BLACK, (start_x + sc.card5 ["x"], start_y + sc.card5 ["y"], sc.card_width, sc.card_height))
        pygame.draw.rect(su.WINDOW, s.BLACK, (start_x + sc.card6 ["x"], start_y + sc.card6 ["y"], sc.card_width, sc.card_height))
        pygame.draw.rect(su.WINDOW, s.BLACK, (start_x + sc.card7 ["x"], start_y + sc.card7 ["y"], sc.card_width, sc.card_height))
        pygame.draw.rect(su.WINDOW, s.BLACK, (start_x + sc.card8 ["x"], start_y + sc.card8 ["y"], sc.card_width, sc.card_height))
        pygame.draw.rect(su.WINDOW, s.BLACK, (start_x + sc.card9 ["x"], start_y + sc.card9 ["y"], sc.card_width, sc.card_height))
        pygame.draw.rect(su.WINDOW, s.BLACK, (start_x + sc.card10 ["x"], start_y + sc.card10 ["y"], sc.card_width, sc.card_height))
        pygame.draw.rect(su.WINDOW, s.BLACK, (start_x + sc.card11 ["x"], start_y + sc.card11 ["y"], sc.card_width, sc.card_height))
        pygame.draw.rect(su.WINDOW, s.BLACK, (start_x + sc.card12 ["x"], start_y + sc.card12 ["y"], sc.card_width, sc.card_height))

        
            #     card = Card(0, x, y, s.CARD_WIDTH, s.CARD_HEIGHT, is_face_up=False)
            #     row_cards.append(card)
            # self.cards.append(row_cards) 
            #     y = start_y + row * (s.CARD_HEIGHT + s.gap_height)
            #     value = r.randint (-2, 12)
            #     card = Card(value, x, y, s.CARD_WIDTH, s.CARD_HEIGHT, is_face_up=False)
            #     row_cards.append(card)
            # self.cards.append(row_cards)

    def draw ( self, surface):
        for row in self.cards:
            for card in row:
                card.draw(surface)

            '''