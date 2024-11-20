from engine.classes.Deck import Deck

if __name__ == "__main__":
    deck = Deck(do_not_shuffle=True)
    print(deck)

    deck = Deck()
    print()
    print(deck)
    while not deck.empty():
        print(deck.deal())
