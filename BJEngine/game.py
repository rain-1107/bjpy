from typing import Self, Callable
from .deck import TableDeck, DiscardPile, Card
from .player import SkeletonPlayer, Dealer

STAGE_CLEAR = -2
STAGE_BET = -1
STAGE_DEAL = 0
STAGE_HIT = 1
STAGE_REWARD = 2
STAGE_END = 3


class Game:
    def __init__(self, **kwargs):
        self.deck = TableDeck(number_of_decks=kwargs.get("number_of_decks", 4))
        self.discard_pile = DiscardPile()
        self.dealer = Dealer()
        self.players: list[SkeletonPlayer] = []
        self.bets = []
        self.max_players: int = kwargs.get("max_players", 1) 
        self.round: int = 0
        self.current_stage: int = STAGE_BET
        self.current_player: int = 0
        self._deck_empty_callbacks = []

    def on_deck_empty(self, function: Callable[[Self], None]) -> Callable[[None], None]:
        def wrapper(self):
            self._deck_empty_callbacks.append(function)

        return wrapper

    def add_player(self, player: SkeletonPlayer) -> None:
        if len(self.players) >= self.max_players:
            raise Exception("Cannot add more players than max players")
        self.players.append(player)
    
    def draw_cards(self) -> None:
        self.round += 1
        self.dealer.draw_cards((self.safely_draw_card(), self.safely_draw_card()))
        for player in self.players:
            player.draw_cards((self.safely_draw_card(), self.safely_draw_card()))

    def safely_draw_card(self) -> Card:
        card = self.deck.draw()
        if not card:
            self.deck.add_cards(self.discard_pile.pop())
            self.deck.shuffle()
            card = self.deck.draw()
            if not card:
                raise IndexError("Idk how this has hapened?? 0 decks perhaps")
        return card
    
    def tick(self) -> None:
        # Clearing cards from previous round
        if self.current_stage == STAGE_CLEAR:
            self.discard_pile.add_cards(self.dealer.hand.clear())
            for player in self.players:
                self.discard_pile.add_cards(player.hand.clear())
            self.current_stage = STAGE_BET
            return
        # Placing bets
        if self.current_stage == STAGE_BET:
            current_player = self.players[self.current_player]
            bet = current_player.place_bet()
            current_player.chips -= bet
            self.bets.append(bet)
            self.current_player += 1
            if self.current_player == len(self.players):
                self.current_stage = STAGE_DEAL
                self.current_player = 0
            return
        # Drawing cards
        if self.current_stage == STAGE_DEAL:
            self.draw_cards()
            self.current_stage = STAGE_HIT
            return
        # Playing round
        if self.current_stage == STAGE_HIT and self.current_player < len(self.players):
            wants_to_hit = self.players[self.current_player].turn()
            if wants_to_hit:
                self.players[self.current_player].hit(self.safely_draw_card())
            if self.players[self.current_player].hand.value > 21 or not wants_to_hit:
                self.current_player += 1
        # Dealer turns cards
        if self.current_stage == STAGE_HIT and self.current_player == len(self.players):
            self.dealer.turn_all_cards()
            self.current_player += 1
            return
        # Dealer hits/stands
        if self.current_stage == STAGE_HIT and self.current_player == len(self.players) + 1:
            wants_to_hit = self.dealer.turn()
            if wants_to_hit:
                self.dealer.hit(self.safely_draw_card())
                return
            self.current_stage = STAGE_REWARD
            self.current_player = 0
            return
        # Reward bets
        if self.current_stage == STAGE_REWARD:
            if 21 >= self.players[self.current_player].hand.value > self.dealer.hand.value or self.dealer.hand.value > 21:
                self.players[self.current_player].chips += self.bets[self.current_player] * 2
            self.current_player += 1
            if self.current_player >= len(self.players):
                self.current_stage = STAGE_END
                self.current_player = 0

    def is_round_over(self) -> bool:
        return self.current_stage == STAGE_END

    def new_round(self) -> None:
        self.current_stage = STAGE_CLEAR
