VALID_CARD_FACES = {
    "2",
    "3",
    "4",
    "5",
    "6",
    "7",
    "8",
    "9",
    "T",
    "J",
    "Q",
    "K",
    "A",
}

VALID_CARD_SUITS = {"S", "H", "D", "C"}

VALID_CARDS = {face + suit for face in VALID_CARD_FACES for suit in VALID_CARD_SUITS}

CARD_VALUES = range(2, 15)

FACE_TO_VALUE = {face: value for face, value in zip(VALID_CARD_FACES, CARD_VALUES)}
