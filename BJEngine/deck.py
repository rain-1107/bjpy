from random import shuffle
from typing import List, Tuple

SUITS = ("Hearts", "Clubs", "Diamond", "Spades")
NUMBERS = ("2", "3", "4", "5", "6", "7", "8", "9",
           "10", "Jack", "Queen", "King", "Ace")
NUMBER_TO_VALUE = {"Ace": 1, "2": 2, "3": 3, "4": 4, "5": 5, "6": 6, "7": 7,
                   "8": 8, "9": 9, "10": 10, "Jack": 10, "Queen": 10, "King": 10}


class Card:
    def __init__(self, suit: str, number: str, face_up: bool = True):
        self.face_up = face_up
        self.suit = suit
        self.number = number
        self.value = NUMBER_TO_VALUE[number]

    def __str__(self):
        if self.face_up:
            return f"{self.number} of {self.suit}"
        return "???"


class DiscardPile:
    def __init__(self):
        self.cards: List[Card] = []

    def add_cards(self, cards: List[Card] | Tuple[Card]) -> None:
        self.cards.extend(cards)


    def pop(self, n_of_cards: int = 0) -> List[Card]:
        if n_of_cards == 0:
            temp = self.cards
            self.cards = []
            return temp
        return self.cards[:n_of_cards]

class TableDeck:
    def __init__(self, number_of_decks: int = 4):
        self.max_cards = number_of_decks * 52
        self.cards: list[Card] = []
        for _ in range(number_of_decks):
            for suit in SUITS:
                for num in NUMBERS:
                    self.cards.append(Card(suit, num))
        shuffle(self.cards)

    def draw(self) -> Card | None:
        if len(self.cards) > 0:
            return self.cards.pop(len(self.cards) - 1)
        return None

    def shuffle(self):
        shuffle(self.cards)

    def add_cards(self, cards: List[Card]) -> None:
        if len(self.cards) + len(cards) > self.max_cards:
            raise OverflowError("Too many cards to add")
        self.cards.extend(cards)
