import pytest
from engine.classes.Player import Player
from engine.classes.Deck import Deck
from engine.classes.SingleGame import SingleGame, PlayerAction

from engine.classes.Card import VERBOSE_NAMES
from loguru import logger


@pytest.fixture
def river_game():
    game = SingleGame(big_blind_bet=2)
    player1 = Player(player_id=1, player_name="John", starting_stack=10)
    player2 = Player(player_id=2, player_name="Jane", starting_stack=10)
    player3 = Player(player_id=3, player_name="Jim", starting_stack=20)
    game.register_players(player1, player2, player3)
    game.advance_betting_round()  # notstarted to preflop
    game.advance_betting_round()  # preflop to flop
    game.advance_betting_round()  # flop to turn
    game.advance_betting_round()  # turn to river
    return game


"""
PART 1: Game, Round
"""


def test_river_betting_round_is_river(river_game):
    assert river_game.get_betting_round() == "river"


"""
PART 2: Cards
"""


"""
PART 3: Players (all players, active players)
"""


"""
PART 4: Pot, Bets
"""
