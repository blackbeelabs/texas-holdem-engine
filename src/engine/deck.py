from typing import List, Optional
from random import shuffle
from engine.constants import VALID_CARDS

fr


class Card:
    def __init__(self, card_name: str, short_name: str):
        # Parse the card name to get suit and rank
        self.rank, self.suit = card_name.split("-")
        self.card_name = card_name
        self.short_name = short_name
        # Extract numerical rank from short_name (last part after splitting by '-')
        self.rank_numerical_value = int(short_name.split("-")[-1])

    def __str__(self) -> str:
        return f"Card(rank={self.rank}, suit={self.suit}, card_name={self.card_name}, rank_value={self.rank_numerical_value})"


class Deck:
    def __init__(self):
        self.cards: List[Card] = []
        self.new_shuffled_deck()

    def new_shuffled_deck(self) -> None:
        """Create a new deck of 52 cards, shuffled."""
        self.cards = [
            Card(card_name, short_name) for card_name, short_name in VALID_CARDS.items()
        ]
        self._shuffle()

    def _shuffle(self) -> None:
        """Shuffle the deck"""
        shuffle(self.cards)

    def deal(self) -> Optional[Card]:
        """Deal one card from the deck"""
        if len(self.cards) > 0:
            return self.cards.pop()
        raise ValueError("No cards remaining in the deck")

    def get_deck(self) -> List[Card]:
        """Return the number of cards remaining in the deck"""
        return self.cards

    def print_deck(self) -> None:
        """Print the deck"""
        for card in self.cards:
            print(card)

    def empty(self) -> bool:
        """Check if the deck is empty"""
        return self.get_deck_size() == 0

    def get_deck_size(self) -> int:
        """Return the number of cards remaining in the deck"""
        return len(self.cards)

    def __str__(self) -> str:
        return f"Deck(cards={self.cards})"
