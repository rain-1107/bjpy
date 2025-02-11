from BJEngine import TableDeck, Dealer, SkeletonPlayer, LocalPlayer


class Game:
    def __init__(self, max_players: int = 1):
        self.deck = TableDeck()
        self.dealer = Dealer()
        self.players: list[SkeletonPlayer] = []
        self.bets = []
        self.max_players: int = max_players
        self.round: int = 0
        self.current_stage: int = -1 # -2: Clearing previous round, -1: Placing bets, 0: Dealing cards, 1: Hit\Stand, 2: Rewarding bets
        self.current_player: int = 0

    def add_player(self, player: SkeletonPlayer) -> None:
        if len(self.players) >= self.max_players:
            raise Exception("Cannot add more players than max players")
        self.players.append(player)
    
    def draw_cards(self) -> None:
        self.round += 1
        self.dealer.draw_cards((self.deck.draw(), self.deck.draw()))
        for player in self.players:
            player.draw_cards((self.deck.draw(), self.deck.draw()))
    
    def tick(self) -> None:
        # Clearing cards from previous round
        if self.current_stage == -2:
            self.dealer.hand.clear()
            for player in self.players:
                player.hand.clear()
            self.current_stage += 1
            return
        # Placing bets
        if self.current_stage == -1:
            current_player = self.players[self.current_player]
            bet = current_player.place_bet()
            current_player.chips -= bet
            self.bets.append(bet)
            self.current_player += 1
            if self.current_player == len(self.players):
                self.current_stage += 1
                self.current_player = 0
            return
        # Drawing cards
        if self.current_stage == 0:
            self.draw_cards()
            self.current_stage += 1
            return
        # Playing round
        if self.current_stage == 1 and self.current_player < len(self.players):
            wants_to_hit = self.players[self.current_player].turn()
            if wants_to_hit:
                self.players[self.current_player].hit(self.deck.draw())
            if self.players[self.current_player].hand.value > 21 or not wants_to_hit:
                self.current_player += 1
        # Dealer turns cards
        if self.current_stage == 1 and self.current_player == len(self.players):
            self.dealer.turn_all_cards()
            self.current_player += 1
            return
        # Dealer hits/stands
        if self.current_stage == 1 and self.current_player == len(self.players) + 1:
            highest_hand_value = 16
            for player in self.players:
                if 21 >= player.hand.value > highest_hand_value:
                    highest_hand_value = player.hand.value
            wants_to_hit = self.dealer.turn(highest_hand_value)
            if wants_to_hit:
                self.dealer.hit(self.deck.draw())
                return
            self.current_stage += 1
            self.current_player = 0
            return
        # Reward bets
        if self.current_stage == 2:
            if 21 >= self.players[self.current_player].hand.value > self.dealer.hand.value or self.dealer.hand.value > 21:
                self.players[self.current_player].chips += self.bets[self.current_player] * 2
            self.current_player += 1
            if self.current_player >= len(self.players):
                self.current_stage = -2
                self.current_player = 0