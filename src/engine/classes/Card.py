import itertools

# 2 to Ace
# Maps card ranks to their numerical values (2-14, where Ace is 14)

VALID_CARD_RANKS = (
    ("2", 2),
    ("3", 3),
    ("4", 4),
    ("5", 5),
    ("6", 6),
    ("7", 7),
    ("8", 8),
    ("9", 9),
    ("10", 10),
    ("J", 11),
    ("Q", 12),
    ("K", 13),
    ("A", 14),
)

# Spades, Hearts, Diamonds, Clubs
VALID_CARD_SUITS = (
    ("Club", "C"),
    ("Diamond", "D"),
    ("Heart", "H"),
    ("Spade", "S"),
)

# 52 cards
VALID_CARDS = []
for (verbose_rank, rank), (verbose_suit, suit) in itertools.product(
    VALID_CARD_RANKS, VALID_CARD_SUITS
):
    VALID_CARDS.append((f"{verbose_rank} {verbose_suit}", (rank, suit)))
VERBOSE_NAMES = [v[0] for v in VALID_CARDS]
RANK_VALUES = [r[1] for r in VALID_CARD_RANKS]
SUIT_VALUES = [s[1] for s in VALID_CARD_SUITS]


class Card:

    def __init__(self, card_name: str, card_face_rank: int, card_face_suit: str):

        if card_name not in VERBOSE_NAMES:
            raise ValueError(f"Invalid card name: {card_name}")
        if card_face_rank not in RANK_VALUES:
            raise ValueError(f"Invalid rank: {card_face_rank}")
        if card_face_suit not in SUIT_VALUES:
            raise ValueError(f"Invalid suit: {card_face_suit}")

        # Parse the card name to get suit and rank
        self.rank, self.suit = card_face_rank, card_face_suit
        self.verbose_name = card_name

    def __str__(self) -> str:
        return (
            f'Card(card_name="{self.verbose_name}",rank={self.rank},suit="{self.suit}")'
        )

    def to_dict(self):
        return {
            "card_name": self.verbose_name,
            "rank": self.rank,
            "suit": self.suit,
        }
