from engine.classes.Player import Player
from engine.classes.Deck import Deck
from engine.classes.SingleGame import SingleGame, PlayerAction

from engine.classes.Card import VALID_CARDS


def test_single_game_has_all_cards(game):
    test_deck = Deck(new_deck=False)
    # Player's hands
    for player in game.players:
        for card in player.hand.cards:
            test_deck.add_card(card)
    # Community cards
    for card in game.community_cards:
        test_deck.add_card(card)
    # Discard pile
    for card in game.discard_pile:
        test_deck.add_card(card)
    # Remaining deck
    for card in game.deck.cards:
        test_deck.add_card(card)
    assert test_deck.get_deck_size() == 52
    assert set([card.verbose_name for card in test_deck.cards]) == set(
        VALID_CARDS.keys()
    )


if __name__ == "__main__":
    player1 = Player(player_id=1, player_name="John", starting_stack=100)
    player2 = Player(player_id=2, player_name="Jane", starting_stack=100)
    player3 = Player(player_id=3, player_name="Jim", starting_stack=100)
    player4 = Player(player_id=4, player_name="Jill", starting_stack=100)

    game = SingleGame()
    game.register_players([player1, player2, player3, player4])

    game.advance_betting_round()
    game.post_blinds()
    game.deal_hole_cards()

    game.advance_betting_round()
    game.deal_community_cards()

    game.advance_betting_round()
    game.deal_community_cards()

    game.advance_betting_round()
    game.deal_community_cards()

    game.advance_betting_round()
    game.deal_community_cards()

    game.advance_betting_round()
    game.deal_community_cards()

    test_single_game_has_all_cards(game)
