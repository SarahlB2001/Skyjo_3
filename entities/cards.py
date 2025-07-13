"""
Diese Klasse Card repräsentiert die einzelnen Spielkarten im Spiel Skyjo.
Jede Karte hat folgende Eigenschaften:
- value: Der Wert der Karte ( -2 bis 12).
- is_face_up: Gibt an, ob die Karte offen (True) oder verdeckt (False) ist.
- Bilder: Bilddateien werden zu Anfang geladen und für die grafische Darstellung verwendet.
Die Klasse enthält eine __repr__-Methode für Debugging und wird genutzt,
um die Kartenlogik und die grafische Darstellung der Karten zu verwalten.
"""
import pygame
import random


# Definieren eines benutzerdefiniertes Event für das Umdrehen einer Karte
CARD_FLIP_EVENT = pygame.USEREVENT + 1

# Laden der Bilder für die Karten
CARD_IMAGES = {value: pygame.image.load(f"Karten_png/card_{value}.png") for value in range(-2, 13)}
CARD_BACK_IMAGE = pygame.image.load("Karten_png/card_back.png")

class Card:
    def __init__(self, value, x, y, width, height, is_face_up=False):
        """
        Repräsentiert eine einzelne Karte.
        - value: Der Wert der Karte (z. B. -2 bis 12 in Skyjo).
        - is_face_up: Gibt an, ob die Karte offen (True) oder verdeckt (False) ist.
        """
        self.value = value
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.is_face_up = is_face_up
        self.removed = False 
        self.front_image = pygame.transform.scale(CARD_IMAGES[value], (width, height))
        self.back_image = pygame.transform.scale(CARD_BACK_IMAGE, (width, height))
        self.rect = pygame.Rect(x, y, width, height)
    
    def draw(self, screen):
        # Entfernte Karten nicht zeichnen
        if self.removed:
            return
            
        if self.is_face_up:
            screen.blit(self.front_image, (self.x, self.y))
        else:
            screen.blit(self.back_image, (self.x, self.y))

   
    def __repr__(self):
        """Gibt eine lesbare Darstellung der Karte zurück."""
        return f"Card(value={self.value}, is_face_up={self.is_face_up})"

def create_deck():
    # Deck mit allen Karten erstellen 
    # Jede Karte kommt mehrmals vor (-2 und 12 je 5x, andere je 10x)
    card_distribution = {
        -2: 5,  # -2 kommt 5x vor
        12: 5,  # 12 kommt 5x vor
    }
    for value in range(-1, 12):  # Werte von -1 bis 11 kommen je 10x vor
        card_distribution[value] = 10

    deck = []
    for value, count in card_distribution.items():
        for _ in range(count):
            deck.append(Card(value))

    random.shuffle(deck)  # Mische das Deck
    return deck # Gibt eine Liste mit allen Karten zurück