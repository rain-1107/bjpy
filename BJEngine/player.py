from BJEngine import Hand, TableDeck, Card
from typing import Callable, Self


class SkeletonPlayer:
    def __init__(self, name: str = "Player"):
        self.hand = Hand()
        self.name = name
        self.chips = 10

    def draw_cards(self, cards: tuple[Card, Card]) -> None:
        self.hand.add(cards[0])
        self.hand.add(cards[1])

    def turn(self) -> bool:
        return False

    def hit(self, card: Card) -> None:
        self.hand.add(card)

    def turn_all_cards(self) -> None:
        for card in self.hand:
            card.face_up = True

    def place_bet(self) -> int:
        return 1


class LocalPlayer(SkeletonPlayer):
    def __init__(self, name: str = "Local", **kwargs):
        super().__init__(name=name)
        self._turn_callback: Callable[[Self], bool]
        self._bet_callback: Callable[[Self], int]
    
    def turn(self) -> bool:
        return self._turn_callback(self)
    
    def place_bet(self) -> int:
        return self._bet_callback(self)

    @property
    def on_turn(self):
        def wrapper(function: Callable[[Self], bool]):
            self._turn_callback = function
            return function

        return wrapper

    @property
    def on_bet(self):
        def wrapper(function: Callable[[Self], int]):
            self._bet_callback = function
            return function

        return wrapper


class BotPlayer(SkeletonPlayer):
    def __init__(self, name: str = "Bot"):
        super().__init__(name=name)

    def turn(self) -> bool:
        if self.hand.value < 19:
            return True
        return False


class Dealer(SkeletonPlayer):
    def __init__(self, name: str = "Dealer"):
        super().__init__(name=name)

    def draw_cards(self, cards: tuple[Card, Card]) -> None:
        cards[0].face_up = False
        self.hand.add(cards[0])
        self.hand.add(cards[1])

    def turn(self) -> bool:
        if self.hand.value < 17:
            return True
        return False

