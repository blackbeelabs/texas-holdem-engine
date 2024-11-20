from engine.classes.Card import VALID_CARDS

if __name__ == "__main__":
    print(VALID_CARDS)

    for card_name, [card_face_rank, card_face_suit] in VALID_CARDS.items():
        print(card_name, card_face_rank, card_face_suit)
