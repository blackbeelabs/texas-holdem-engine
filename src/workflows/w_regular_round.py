from engine.classes.Player import Player
from engine.classes.Deck import Deck
from engine.classes.SingleGame import SingleGame, PlayerAction

from engine.classes.Card import VALID_CARDS

from loguru import logger

if __name__ == "__main__":

    player1 = Player(player_id=6, player_name="John", starting_stack=100)
    player2 = Player(player_id=5, player_name="Jane", starting_stack=50)
    player3 = Player(player_id=4, player_name="Jim", starting_stack=100)
    player4 = Player(player_id=3, player_name="Jill", starting_stack=70)
    player5 = Player(player_id=2, player_name="Jack", starting_stack=20)
    game = SingleGame()
    # Register players
    game.register_players(player1, player2, player3, player4, player5)
    # Advance to preflop
    game.advance_betting_round()
    game.post_blinds()
    game.deal_hole_cards()
    # logger.info(f"(should throw no player found error)")
    # try:
    #     game.process_player_action(
    #         1, PlayerAction.CHECK
    #     )  # should throw no player found error
    # except ValueError as e:
    #     logger.error(e)
    # logger.info(f"(should throw out of turn error)")
    # try:
    #     game.process_player_action(
    #         10, PlayerAction.FOLD
    #     )  # should throw inactive player error
    # except ValueError as e:
    #     logger.error(e)
    # logger.info(f"(should throw cannot check error)")
    # try:
    #     game.process_player_action(
    #         14, PlayerAction.CHECK
    #     )  # should throw cannot check error
    # except ValueError as e:
    #     logger.error(e)
    try:
        game.process_player_action(4, PlayerAction.CALL)
        game.process_player_action(3, PlayerAction.CALL)
        game.process_player_action(2, PlayerAction.CALL)
    except ValueError as e:
        logger.error(e)
    try:
        game.advance_betting_round()  # should throw cannot advance round error
    except ValueError as e:
        logger.error(e)
    try:
        game.process_player_action(6, PlayerAction.CALL)
    except ValueError as e:
        logger.error(e)
    try:
        game.advance_betting_round()
    except ValueError as e:
        logger.error(e)

    # game.process_player_action(2, PlayerAction.CHECK)
    # game.process_player_action(3, PlayerAction.CHECK)
    # game.advance_betting_round()
    # game.deal_community_cards()

    # game.advance_betting_round()
    # game.deal_community_cards()

    # game.advance_betting_round()
    # game.deal_community_cards()

    # game.advance_betting_round()
    # game.deal_community_cards()

    # game.advance_betting_round()
    # game.deal_community_cards()
