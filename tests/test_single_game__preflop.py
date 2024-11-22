import pytest
from engine.classes.Player import Player
from engine.classes.Deck import Deck
from engine.classes.SingleGame import SingleGame, PlayerAction

from engine.classes.Card import VERBOSE_NAMES


def test_preflop_betting_round_is_preflop():
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
    game.register_players(player1, player2, player3)
    game.advance_betting_round()
    assert game.get_betting_round() == "preflop"


def test_preflop_game_has_all_cards():

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
    game.register_players(player1, player2, player3)
    game.advance_betting_round()
    game.advance_betting_round()

    test_deck = Deck(new_deck=False)
    for card in game.get_deck().get_cards():
        test_deck.add_card(card)
    for card in game.get_discard_pile().get_cards():
        test_deck.add_card(card)
    for player in game.get_players():
        for card in player.get_hand().get_cards():
            test_deck.add_card(card)
    for card in game.get_community_cards().get_cards():
        test_deck.add_card(card)
    assert test_deck.get_deck_size() == 52
    assert set([card.verbose_name for card in test_deck.get_cards()]) == set(
        VERBOSE_NAMES
    )