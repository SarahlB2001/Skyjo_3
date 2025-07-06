from entities.cards import Card
import settings as s
import random as r
import surface as sf


class CardLayout:
    def __init__( self, start_x, start_y, spieler_id, matrix, rows=s.ROWS, cols=s.COLS):
        self.spieler_id = spieler_id
        self.cards = []
        for row in range (rows):
            row_cards = []
            for col in range (cols):
                value = matrix[row][col]
                x = start_x + col * (s.CARD_WIDTH + s.gap_width)
                y = start_y + row * (s.CARD_HEIGHT + s.gap_height)
                card = Card(value, x, y, s.CARD_WIDTH, s.CARD_HEIGHT, is_face_up=False)
                row_cards.append(card)
            self.cards.append(row_cards)

    def draw (self, surface):
        for row in self.cards:
            for card in row:
                card.draw(surface)
