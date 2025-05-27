"""Dieses Modul definiert die Klasse `Stack`, die einen Kartenstapel und einen Ablagestapel repräsentiert. 
Es ermöglicht das Mischen, Ziehen und Ablegen von Karten. Die Klasse enthält Methoden zum Mischen des Stapels, Ziehen von Karten 
vom Stapel oder Ablagestapel, und Ablegen von Karten auf den Ablagestapel. Benutzerdefinierte Events werden 
ausgelöst, um auf das Ziehen und Ablegen von Karten zu reagieren."""

import pygame
import random
from .cards import Card, CARD_FLIP_EVENT

# Definiere benutzerdefinierte Events für den Kartenstapel
CARD_DRAW_EVENT = pygame.USEREVENT + 2  # Event für das Ziehen einer Karte
CARD_DISCARD_EVENT = pygame.USEREVENT + 3  # Event für das Ablegen einer Karte

class Stack:
    def __init__(self, deck=None):
        # Repräsentiert den Kartenstapel und den Ablagestapel.
        # deck: Eine Liste von Card-Objekten, die den Stapel bilden.
        self.deck = deck if deck else []  # Der Kartenstapel (Liste von Card-Objekten)
        self.discard_pile = None  # Ablagestapel (nur die oberste Karte)

    def shuffle(self):
        """Mische den Kartenstapel."""
        random.shuffle(self.deck)

    def draw_card(self):
        """
        Ziehe die oberste Karte vom Kartenstapel.
        :return: Die gezogene Karte oder None, wenn der Stapel leer ist.
        """
        if len(self.deck) == 0:
            print("Der Kartenstapel ist leer!")
            return None

        card = self.deck.pop(0)  # Entferne die oberste Karte
        self._post_draw_event(card)  # Löse ein Event aus
        return card

    def draw_from_discard(self):
        """
        Ziehe die oberste Karte vom Ablagestapel.
        :return: Die gezogene Karte oder None, wenn der Ablagestapel leer ist.
        """
        if not self.discard_pile:
            return None

        card = self.discard_pile
        self.discard_pile = None  # Entferne die Karte vom Ablagestapel
        return card

    def discard_card(self, card):
        """
        Lege eine Karte auf den Ablagestapel.
        - card: Die Karte, die abgelegt werden soll.
        """
        self.discard_pile = card  # Speichere die Karte als oberste Karte des Ablagestapels
        self._post_discard_event(card)  # Löse ein Event aus
        print(f"Karte abgelegt: {card}")

    def _post_draw_event(self, card):
        """
        Löst ein Event aus, wenn eine Karte vom Kartenstapel gezogen wird.
        - card: Die gezogene Karte.
        """
        event_data = {
            "value": card.value,
            "is_face_up": card.is_face_up
        }
        draw_event = pygame.event.Event(CARD_DRAW_EVENT, event_data)
        pygame.event.post(draw_event)

    def _post_discard_event(self, card):
        """
        Löst ein Event aus, wenn eine Karte auf den Ablagestapel gelegt wird.
        - card: Die abgelegte Karte.
        """
        event_data = {
            "value": card.value,
            "is_face_up": card.is_face_up
        }
        discard_event = pygame.event.Event(CARD_DISCARD_EVENT, event_data)
        pygame.event.post(discard_event)

    def __repr__(self):
        # Gibt eine lesbare Darstellung des Stapels zurück
        discard_info = f"Discard: {self.discard_pile}" if self.discard_pile else "Discard: leer"
        return f"Stack({len(self.deck)} Karten, {discard_info})"