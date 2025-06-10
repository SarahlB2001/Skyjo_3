from entities.cards import Card
import settings as s
import random as r
import surface as sf


class CardLayout:
    def __init__( self, start_x, start_y, rows=3, cols=4):
        self.cards = []
        for row in range (rows):
            row_cards = []
            for col in range (cols):
                x = start_x + col * (s.CARD_WIDTH + sf.gap_width )
                y = start_y + row * (s.CARD_HEIGHT + sf.gap_height)
                value = r.randint (-2, 12)
                card = Card(value, x, y, s.CARD_WIDTH, s.CARD_HEIGHT, is_face_up=False)
                row_cards.append(card)
            self.cards.append(row_cards)

    def draw ( self, surface):
        for row in self.cards:
            for card in row:
                card.draw(surface)