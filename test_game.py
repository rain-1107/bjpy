import time

import BJEngine

def bet() -> int:
    return int(input("How much do you want to bet? "))

def turn() -> bool:
    if input("Do you want to draw a card? (y/n) ").lower() == "y":
        return True
    return False


if __name__ == '__main__':
    game = BJEngine.Game(max_players=2, number_of_decks=1)
    for i in range(50):
        game.discard_pile.add_cards([game.safely_draw_card(), ])
    player = BJEngine.LocalPlayer(name="Ryan", turn_callback=turn, bet_callback=bet)
    bot1 = BJEngine.BotPlayer(name="Bot1")
    
    @game.on_deck_empty
    def test(ctx: BJEngine.Game):
        print("hello")

    game.add_player(player)
    game.add_player(bot1)
    for player in game.players:
        print(f"{player.name}: {player.chips} chips")
    while True:
        game.tick()
        print(f"{game.dealer.name}: {game.dealer.hand} (Value: {game.dealer.hand.value})")
        for player in game.players:
            print(f"{player.name}: {player.hand} (Value: {player.hand.value})")
        if game.current_stage == -2:
            for player in game.players:
                print(f"{player.name}: {player.chips} chips")
        if game.is_round_over():
            game.new_round()
            for player in game.players:
                print(f"{player.name}: {player.chips} chips")
        print()
        time.sleep(1)

