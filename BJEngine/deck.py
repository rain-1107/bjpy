from random import shuffle

SUITS = ("Hearts", "Diamonds", "Clubs", "Spades")
NUMBERS = ("Ace", "2", "3", "4", "5", "6", "7", "8", "9",
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


class Deck:
    def __init__(self):
        self.cards: list[Card] = []
        for suit in SUITS:
            for num in NUMBERS:
                self.cards.append(Card(suit, num))
        self.shuffle()

    def shuffle(self) -> None:
        shuffle(self.cards)

    def draw(self) -> Card | None:
        if len(self.cards) == 0:
            return None
        return self.cards.pop(len(self.cards) - 1)

    def repopulate(self) -> None:
        self.cards = []
        for suit in SUITS:
            for num in NUMBERS:
                self.cards.append(Card(suit, num))
        self.shuffle()

    @property
    def n_cards(self) -> int:
        return len(self.cards)


class TableDeck:
    def __init__(self, number_of_decks: int = 4):
        self.decks: list[Deck] = []
        for i in range(number_of_decks):
            self.decks.append(Deck())
        self.current_deck = 0

    def draw(self) -> Card | None:
        if self.current_deck >= len(self.decks):
            return None
        card = self.decks[self.current_deck].draw()
        if self.decks[self.current_deck].n_cards == 0:
            self.current_deck += 1
        return card

    def reshuffle(self) -> None:
        for deck in self.decks:
            deck.repopulate()
        self.current_deck = 0