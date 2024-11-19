from typing import List, Optional
from engine.deck import Card


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
        self.hand: List[Card] = []  # Player's hole cards
        # Player status. Use these statuses to track the player's progress in the game
        # Whether player is still in the current single game
        self.is_active: bool = True
        # Player's position in the current game, starts from 0. 0 is the dealer
        self.is_all_in: bool = False
        self.has_acted: bool = False

    def reset_player_for_new_single_game(self):
        """Reset the player's attributes to their initial values"""
        self.hand = []
        self.is_active = True
        self.is_all_in = False
        self.has_acted = False

    def receive_card(self, card: Card):
        """Add a card to the player's hand"""
        if len(self.hand) < 2:
            self.hand.append(card)

    def __str__(self):
        return str(self.to_dict())

    def _get_hand_as_list(self):
        return [str(card) for card in self.hand]

    def to_dict(self):
        return {
            "player_id": self.player_id,
            "player_name": self.player_name,
            "starting_stack": self.starting_stack,
            "current_stack": self.current_stack,
            "hand": self._get_hand_as_list(),
            "is_active": self.is_active,
            "is_all_in": self.is_all_in,
            "has_acted": self.has_acted,
        }
