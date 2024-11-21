from typing import List
from engine.classes.Card import Card
from engine.classes.Deck import Deck
from loguru import logger


class Player:
    def __init__(
        self,
        player_id: int,
        player_name: str,
        starting_stack: int = 1000,
    ):
        # Player attributes
        self.player_id: int = player_id
        self.player_name: str = player_name
        # Player stack.
        # Amount of money/chips the player has coming into the game
        # Starting stack and current stack are the same when the game starts
        self.starting_stack: int = starting_stack
        self.current_stack: int = starting_stack
        # Player hand
        self.hand: Deck = Deck(new_deck=False)  # Player's hole cards
        # Player status. Use these statuses to track the player's progress in the game
        # Whether player is still in the current single game
        self.is_active: bool = False
        # Player's position in the current game, starts from 0. 0 is the dealer
        self.is_all_in: bool = False
        self.has_acted: bool = False

    def reset_player_for_new_single_game(self):
        """Reset the player's attributes to their initial values"""
        self.hand = Deck(new_deck=False)
        self.is_active = True
        self.is_all_in = False
        self.has_acted = False
        logger.info(
            f"Player {self.player_id}: Reset for new single game. Current stack: {self.current_stack}"
        )

    def receive_card(self, card: Card):
        """Add a card to the player's hand"""
        if self.hand.get_deck_size() < 2:
            self.hand.add_card(card)

    def update_is_active(self, is_active: bool) -> None:
        """Update the is_active attribute of the player"""
        self.is_active = is_active

    def bet(self, amount: int):
        """Place a bet"""
        if not self.is_active:
            raise ValueError(
                f"Player {self.player_id}: Cannot bet. Player is not active."
            )
        if self.has_acted:
            raise ValueError(
                f"Player {self.player_id}: Cannot bet. Player has already acted."
            )
        if amount > self.current_stack:
            raise ValueError(
                f"Player {self.player_id}: Cannot bet. Bet amount is greater than the player's current stack."
            )
        self.current_stack -= amount
        self.has_acted = True
        logger.info(
            f"Player {self.player_id}: Placed bet of {amount}. Current stack: {self.current_stack}"
        )

    def active(self):
        self.is_active = True

    def yet_to_act(self):
        self.has_acted = False

    def all_in(self):
        """Set the player's current stack to 0"""
        if not self.is_active:
            raise ValueError(
                f"Player {self.player_id}: Cannot all-in. Player is not active."
            )
        if self.is_all_in:
            raise ValueError(
                f"Player {self.player_id}: Cannot all-in. Player is already all-in."
            )

        self.bet(self.current_stack)
        self.is_all_in = True
        logger.info(
            f"Player {self.player_id}: went all-in. Current stack: {self.current_stack}"
        )

    def __str__(self):
        return str(self.to_dict())

    def get_hand(self) -> Deck:
        return self.hand

    def _get_hand_as_list(self):
        return [str(card) for card in self.hand.cards]

    def to_dict(self):
        return {
            "player_id": self.player_id,
            "player_name": self.player_name,
            "starting_stack": self.starting_stack,
            "current_stack": self.current_stack,
            "hand": str(self.hand),
            "is_active": self.is_active,
            "is_all_in": self.is_all_in,
            "has_acted": self.has_acted,
        }

    def __eq__(self, other):
        return self.player_id == other.player_id
