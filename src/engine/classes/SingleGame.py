from enum import Enum
from typing import List, Dict, Optional, Any

from engine.classes.Deck import Deck, Card
from engine.classes.Player import Player


# from engine.utils.WinningHandSelector import WinningHandSelector
from loguru import logger


class BettingRound(Enum):
    NOTSTARTED = "notstarted"
    PREFLOP = "preflop"
    FLOP = "flop"
    TURN = "turn"
    RIVER = "river"
    ENDED = "ended"


class PlayerAction(Enum):
    FOLD = "fold"
    BLIND = "blind"
    CHECK = "check"
    CALL = "call"
    RAISE = "raise"


class Bet:
    def __init__(self, player: Player, amount: int):
        self.player = player
        self.amount = amount

    def __str__(self) -> str:
        return f"{self.player.player_id}: {self.amount}"


class SingleGame:
    def __init__(
        self,
        big_blind_bet: int = 20,
    ):
        # About the blinds
        assert big_blind_bet > 0, "Big blind bet must be greater than 0"
        assert big_blind_bet % 2 == 0, "Big blind bet must be even"
        self.big_blind_bet: int = big_blind_bet
        self.small_blind_bet: int = big_blind_bet / 2
        # About the players
        self.all_players: List[Player] = (
            []
        )  # Already has the order for the full betting street
        self.active_players: List[Player] = []
        self.current_betting_street_players: List[Player] = []
        # About the deck
        self.deck = Deck()
        # About the betting round, the active players, and the discard pile
        self.current_betting_round = BettingRound.NOTSTARTED
        self.discard_pile: Deck = Deck(new_deck=False)
        self.community_cards: Deck = Deck(new_deck=False)
        # About the bets
        self.bets: Dict[str, List[Bet]] = {}
        # ...to handle re-raising
        self.current_bet: int = 0
        self.last_raiser_player_index: Optional[int] = None
        self.bets_per_player: Dict[Player, int] = {}
        logger.info("Game initialized.")

    def _log_state_in_debug_mode(self):
        logger.debug(f"Current betting round: {self.current_betting_round.value}")
        logger.debug(
            f"Active players: {[player.player_id for player in self.active_players]}"
        )
        logger.debug(
            f"Betting street: {[player.player_id for player in self.current_betting_street_players]}"
        )
        logger.debug(f"Bets: {str(self.bets)}")
        logger.debug(f"Pot: {self.get_pot()}")
        logger.debug(
            f"Stacks per player in current round: {self._stacks_per_player_in_current_round()}"
        )

    def register_player(self, player: Player):
        """Register a player to the game"""
        player.update_is_active(True)
        self.all_players.append(player)
        logger.info(
            f"Player {player.player_id} ({player.player_name}) has joined the game."
        )
        logger.debug(
            f"All players: {[player.player_id for player in self.all_players]}"
        )

    def register_players(self, players: List[Player]):
        """Register multiple players to the game"""
        for player in players:
            self.register_player(player)
        logger.info(f"Registered {len(players)} players to the game.")

    def set_active_players(self):
        """Set the active players"""
        self.active_players = [
            player for player in self.all_players if player.is_active
        ]

    def place_bet(self, player: Player, action: PlayerAction, amount: int):
        """Place a bet"""
        player.bet(amount)
        if 0 < amount:
            current_round_bets = self.bets.get(self.current_betting_round.value, [])
            current_round_bets.append(Bet(player, amount))
            self.bets[self.current_betting_round.value] = current_round_bets
            logger.info(f"Player {player.player_id} has placed a bet of {amount}.")
        else:
            logger.info(f"Player {player.player_id} has checked.")
        self.update_betting_street_on_bet(player, action)

    def _post_small_blind(self):
        small_blind_player = self.get_next_actionable_player()
        self.place_bet(small_blind_player, PlayerAction.BLIND, self.small_blind_bet)
        # Add small blind player to betting street. He needs to call the big blind
        # to stay in the game.
        small_blind_player.yet_to_act()
        self.add_player_to_end_of_betting_street(small_blind_player)

    def _post_big_blind(self):
        self.place_bet(
            self.get_next_actionable_player(), PlayerAction.BLIND, self.big_blind_bet
        )

    def post_blinds(self):
        if len(self.active_players) < 2:
            raise ValueError("Not enough players to start a round")
        """Post small blind"""
        self._post_small_blind()
        self._log_state_in_debug_mode()
        self._post_big_blind()
        self._log_state_in_debug_mode()
        logger.info("Small and big blinds have been posted.")
        self.advance_betting_round()

    def deal_card_to_player(self, player: Player):
        """Deal a card to a player"""
        player.receive_card(self.deck.deal())
        logger.info(f"Dealt 1 card to Player {player.player_id}")

    def deal_hole_cards(self):
        """Deal two cards to each player"""
        for _ in range(2):
            for player in self.active_players:
                self.deal_card_to_player(player)
        logger.info(f"Dealt hole cards to {len(self.active_players)} players")

    def discard_card(self):
        """Discard a card"""
        self.discard_pile.add_card(self.deck.deal())
        logger.info(f"Discarded 1 card")

    def deal_community_card(self):
        """Deal a community card"""
        self.community_cards.add_card(self.deck.deal())
        logger.info(f"Dealt 1 community card")

    def _update_betting_street_on_raise(self, player: Player, amount: int):
        pass

    def _validate_player_action(
        self, player_id: int, action: PlayerAction, amount: int = 0
    ):
        # Validate if player_id is in the game
        if not player_id in [
            player.player_id for player in self.current_betting_street_players
        ]:
            logger.error(
                f"Error processing player action: Player {player_id} is not in the game."
            )
            raise ValueError(f"Player {player_id} is not in the game.")
        # Validate if player_id is next to act
        if not self.betting_street_players[0].player_id == player_id:
            logger.error(
                f"Error processing player action: Player {player_id} is not next to act."
            )
            raise ValueError(f"Player {player_id} is not next to act.")
        # Validate if player has folded
        if not self.betting_street_players[0].is_active:
            logger.error(
                f"Error processing player action: Player {player_id} has folded."
            )
            raise ValueError(f"Player {player_id} has folded.")

    def _stacks_per_player_in_current_round(self):
        return {
            player.player_id: sum(
                [
                    bet.amount
                    for bet in self.bets.get(self.current_betting_round.value, [])
                    if bet.player == player
                ]
            )
            for player in self.active_players
        }

    def process_player_action(
        self, player_id: int, action: PlayerAction, amount: int = 0
    ):
        logger.info(f"Processing player action: {action} for player {player_id}")
        logger.debug(f"Next player to act: {self.betting_street_players[0].player_id}")
        self._validate_player_action(player_id, action, amount)
        player = self.get_next_actionable_player()
        if action == PlayerAction.CHECK:
            if self.current_bet_amount > 0:
                logger.error(
                    f"Cannot check when there's an active bet. Current bet: {self.current_bet_amount}"
                )
                raise ValueError("Cannot check when there's an active bet")
        elif action == PlayerAction.CALL:
            # Player has to topup to current bet amount to call
            max_stack_in_current_betting_round = max(
                self._stacks_per_player_in_current_round().values()
            )
            logger.debug(
                f"Max stack in current betting round: {max_stack_in_current_betting_round}"
            )
            player_stack_in_current_round = self._stacks_per_player_in_current_round()[
                player.player_id
            ]
            logger.debug(
                f"Player {player.player_id}'s stack in current round: {player_stack_in_current_round}"
            )
            player_topup_needed_to_call = (
                max_stack_in_current_betting_round - player_stack_in_current_round
            )
            logger.debug(
                f"Player {player.player_id} has to topup {player_topup_needed_to_call} to successfully call."
            )
            self.place_bet(player, action, player_topup_needed_to_call)

        self._log_state_in_debug_mode()

    def deal_community_cards(self):
        """Deal community cards based on current betting round"""

        def _check_community_cards_against_betting_round():
            if (
                self.current_betting_round == BettingRound.PREFLOP
                or self.current_betting_round == BettingRound.NOTSTARTED
                or self.current_betting_round == BettingRound.ENDED
            ):
                raise ValueError("Community cards cannot be dealt before the flop")
            elif self.current_betting_round == BettingRound.FLOP:
                if self.community_cards.get_deck_size() == 3:
                    raise ValueError("Flop already dealt")
            elif self.current_betting_round == BettingRound.TURN:
                if self.community_cards.get_deck_size() == 4:
                    raise ValueError("Turn already dealt")
            elif self.current_betting_round == BettingRound.RIVER:
                if self.community_cards.get_deck_size() == 5:
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

    def reset_betting_street_for_new_round(self):
        """Reset betting tracking for a new round"""
        for player in self.active_players:
            player.yet_to_act()
        self.current_betting_street_players = [
            player for player in self.all_players if player.is_active
        ]
        self._log_state_in_debug_mode()

    def add_player_to_end_of_betting_street(self, player: Player):
        """Add a player to the end of the betting street"""
        self.betting_street_players.append(player)

    def update_betting_street_on_bet(self, player: Player, action: PlayerAction):
        """Update the betting street after a bet"""
        if (
            action == PlayerAction.BLIND
            or action == PlayerAction.CHECK
            or action == PlayerAction.CALL
        ):
            self.betting_street_players = [
                player
                for player in self.current_betting_street_players
                if (player.is_active and not player.has_acted)
            ]

    def advance_betting_round(self):
        """Advance to the next betting round"""
        if self.current_betting_round == BettingRound.NOTSTARTED:
            logger.info(
                f"Game starting. Betting round advancing from "
                + f"{BettingRound.NOTSTARTED.value} to "
                + f"{BettingRound.PREFLOP.value}."
            )
            self.current_betting_round = BettingRound.PREFLOP
            # Enlist all players to the list active players
            self.set_active_players()
            self.deal_hole_cards()
            self.reset_betting_street_for_new_round()
        elif self.current_betting_round == BettingRound.PREFLOP:
            logger.info(
                f"Betting round advancing from "
                + f"{BettingRound.PREFLOP.value} to "
                + f"{BettingRound.FLOP.value}."
            )
            self.current_betting_round = BettingRound.FLOP
            self.deal_community_cards()
            self.reset_betting_street_for_new_round()
        elif self.current_betting_round == BettingRound.FLOP:
            logger.info(
                f"Betting round advancing from "
                + f"{BettingRound.FLOP.value} to "
                + f"{BettingRound.TURN.value}."
            )
            self.current_betting_round = BettingRound.TURN
            self.deal_community_cards()
            self.reset_betting_street_for_new_round()
        elif self.current_betting_round == BettingRound.TURN:
            logger.info(
                f"Betting round advancing from "
                + f"{BettingRound.TURN.value} to "
                + f"{BettingRound.RIVER.value}."
            )
            self.current_betting_round = BettingRound.RIVER
            self.deal_community_cards()
            self.reset_betting_street_for_new_round()
        else:
            raise ValueError(
                f"Invalid call to advance_betting_round(). Current betting round is {self.current_betting_round.value}."
            )

    def get_next_actionable_player(self):
        """Get the next actionable player"""
        return self.current_betting_street_players[0]

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

    def get_players(self) -> List[Player]:
        """Get the players"""
        return self.all_players

    def get_deck(self) -> Deck:
        """Get the deck"""
        return self.deck

    def get_discard_pile(self) -> Deck:
        """Get the discard pile"""
        return self.discard_pile

    def get_community_cards(self) -> Deck:
        """Get the community cards"""
        return self.community_cards

    def get_pot(self):
        """Get the total amount in the pot"""
        if len(self.bets) == 0:
            return 0
        return sum(
            [bet.amount for bet in self.bets.get(self.current_betting_round.value, [])]
        )

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
