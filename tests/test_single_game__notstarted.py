import pytest
from engine.classes.Player import Player
from engine.classes.Deck import Deck
from engine.classes.SingleGame import SingleGame, PlayerAction

from engine.classes.Card import VERBOSE_NAMES


@pytest.fixture
def notstarted_game():
    game = SingleGame(big_blind_bet=2)
    player1 = Player(player_id=1, player_name="John", starting_stack=5)
    player2 = Player(player_id=2, player_name="Jane", starting_stack=10)
    player3 = Player(player_id=3, player_name="Jim", starting_stack=20)
    game.register_players(player1, player2, player3)
    return game


"""
PART 1: Game, Round
"""


def test_notstarted_round_is_notstarted(notstarted_game):
    assert notstarted_game.get_betting_round() == "notstarted"


def test_reject_game_initialization_when_big_blind_is_not_even():
    with pytest.raises(ValueError):
        SingleGame(big_blind_bet=19)


def test_reject_game_initialization_when_big_blind_is_zero():
    with pytest.raises(ValueError):
        SingleGame(big_blind_bet=0)


def test_reject_game_initialization_when_big_blind_is_not_positive():
    with pytest.raises(ValueError):
        SingleGame(big_blind_bet=-1)


def test_allow_game_initialization_when_player_stack_is_less_than_big_blind(
    notstarted_game,
):
    player1 = Player(player_id=4, player_name="John", starting_stack=1)
    notstarted_game.register_players(player1)
    assert notstarted_game.count_players() == 4


"""
PART 2: Cards
"""


def test_notstarted_game_has_all_cards(notstarted_game):

    test_deck = Deck(new_deck=False)
    for card in notstarted_game.get_deck().get_cards():
        test_deck.add_card(card)
    assert test_deck.get_deck_size() == 52
    assert set([card.verbose_name for card in test_deck.get_cards()]) == set(
        VERBOSE_NAMES
    )
    assert notstarted_game.get_deck() == test_deck


def test_notstarted_game_has_shuffled_deck():
    """Test that two new games don't have identical card order"""
    game1 = SingleGame()
    game2 = SingleGame()
    assert game1.get_deck() != game2.get_deck()


def test_notstarted_game_has_no_community_cards():
    game = SingleGame()
    assert game.get_community_cards().get_deck_size() == 0


def test_notstarted_game_has_no_discarded_cards():
    game = SingleGame()
    assert game.get_discard_pile().get_deck_size() == 0


"""
PART 3: Players (all players, active players)
"""


def test_correct_number_of_players(notstarted_game):
    assert len(notstarted_game.get_players()) == 3


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
    game = SingleGame(big_blind_bet=2)
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


def test_correct_number_of_active_players(notstarted_game):

    notstarted_game.advance_betting_round()
    assert len(notstarted_game.get_active_players()) == 3


def test_reject_player_with_negative_starting_stack(notstarted_game):
    player = Player(player_id=4, player_name="John", starting_stack=-10)
    notstarted_game.register_players(player)
    assert notstarted_game.count_players() == 3


def test_reject_player_with_empty_name(notstarted_game):
    player = Player(player_id=4, player_name="", starting_stack=20)
    notstarted_game.register_players(player)
    assert notstarted_game.count_players() == 3


def test_reject_game_start_when_less_than_two_players_are_registered():
    game = SingleGame()
    player = Player(player_id=1, player_name="John", starting_stack=20)
    game.register_players(player)
    with pytest.raises(ValueError):
        game.advance_betting_round()


"""
PART 4: Pot, Bets
"""


def test_notstarted_game_has_pot_of_zero(notstarted_game):
    assert notstarted_game.get_pot() == 0


def test_notstarted_game_has_correct_blind_values():
    game = SingleGame(big_blind_bet=10)
    assert game.get_big_blind_bet() == 10
    assert game.get_small_blind_bet() == 5


def test_notstarted_game_has_no_players_bets(notstarted_game):
    assert notstarted_game.get_bets() == {}


def test_reject_odd_numbered_big_blind():
    with pytest.raises(ValueError):
        SingleGame(big_blind_bet=5)
