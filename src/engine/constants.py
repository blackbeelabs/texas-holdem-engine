import itertools

# 2 to Ace
# Maps card ranks to their numerical values (2-14, where Ace is 14)
VALID_CARD_RANKS = {
    "2": 2,
    "3": 3,
    "4": 4,
    "5": 5,
    "6": 6,
    "7": 7,
    "8": 8,
    "9": 9,
    "10": 10,
    "J": 11,
    "Q": 12,
    "K": 13,
    "A": 14,
}

# Spades, Hearts, Diamonds, Clubs
VALID_CARD_SUITS = {
    "Spades": "S",
    "Hearts": "H",
    "Diamonds": "D",
    "Clubs": "C",
}

# 52 cards
VALID_CARDS = {
    f"{rank}-{suit}": f"{rank}-{VALID_CARD_SUITS[suit]}-{VALID_CARD_RANKS[rank]}"
    for rank, suit in itertools.product(VALID_CARD_RANKS, VALID_CARD_SUITS)
}
