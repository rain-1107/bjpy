import BJEngine

if __name__ == '__main__':
    table = BJEngine.GameDeck()
    hand = BJEngine.Hand()
    hand.add(BJEngine.Card("Hearts", "Ace"))
    hand.add(BJEngine.Card("Hearts", "Ace"))
    hand.add(table.draw())
    print(hand)
    print(hand.value)
