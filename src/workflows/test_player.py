from engine.classes.Player import Player
from engine.classes.Deck import Deck  # for convenience
from loguru import logger

if __name__ == "__main__":
    # Player
    player = Player(player_id=1, player_name="John")
    print(player)

    # Player with hands
    deck = Deck()

    player2 = Player(
        player_id=2,
        player_name="Jane",
    )
    player2.receive_card(deck.deal())
    player2.receive_card(deck.deal())
    print(player2)

    player3 = Player(
        player_id=3,
        player_name="Jim",
    )
    print(player3)
    player3.receive_card(deck.deal())
    player3.receive_card(deck.deal())
    try:
        player3.bet(100)
    except ValueError as e:
        logger.error(e)
    print(player3)
    try:
        player3.all_in()
    except ValueError as e:
        logger.error(e)
    print(player3)

    player4 = Player(
        player_id=4,
        player_name="Jill",
    )
    player4.update_is_active(True)
    player4.receive_card(deck.deal())
    player4.receive_card(deck.deal())
    try:
        player4.all_in()
    except ValueError as e:
        logger.error(e)
    print(player4)
    try:
        player4.all_in()
    except ValueError as e:
        logger.error(e)
    print(player4)
    try:
        player4.bet(10)
    except ValueError as e:
        logger.error(e)
    print(player4)
