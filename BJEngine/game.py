from typing import Self, Callable
from .deck import TableDeck, DiscardPile, Card
from .player import SkeletonPlayer, Dealer

STAGE_CLEAR = 0 
STAGE_BET = 1 
STAGE_DEAL = 2 
STAGE_HIT = 3
STAGE_REWARD = 4
STAGE_END = 5


class Game:
    def __init__(self, **kwargs):
        self.deck = TableDeck(number_of_decks=kwargs.get("number_of_decks", 4))
        self.discard_pile = DiscardPile()
        self.dealer = Dealer()
        self.players: list[SkeletonPlayer] = []
        self.player_data: list[dict[str, str | int]] = []
        self.max_players: int = kwargs.get("max_players", 1) 
        self.round: int = 0
        self.current_stage: int = STAGE_BET
        self.current_player: int = 0
        self._deck_empty_callbacks = []
        self._round_over_callbacks = []
    
    @property
    def on_deck_empty(self) -> Callable:
        def wrapper(function: Callable[[Self], None]):
            self._deck_empty_callbacks.append(function)
            return function

        return wrapper
    
    @property
    def on_round_over(self) -> Callable:
        def wrapper(function: Callable[[Self], None]):
            self._round_over_callbacks.append(function)
            return function
        
        return wrapper

    def add_player(self, player: SkeletonPlayer) -> None:
        if len(self.players) >= self.max_players:
            raise Exception("Cannot add more players than max players")
        self.players.append(player)
        self.player_data.append({"bet": 0, "playing": True})
    
    def draw_cards(self) -> None:
        self.round += 1
        self.dealer.draw_cards((self.safely_draw_card(), self.safely_draw_card()))
        for player in self.players:
            player.draw_cards((self.safely_draw_card(), self.safely_draw_card()))
    
    # Would recommend using this instead of drawing cards willy nilly and getting index errors and none types
    def safely_draw_card(self) -> Card: 
        card = self.deck.draw()
        if not card:
            for func in self._deck_empty_callbacks:
                func(self)
            self.deck.add_cards(self.discard_pile.pop())
            self.deck.shuffle()
            card = self.deck.draw()
            if not card:
                raise IndexError("Idk how this has hapened?? 0 decks perhaps")
        return card
    
    # Defines what happens in one "action" of the game, advancing on from the previous state
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
            bet = self.players[self.current_player].place_bet()
            # Cheeky bit of *bet validation*
            if 0 >= bet > self.players[self.current_player].chips:
                self.player_data[self.current_player]["playing"] = False
            else:
                self.players[self.current_player].chips -= bet
                self.player_data[self.current_player]["bet"] = bet 
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
            if not self.player_data[self.current_player]["playing"]:
                self.current_player += 1
                return
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
                self.players[self.current_player].chips += int(self.player_data[self.current_player]["bet"]) * 2
            self.current_player += 1
            if self.current_player >= len(self.players):
                self.current_stage = STAGE_END
                self.current_player = 0
        if self.current_stage == STAGE_END:
            for func in self._round_over_callbacks:
                func(self)
    
    def new_round(self):
        self.current_stage = STAGE_CLEAR
