from typing import List, Dict, Tuple
from collections import Counter
from enum import Enum, auto

from constants.constants import VALID_CARD_SUITS, VALID_CARD_FACES, VALID_CARDS


class HandRank(Enum):
    HIGH_CARD = auto()
    PAIR = auto()
    TWO_PAIR = auto()
    THREE_OF_A_KIND = auto()
    STRAIGHT = auto()
    FLUSH = auto()
    FULL_HOUSE = auto()
    FOUR_OF_A_KIND = auto()
    STRAIGHT_FLUSH = auto()
    ROYAL_FLUSH = auto()


class WinningHandSelector:

    @staticmethod
    def validate_hands(
        player_hands: Dict[str, List[str]], community_cards: List[str]
    ) -> bool:
        """
        Validate the format and uniqueness of all cards in play
        Args:
            player_hands: Dict of player name to their two hole cards
            community_cards: List of community cards
        Returns:
            bool: True if all hands are valid, raises ValueError otherwise
        """
        # Collect all cards for uniqueness check
        all_cards = []
        for cards in player_hands.values():
            all_cards.extend(cards)
        all_cards.extend(community_cards)

        # Check for duplicate cards
        if len(all_cards) != len(set(all_cards)):
            raise ValueError("Duplicate cards found in the game")

        # Validate each card's format and values
        for card in all_cards:
            if len(card) != 2:
                raise ValueError(
                    f"Invalid card format: {card}. Each card must be exactly 2 characters"
                )

            face, suit = card[0], card[1]

            if face not in VALID_CARD_FACES:
                raise ValueError(
                    f"Invalid card face: {face}. Must be one of: {VALID_CARD_FACES}"
                )

            if suit not in VALID_CARD_SUITS:
                raise ValueError(
                    f"Invalid card suit: {suit}. Must be one of: {VALID_CARD_SUITS}"
                )

        # Validate number of hole cards per player
        for player, cards in player_hands.items():
            if len(cards) != 2:
                raise ValueError(f"Player {player} must have exactly 2 hole cards")

        # Validate number of community cards
        if len(community_cards) not in [0, 3, 4, 5]:
            raise ValueError("Number of community cards must be 0, 3, 4, or 5")

        return True

    @staticmethod
    def evaluate_hands(
        player_hands: Dict[str, List[str]], community_cards: List[str]
    ) -> List[str]:
        """
        Evaluate all player hands and return the winner(s)
        Args:
            player_hands: Dict of player name to their two hole cards
            community_cards: List of community cards
        Returns:
            List of winning player names (multiple in case of tie)
        """
        hand_rankings = {}

        for player, hole_cards in player_hands.items():
            all_cards = hole_cards + community_cards
            hand_rank = WinningHandSelector._evaluate_single_hand(all_cards)
            hand_rankings[player] = hand_rank

        # Find highest ranking hand(s)
        max_rank = max(hand_rankings.values(), key=lambda x: (x[0].value, x[1]))
        winners = [
            player
            for player, rank in hand_rankings.items()
            if rank[0].value == max_rank[0].value and rank[1] == max_rank[1]
        ]

        return winners

    @staticmethod
    def _evaluate_single_hand(cards: List[str]) -> Tuple[HandRank, List[int]]:
        """
        Evaluate a single hand of 7 cards and return its rank and kickers
        Returns tuple of (HandRank, list of relevant card values for tiebreaking)
        """
        values = [card[0] for card in cards]
        suits = [card[1] for card in cards]
        value_counts = Counter(values)
        suit_counts = Counter(suits)

        # Convert card values to numbers
        numeric_values = [WinningHandSelector.CARD_VALUES[val] for val in values]
        numeric_values.sort(reverse=True)

        # Check for flush
        flush_suit = next(
            (suit for suit, count in suit_counts.items() if count >= 5), None
        )
        flush_cards = (
            [
                WinningHandSelector.CARD_VALUES[card[0]]
                for card in cards
                if card[1] == flush_suit
            ]
            if flush_suit
            else []
        )

        # Check for straight
        straight_high = WinningHandSelector._find_straight(numeric_values)

        # Royal Flush
        if (
            flush_suit
            and straight_high == 14
            and all(v in flush_cards for v in range(10, 15))
        ):
            return (HandRank.ROYAL_FLUSH, [14])

        # Straight Flush
        if (
            flush_suit
            and straight_high
            and all(
                v in flush_cards for v in range(straight_high - 4, straight_high + 1)
            )
        ):
            return (HandRank.STRAIGHT_FLUSH, [straight_high])

        # Four of a Kind
        fours = [val for val, count in value_counts.items() if count == 4]
        if fours:
            kicker = max(
                v
                for v in numeric_values
                if WinningHandSelector.CARD_VALUES[fours[0]] != v
            )
            return (
                HandRank.FOUR_OF_A_KIND,
                [WinningHandSelector.CARD_VALUES[fours[0]], kicker],
            )

        # Full House
        threes = [val for val, count in value_counts.items() if count == 3]
        pairs = [val for val, count in value_counts.items() if count == 2]
        if threes and pairs:
            return (
                HandRank.FULL_HOUSE,
                [
                    WinningHandSelector.CARD_VALUES[threes[0]],
                    WinningHandSelector.CARD_VALUES[pairs[0]],
                ],
            )

        # Flush
        if flush_cards:
            return (HandRank.FLUSH, sorted(flush_cards, reverse=True)[:5])

        # Straight
        if straight_high:
            return (HandRank.STRAIGHT, [straight_high])

        # Three of a Kind
        if threes:
            kickers = [
                v
                for v in numeric_values
                if WinningHandSelector.CARD_VALUES[threes[0]] != v
            ][:2]
            return (
                HandRank.THREE_OF_A_KIND,
                [WinningHandSelector.CARD_VALUES[threes[0]]] + kickers,
            )

        # Two Pair
        if len(pairs) >= 2:
            pairs_values = sorted(
                [WinningHandSelector.CARD_VALUES[p] for p in pairs], reverse=True
            )[:2]
            kicker = max(v for v in numeric_values if v not in pairs_values)
            return (HandRank.TWO_PAIR, pairs_values + [kicker])

        # One Pair
        if pairs:
            kickers = [
                v
                for v in numeric_values
                if WinningHandSelector.CARD_VALUES[pairs[0]] != v
            ][:3]
            return (
                HandRank.PAIR,
                [WinningHandSelector.CARD_VALUES[pairs[0]]] + kickers,
            )

        # High Card
        return (HandRank.HIGH_CARD, numeric_values[:5])

    @staticmethod
    def _find_straight(values: List[int]) -> int:
        """Find the highest straight in the values list, return highest card value or None"""
        values = sorted(set(values), reverse=True)

        # Check for Ace-low straight
        if set([14, 2, 3, 4, 5]).issubset(set(values)):
            return 5

        # Check for regular straights
        for i in range(len(values) - 4):
            if values[i] - values[i + 4] == 4:
                return values[i]

        return None
