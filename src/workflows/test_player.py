from engine.player import Player
from engine.deck import Deck

if __name__ == "__main__":
    # Player
    player = Player(player_id=1, player_name="John")
    print(player)

    # Player with hands
    deck = Deck()
    print(deck)

    player2 = Player(
        player_id=2,
        player_name="Jane",
    )
    player2.receive_card(deck.deal())
    player2.receive_card(deck.deal())
    print(deck.deal())
    card = deck.deal()
    print(card)
    print(player2)
