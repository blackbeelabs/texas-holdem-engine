from engine.classes.Card import VALID_CARD_RANKS, VALID_CARD_SUITS
import itertools

if __name__ == "__main__":

    VALID_CARDS = []
    for (verbose_rank, rank), (verbose_suit, suit) in itertools.product(
        VALID_CARD_RANKS, VALID_CARD_SUITS
    ):
        VALID_CARDS.append((f"{verbose_rank}-{verbose_suit}", rank, suit))

    print(VALID_CARDS)
