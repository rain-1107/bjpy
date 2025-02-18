from BJEngine import Hand, TableDeck, Card
from typing import Callable


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
    def __init__(self, bet_callback: Callable, turn_callback: Callable, name: str = "Local"):
        super().__init__(name=name)
        self.place_bet = bet_callback
        self.turn = turn_callback


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
