from typing import List, Optional
from random import shuffle
from engine.classes.Card import Card, VALID_CARDS


class Deck:
    def __init__(self, new_deck: bool = True, do_not_shuffle: bool = False):
        self.cards = []
        if new_deck:
            self.cards = [
                Card(card_name, card_face_rank, card_face_suit)
                for card_name, [card_face_rank, card_face_suit] in VALID_CARDS
            ]
        if not do_not_shuffle:
            self._shuffle()

    def _shuffle(self) -> None:
        """Shuffle the deck"""
        shuffle(self.cards)

    def deal(self) -> Optional[Card]:
        """Deal one card from the deck"""
        if self.get_deck_size() > 0:
            return self.cards.pop()
        raise ValueError("No cards remaining in the deck")

    def add_card(self, card: Card) -> None:
        """Add a card to the deck"""
        self.cards.append(card)

    def update_is_active(self, is_active: bool) -> None:
        """Update the is_active attribute of the deck"""
        self.is_active = is_active

    def empty(self) -> bool:
        """Check if the deck is empty"""
        return self.get_deck_size() == 0

    def get_deck_size(self) -> int:
        """Return the number of cards remaining in the deck"""
        return len(self.cards)

    def get_cards(self) -> List[Card]:
        """Return the list of cards remaining in the deck"""
        return self.cards

    def _get_cards_as_list(self) -> List[str]:
        """use str() if not you'll get only the card address"""
        return [str(card) for card in self.cards]

    def _get_cards_as_concatenated_string(self) -> str:
        """use str() if not you'll get only the card address"""
        return ", ".join(self._get_cards_as_list())

    def __str__(self) -> str:
        if self.empty():
            return "Deck([])"
        return f"Deck([{', '.join(self._get_cards_as_list())}])"

    def __eq__(self, other: "Deck") -> bool:
        return (
            self._get_cards_as_concatenated_string()
            == other._get_cards_as_concatenated_string()
        )
