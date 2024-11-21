from engine.classes.Player import Player
from engine.classes.Deck import Deck
from engine.classes.SingleGame import SingleGame, PlayerAction

from engine.classes.Card import VERBOSE_NAMES


def test_single_game_has_all_cards():

    game = SingleGame()
    player1 = Player(
        player_id=1,
        player_name="John",
    )
    player2 = Player(
        player_id=2,
        player_name="Jane",
    )
    player3 = Player(
        player_id=3,
        player_name="Jim",
    )
    game.register_players([player1, player2, player3])
    game.advance_betting_round()  # New game to Preflop
    game.advance_betting_round()  # Preflop to Flop
    game.advance_betting_round()  # Flop to Turn
    game.advance_betting_round()  # Turn to River

    test_deck = Deck(new_deck=False)
    for player in game.get_players():
        for card in player.get_hand().get_cards():
            test_deck.add_card(card)
    # Community cards
    for card in game.get_community_cards().get_cards():
        test_deck.add_card(card)
    # Discard pile
    for card in game.get_discard_pile().get_cards():
        test_deck.add_card(card)
    # Remaining deck
    for card in game.get_deck().get_cards():
        test_deck.add_card(card)
    assert test_deck.get_deck_size() == 52
    assert set([card.verbose_name for card in test_deck.get_cards()]) == set(
        VERBOSE_NAMES
    )


# if __name__ == "__main__":


#     game = SingleGame()
#     game.register_players([player1, player2, player3, player4])

#     game.advance_betting_round()
#     game.post_blinds()
#     game.deal_hole_cards()

#     game.advance_betting_round()
#     game.deal_community_cards()

#     game.advance_betting_round()
#     game.deal_community_cards()

#     game.advance_betting_round()
#     game.deal_community_cards()

#     game.advance_betting_round()
#     game.deal_community_cards()

#     game.advance_betting_round()
#     game.deal_community_cards()

#     test_single_game_has_all_cards(game)
