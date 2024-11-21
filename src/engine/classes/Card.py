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
    VALID_CARDS.append((f"{verbose_rank}-{verbose_suit}", (rank, suit)))


class Card:

    def __init__(self, card_name: str, card_face_rank: int, card_face_suit: str):
        # Parse the card name to get suit and rank
        self.rank, self.suit = card_face_rank, card_face_suit
        self.verbose_name = card_name

    def __str__(self) -> str:
        return f"Card({str(self.to_dict())})"

    def to_dict(self):
        return {
            "card_name": self.verbose_name,
            "rank": self.rank,
            "suit": self.suit,
        }
