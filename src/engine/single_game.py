from enum import Enum
from typing import List, Dict, Optional, Any

from engine.deck import Card, Deck
from engine.player import Player

from utils.WinningHandSelector import WinningHandSelector
from loguru import logger


class BettingRound(Enum):
    NOTSTARTED = "notstarted"
    NEWGAME = "newgame"
    PREFLOP = "preflop"
    FLOP = "flop"
    TURN = "turn"
    RIVER = "river"
    ENDED = "ended"


class PlayerAction(Enum):
    FOLD = "fold"
    CHECK = "check"
    CALL = "call"
    RAISE = "raise"


class Bet:
    def __init__(self, player: Player, amount: int):
        self.player = player
        self.amount = amount

    def __str__(self) -> str:
        return f"{self.player.player_name}: {self.amount}"


class SingleGame:
    def __init__(
        self,
        small_blind_position: int = 0,
        small_blind_bet: int = 10,
        big_blind_bet: int = 20,
    ):
        # About the blinds
        self.small_blind_position: int = small_blind_position
        self.small_blind_bet: int = small_blind_bet
        self.big_blind_bet: int = big_blind_bet
        # About the players
        self.players: List[Player] = []
        self.current_player_index: int = 0
        # About the deck
        self.deck = Deck()
        # About the betting round, the active players, and the discard pile
        self.current_betting_round = BettingRound.NOTSTARTED
        self.discard_pile: List[Card] = []
        self.community_cards: List[Card] = []
        # About the bets
        self.bets: List[Bet] = []
        # ...to handle re-raising
        self.current_bet: int = 0
        self.last_raiser_player_index: Optional[int] = None
        self.bets_per_player: Dict[Player, int] = {}

    def register_player(self, player: Player):
        """Register a player to the game"""
        self.players.append(player)
        logger.info(
            f"Player {player.player_id} ({player.player_name}) has joined the game."
        )

    def register_players(self, players: List[Player]):
        """Register multiple players to the game"""
        for player in players:
            self.register_player(player)

    def place_bet(self, player: Player, amount: int):
        """Place a bet"""
        self.bets.append(Bet(player, amount))
        player.current_stack -= amount
        player.has_acted = True
        logger.info(f"Player {player.player_id} has placed a bet of {amount}.")

    def post_blinds(self):
        """Post small and big blinds"""
        if len(self.players) < 2:
            raise ValueError("Not enough players to start a round")

        self.place_bet(self.players[0], self.small_blind_bet)
        self.place_bet(self.players[1], self.big_blind_bet)
        logger.info("Small and big blinds have been posted.")

    def deal_card_to_player(self, player: Player):
        """Deal a card to a player"""
        player.receive_card(self.deck.deal())
        logger.info(f"Dealt 1 card to Player {player.player_id}")

    def deal_hole_cards(self):
        """Deal two cards to each player"""
        for _ in range(2):
            for player in self.players:
                self.deal_card_to_player(player)
        logger.info(f"Dealt hole cards to {len(self.players)} players")

    def discard_card(self):
        """Discard a card"""
        self.discard_pile.append(self.deck.deal())
        logger.info(f"Discarded 1 card")

    def deal_community_card(self):
        """Deal a community card"""
        self.community_cards.append(self.deck.deal())
        logger.info(f"Dealt 1 community card")

    def _update_betting_street_on_raise(self, player: Player, amount: int):
        pass

    def process_player_action(
        self, player_index: int, action: PlayerAction, amount: int = 0
    ):
        def _validate_player_action_turn():
            # TODO: Implement the logic for the turn
            pass

        player = self.players[player_index]

        # Validate minimum raise amount
        if action == PlayerAction.RAISE:
            min_raise = self.current_bet * 2
            if amount < min_raise:
                raise ValueError(f"Raise amount must be at least {min_raise}")
            self.current_bet = amount
            self.last_raiser = player

        elif action == PlayerAction.CALL:
            if amount != self.current_bet:
                raise ValueError(f"Call amount must be {self.current_bet}")

        elif action == PlayerAction.CHECK:
            if self.current_bet > 0:
                raise ValueError("Cannot check when there's an active bet")

        # Update bets tracking
        if action in [PlayerAction.CALL, PlayerAction.RAISE]:
            current_player_total = self.bets_per_player.get(player, 0)
            additional_amount = amount - current_player_total
            self.bets.append(Bet(player, additional_amount))
            self.bets_per_player[player] = amount

    def deal_community_cards(self):
        """Deal community cards based on current betting round"""

        def _check_community_cards_against_betting_round():
            if (
                self.current_betting_round == BettingRound.PREFLOP
                or self.current_betting_round == BettingRound.NEWGAME
                or self.current_betting_round == BettingRound.NOTSTARTED
                or self.current_betting_round == BettingRound.ENDED
            ):
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
            self.discard_card()
            for _ in range(3):
                self.deal_community_card()
        elif self.current_betting_round in [BettingRound.TURN, BettingRound.RIVER]:
            # Burn a card
            self.discard_card()
            self.deal_community_card()

    def reset_betting_street(self):
        """Reset betting tracking for a new street"""
        self.current_bet = 0
        self.last_raiser_player_index = None
        self.bets_per_player = {}

    def advance_betting_round(self):
        """Advance to the next betting round"""
        if self.current_betting_round == BettingRound.NOTSTARTED:
            logger.info(
                f"Betting round advancing from {BettingRound.NOTSTARTED.value} to {BettingRound.NEWGAME.value}."
            )
            self.current_betting_round = BettingRound.NEWGAME
        elif self.current_betting_round == BettingRound.NEWGAME:
            logger.info(
                f"Betting round advancing from {BettingRound.NEWGAME.value} to {BettingRound.PREFLOP.value}."
            )
            self.current_betting_round = BettingRound.PREFLOP
        elif self.current_betting_round == BettingRound.PREFLOP:
            logger.info(
                f"Betting round advancing from {BettingRound.PREFLOP.value} to {BettingRound.FLOP.value}."
            )
            self.current_betting_round = BettingRound.FLOP
        elif self.current_betting_round == BettingRound.FLOP:
            logger.info(
                f"Betting round advancing from {BettingRound.FLOP.value} to {BettingRound.TURN.value}."
            )
            self.current_betting_round = BettingRound.TURN
        elif self.current_betting_round == BettingRound.TURN:
            logger.info(
                f"Betting round advancing from {BettingRound.TURN.value} to {BettingRound.RIVER.value}."
            )
            self.current_betting_round = BettingRound.RIVER
        elif self.current_betting_round == BettingRound.RIVER:
            logger.info(
                f"Betting round advancing from {BettingRound.RIVER.value} to {BettingRound.ENDED.value}."
            )
            self.current_betting_round = BettingRound.ENDED
        else:
            raise ValueError(
                f"Invalid call to advance_betting_round(). Current betting round is {self.current_betting_round.value}."
            )

    def get_next_actionable_player_index(self):
        """Get the index of the next actionable player"""
        for i in range(self.current_player_index + 1, len(self.players)):
            if self.players[i].is_active:
                return i
        return 0

    def get_remaining_betting_street(self) -> List[int]:
        """Get the remaining player actions for the current betting round"""
        return [
            player.player_id
            for player in self.players
            if player.is_active and not player.has_acted
        ]

    def resolve_winner(self):
        """Resolve the winner of the current betting round"""
        winning_player = WinningHandSelector.select_winner(
            self.players, self.community_cards
        )
        return 0

    def get_pot(self):
        """Get the total amount in the pot"""
        return sum([bet.amount for bet in self.bets])

    def get_last_raiser_index(self):
        """Get the index of the last player who raised"""
        for i in range(len(self.players) - 1, -1, -1):
            if self.players[i].has_acted:
                return i
        return 0

    def get_last_bet_amount(self):
        """Get the amount of the last bet in the current betting round"""
        return self.bets[-1].amount

    def get_current_state(self) -> Dict[str, Any]:
        """Return a dictionary with the current state of the game"""
        return {
            "current_betting_round": self.current_betting_round.value,
            "players": [str(player) for player in self.players],
            "community_cards": [str(card) for card in self.community_cards],
            # "deck": str(self.deck),
            "pot": self.get_pot(),
        }

    def __str__(self) -> str:
        return str(self.get_current_state())
