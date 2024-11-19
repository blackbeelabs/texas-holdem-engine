from engine.player import Player
from engine.single_game import SingleGame

from engine.constants import VALID_CARDS


def test_single_game_has_all_cards(game):
    test_deck = []
    for player in game.players:
        for card in player.hand:
            test_deck.append(card.card_name)
    print(len(test_deck))
    for card in game.community_cards:
        test_deck.append(card.card_name)
    print(len(test_deck))
    for card in game.discard_pile:
        test_deck.append(card.card_name)
    print(len(test_deck))
    for card in game.deck.cards:
        test_deck.append(card.card_name)
    print(len(test_deck))
    print(test_deck)
    assert len(test_deck) == 52
    assert len(set(test_deck)) == 52
    assert set(test_deck) == set(VALID_CARDS.keys())


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
