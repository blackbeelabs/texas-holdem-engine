import pytest
from engine.classes.Player import Player
from engine.classes.Deck import Deck
from engine.classes.SingleGame import SingleGame, PlayerAction

from engine.classes.Card import VERBOSE_NAMES
from loguru import logger


@pytest.fixture
def preflop_game():
    game = SingleGame(big_blind_bet=2)
    player1 = Player(player_id=1, player_name="John", starting_stack=10)
    player2 = Player(player_id=2, player_name="Jane", starting_stack=10)
    player3 = Player(player_id=3, player_name="Jim", starting_stack=20)
    game.register_players(player1, player2, player3)
    game.advance_betting_round()  # notstarted to preflop
    return game


def test_preflop_game_has_all_cards_after_dealing_hole_cards(preflop_game):

    test_deck = Deck(new_deck=False)
    for card in preflop_game.get_deck().get_cards():
        test_deck.add_card(card)
    for player in preflop_game.get_players():
        for card in player.get_hand().get_cards():
            print(card)
            test_deck.add_card(card)
    assert test_deck.get_deck_size() == 52
    assert set([card.verbose_name for card in test_deck.get_cards()]) == set(
        VERBOSE_NAMES
    )


def test_preflop_betting_round_is_preflop(preflop_game):
    assert preflop_game.get_betting_round() == "preflop"


def test_preflop_game_has_all_cards(preflop_game):

    test_deck = Deck(new_deck=False)
    for card in preflop_game.get_deck().get_cards():
        test_deck.add_card(card)
    for card in preflop_game.get_discard_pile().get_cards():
        test_deck.add_card(card)
    for player in preflop_game.get_players():
        for card in player.get_hand().get_cards():
            test_deck.add_card(card)
    for card in preflop_game.get_community_cards().get_cards():
        test_deck.add_card(card)
    assert test_deck.get_deck_size() == 52
    assert set([card.verbose_name for card in test_deck.get_cards()]) == set(
        VERBOSE_NAMES
    )


def test_all_players_have_two_hole_cards(preflop_game):

    for player in preflop_game.get_players():
        assert len(player.get_hand().get_cards()) == 2
        assert len(set(player.get_hand()._get_cards_as_list())) == 2


def test_pot_amount_after_blinds_are_posted(preflop_game):

    big_blind: int = preflop_game.get_big_blind_bet()
    small_blind: int = int(big_blind / 2)
    assert preflop_game.get_pot() == big_blind + small_blind
