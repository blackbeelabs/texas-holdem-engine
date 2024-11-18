from enum import Enum
from typing import List, Tuple

from engine.deck import Card, Deck
from engine.player import Player

from utils.WinningHandSelector import WinningHandSelector


class BettingRound(Enum):
    PREFLOP = "preflop"
    FLOP = "flop"
    TURN = "turn"
    RIVER = "river"


class PlayerAction(Enum):
    FOLD = "fold"
    CHECK = "check"
    CALL = "call"
    RAISE = "raise"


class Bet:
    def __init__(self, player: Player, amount: int):
        self.player = player
        self.amount = amount


class SingleGame:
    def __init__(
        self,
        players: List[Player] = [],
        small_blind_position: int = 0,
        small_blind_bet: int = 10,
        big_blind_bet: int = 20,
    ):
        # About the blinds
        self.small_blind_position: int = small_blind_position
        self.small_blind_bet: int = small_blind_bet
        self.big_blind_bet: int = big_blind_bet
        # About the players
        self.players: List[Player] = players
        self.current_player_index: int = 0
        # About the deck
        self.deck = Deck()
        # About the betting round, the active players, and the discard pile
        self.current_betting_round = BettingRound.PREFLOP
        self.discard_pile: List[Card] = []
        self.community_cards: List[Card] = []
        # About the bets
        self.bets: List[Bet] = []

    def register_player(self, player: Player):
        """Register a player to the game"""
        self.players.append(player)
        self.active_players.append(player)

    def deal_hole_cards(self):
        """Deal two cards to each player"""
        for _ in range(2):
            for player in self.players:
                player.receive_card(self.deck.deal())
        print(f"Dealt hole cards to {len(self.players)} players")

    def deal_community_cards(self):
        """Deal community cards based on current betting round"""

        def _check_community_cards_against_betting_round():
            if self.current_betting_round == BettingRound.PREFLOP:
                raise ValueError("Community cards cannot be dealt before the flop")
            elif self.current_betting_round == BettingRound.FLOP:
                if len(self.community_cards) == 3:
                    raise ValueError("Flop already dealt")
            elif self.current_betting_round == BettingRound.TURN:
                if len(self.community_cards) == 4:
                    raise ValueError("Turn already dealt")
            elif self.current_betting_round == BettingRound.RIVER:
                if len(self.community_cards) == 5:
                    raise ValueError("River already dealt")

        if self.current_betting_round == BettingRound.FLOP:
            _check_community_cards_against_betting_round()
            # Burn a card
            self.discard_pile.append(self.deck.deal())
            self.community_cards.extend([self.deck.deal() for _ in range(3)])
        elif self.current_betting_round in [BettingRound.TURN, BettingRound.RIVER]:
            # Burn a card
            self.discard_pile.append(self.deck.deal())
            self.community_cards.append(self.deck.deal())

    def post_blinds(self):
        """Post small and big blinds"""
        if len(self.players) < 2:
            raise ValueError("Not enough players to start a round")

        self.bets.append(Bet(self.players[0], self.small_blind_bet))
        self.bets.append(Bet(self.players[1], self.big_blind_bet))

    def get_pot(self):
        """Get the total amount in the pot"""
        return sum([bet.amount for bet in self.bets])

    def process_player_action(
        self, player_index: int, action: PlayerAction, amount: int = 0
    ):
        """Process a player's action (fold, check, call, raise)"""
        player = self.players[player_index]
        if action == PlayerAction.FOLD:
            player.is_active = False
        elif action in [PlayerAction.CALL, PlayerAction.RAISE]:
            self.bets.append(Bet(player, amount))
        elif action == PlayerAction.CHECK:
            pass
        else:
            raise ValueError(f"Invalid player action: {action}")

    def advance_betting_round(self):
        """Advance to the next betting round"""
        if self.current_betting_round == BettingRound.PREFLOP:
            print(
                f"Betting round advancing from {BettingRound.PREFLOP.value} to {BettingRound.FLOP.value}."
            )
            self.current_betting_round = BettingRound.FLOP
        elif self.current_betting_round == BettingRound.FLOP:
            print(
                f"Betting round advancing from {BettingRound.FLOP.value} to {BettingRound.TURN.value}."
            )
            self.current_betting_round = BettingRound.TURN
        elif self.current_betting_round == BettingRound.TURN:
            print(
                f"Betting round advancing from {BettingRound.TURN.value} to {BettingRound.RIVER.value}."
            )
            self.current_betting_round = BettingRound.RIVER
        else:
            raise ValueError(
                f"Invalid advance_betting_round call. Current betting round is {self.current_betting_round.value}."
            )

    def resolve_winner(self):
        """Resolve the winner of the current betting round"""
        winning_player = WinningHandSelector.select_winner(
            self.players, self.community_cards
        )

    def print_current_state(self):
        """Print the current state of the game"""
        print(f"Current betting round: {self.current_betting_round}")
        print("Players:")
        for player in self.players:
            print(
                f"  {player.name} ({'active' if player.is_active else 'inactive'}): {player.get_hand_string()}"
            )
        print("Community cards:")
        if len(self.community_cards) == 0:
            print("  (No community cards)")
        else:
            for card in self.community_cards:
                print(f"  {card}")
        print("Deck:")
        self.deck.print_deck()
        print("Bets:")
        for bet in self.bets:
            print(f"  {bet.player.name}: {bet.amount}")
        print(f"Pot: {self.get_pot()}")
