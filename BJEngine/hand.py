from BJEngine import Card


class Hand:
    def __init__(self):
        self.cards = []

    def add(self, card: Card) -> None:
        self.cards.append(card)

    @property
    def value(self) -> int:
        total = 0
        aces = 0
        for card in self.cards:
            if card.number == "Ace":
                aces += 1
            else:
                total += card.value
        for i in range(aces):
            total += 1
            if total <= 11:
                total += 10
        return total

    def __str__(self):
        text = ""
        for card in self.cards:
            text += str(card) + "\n"
        return text