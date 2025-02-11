import time

import BJEngine

def bet() -> int:
    return int(input("How much do you want to bet? "))

def turn() -> bool:
    if input("Do you want to draw a card? (y/n) ").lower() == "y":
        return True
    return False


if __name__ == '__main__':
    game = BJEngine.Game(max_players=2)
    player = BJEngine.LocalPlayer(name="Ryan", turn_callback=turn, bet_callback=bet)
    bot1 = BJEngine.BotPlayer(name="Bot1")
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
        print()
        time.sleep(1)

