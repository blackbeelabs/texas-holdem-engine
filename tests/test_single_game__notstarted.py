import pytest
from engine.classes.Player import Player
from engine.classes.Deck import Deck
from engine.classes.SingleGame import SingleGame, PlayerAction

from engine.classes.Card import VERBOSE_NAMES


def test_new_game_has_all_cards():

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

    test_deck = Deck(new_deck=False)
    for card in game.get_deck().get_cards():
        test_deck.add_card(card)
    assert test_deck.get_deck_size() == 52
    assert set([card.verbose_name for card in test_deck.get_cards()]) == set(
        VERBOSE_NAMES
    )


def test_game_has_all_cards_after_dealing_hole_cards():

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
    player4 = Player(
        player_id=3,
        player_name="Jill",
    )
    game.register_players(player1, player2, player3, player4)
    game.advance_betting_round()
    test_deck = Deck(new_deck=False)
    for card in game.get_deck().get_cards():
        test_deck.add_card(card)
    for player in game.get_players():
        for card in player.get_hand().get_cards():
            test_deck.add_card(card)
    assert test_deck.get_deck_size() == 52
    assert set([card.verbose_name for card in test_deck.get_cards()]) == set(
        VERBOSE_NAMES
    )


def test_completed_game_has_all_cards():

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


def test_all_players_have_two_hole_cards():

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
    game.advance_betting_round()  # New game to Preflop

    for player in game.get_players():
        assert len(player.get_hand().get_cards()) == 2
        assert len(set(player.get_hand()._get_cards_as_list())) == 2


def test_correct_number_of_players():
    game = SingleGame()
    player1 = Player(player_id=1, player_name="John", starting_stack=20)
    player2 = Player(player_id=2, player_name="Jane", starting_stack=20)
    game.register_players(player1, player2)
    assert len(game.get_players()) == 2


def test_correct_number_of_players_over_five():
    game = SingleGame()
    player1 = Player(player_id=1, player_name="John", starting_stack=20)
    player2 = Player(player_id=2, player_name="Jane", starting_stack=20)
    player3 = Player(player_id=3, player_name="Jim", starting_stack=20)
    player4 = Player(player_id=4, player_name="Jill", starting_stack=20)
    player5 = Player(player_id=5, player_name="Jack", starting_stack=20)
    player6 = Player(player_id=6, player_name="Jake", starting_stack=20)
    player7 = Player(player_id=7, player_name="Julia", starting_stack=20)
    player8 = Player(player_id=8, player_name="Ken", starting_stack=20)
    game.register_players(
        player1, player2, player3, player4, player5, player6, player7, player8
    )
    assert len(game.get_players()) == 8


def test_correct_number_of_players_when_any_player_has_zero_stack():
    game = SingleGame()
    player1 = Player(player_id=1, player_name="John", starting_stack=20)
    player2 = Player(player_id=2, player_name="Jane", starting_stack=20)
    player3 = Player(player_id=3, player_name="Jim", starting_stack=0)
    game.register_players(player1, player2, player3)
    game.advance_betting_round()
    assert len(game.get_players()) == 2


def test_correct_number_of_players_when_any_player_ids_collide():
    game = SingleGame()
    player1 = Player(player_id=1, player_name="John", starting_stack=20)
    player2 = Player(player_id=1, player_name="Jane", starting_stack=20)
    player3 = Player(player_id=2, player_name="Jim", starting_stack=20)
    game.register_players(player1, player2, player3)
    assert len(game.get_players()) == 2


def test_correct_number_of_active_players():
    game = SingleGame()
    player1 = Player(player_id=1, player_name="John", starting_stack=20)
    player2 = Player(player_id=2, player_name="Jane", starting_stack=20)
    player3 = Player(player_id=3, player_name="Jim", starting_stack=10)
    game.register_players(player1, player2, player3)
    game.advance_betting_round()
    assert len(game.get_players()) == 3


def test_reject_game_start_when_less_than_two_players_are_registered():
    game = SingleGame()
    player = Player(player_id=1, player_name="John", starting_stack=20)
    game.register_players(player)
    with pytest.raises(ValueError):
        game.advance_betting_round()


def test_betting_round_is_new_game():
    game = SingleGame()
    assert game.get_betting_round() == "notstarted"
