import time

import BJEngine


def main():
    game = BJEngine.Game(max_players=2, number_of_decks=1)
    for i in range(50):
        game.discard_pile.add_cards([game.safely_draw_card(), ])
    player = BJEngine.LocalPlayer(name="Ryan")

    @player.on_bet
    def bet(ctx: BJEngine.LocalPlayer) -> int:
        return int(input("Place a bet: ")) 
    
    @player.on_turn
    def turn(ctx: BJEngine.LocalPlayer) -> bool:
        return input("Hit? [y/n]: ") == "y"

    bot1 = BJEngine.BotPlayer(name="Bot1")
    
    @game.on_deck_empty
    def test(ctx: BJEngine.Game):
        print("hello")

    @game.on_round_over
    def test2(ctx: BJEngine.Game):
        for player in ctx.players:
            print(f"{player.name}: {player.chips} chips")

    game.add_player(player)
    game.add_player(bot1)
    for player in game.players:
        print(f"{player.name}: {player.chips} chips")
    while True:
        game.tick()
        print(f"\n{game.dealer.name}: {game.dealer.hand} (Value: {game.dealer.hand.value})")
        for player in game.players:
            print(f"{player.name}: {player.hand} (Value: {player.hand.value})")
        time.sleep(1)


if __name__ == '__main__':
    main() 
