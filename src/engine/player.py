from typing import List, Optional
from engine.deck import Card


class Player:
    def __init__(self, name: str, stack: int = 1000):
        self.name: str = name
        self.stack: int = stack  # Amount of money/chips the player has
        self.hand: List[Card] = []  # Player's hole cards
        self.is_active: bool = True  # Whether player is still in the current hand
        self.position: int = 0

    def clear_hand(self):
        """Clear the player's hand"""
        self.hand = []

    def receive_card(self, card: Card):
        """Add a card to the player's hand"""
        if len(self.hand) < 2:
            self.hand.append(card)

    def get_hand_string(self):
        if len(self.hand) == 0:
            return "(No cards)"
        """Get a string representation of the player's hand"""
        hand_str = ", ".join([str(card) for card in self.hand])
        return f"{hand_str}"
