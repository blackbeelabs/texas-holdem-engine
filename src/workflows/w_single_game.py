# import pytest
# from engine.single_game import SingleGame, PlayerAction, BettingRound
# from engine.player import Player


# class TestSingleGame:
#     @pytest.fixture
#     def basic_game(self):
#         """Basic game setup with 2 players"""
#         players = [
#             Player("Player 1", 1000),
#             Player("Player 2", 1000),
#         ]
#         return SingleGame(players=players)

#     @pytest.fixture
#     def full_game(self):
#         """Game setup with 6 players"""
#         players = [Player(f"Player {i}", 1000) for i in range(1, 7)]
#         return SingleGame(players=players)

#     # Simple Unit Tests
#     def test_game_initialization(self, basic_game):
#         """Test basic game initialization"""
#         assert len(basic_game.players) == 2
#         assert basic_game.small_blind_bet == 10
#         assert basic_game.big_blind_bet == 20
#         assert basic_game.current_betting_round == BettingRound.PREFLOP
#         assert len(basic_game.community_cards) == 0

#     def test_register_player(self):
#         """Test player registration"""
#         game = SingleGame()
#         player = Player("Test Player", 1000)
#         game.register_player(player)
#         assert len(game.players) == 1
#         assert game.players[0].name == "Test Player"

#     def test_post_blinds(self, basic_game):
#         """Test posting of blinds"""
#         basic_game.post_blinds()
#         assert len(basic_game.bets) == 2
#         assert basic_game.bets[0].amount == 10  # Small blind
#         assert basic_game.bets[1].amount == 20  # Big blind
#         assert basic_game.get_pot() == 30

#     def test_deal_hole_cards(self, basic_game):
#         """Test dealing hole cards"""
#         basic_game.deal_hole_cards()
#         for player in basic_game.players:
#             assert len(player.hand) == 2

#     # Error Cases
#     def test_post_blinds_with_insufficient_players(self):
#         """Test posting blinds with insufficient players"""
#         game = SingleGame([Player("Solo Player", 1000)])
#         with pytest.raises(ValueError):
#             game.post_blinds()

#     def test_invalid_betting_round_advance(self, basic_game):
#         """Test invalid betting round advancement"""
#         basic_game.current_betting_round = BettingRound.RIVER
#         with pytest.raises(ValueError):
#             basic_game.advance_betting_round()

#     # Complex Integration Tests
#     def test_full_preflop_round(self, basic_game):
#         """Test a complete preflop round"""
#         # Setup
#         basic_game.deal_hole_cards()
#         basic_game.post_blinds()

#         # Player actions
#         basic_game.process_player_action(
#             0, PlayerAction.CALL, 20
#         )  # Complete the small blind
#         basic_game.process_player_action(1, PlayerAction.CHECK)

#         assert basic_game.get_pot() == 40
#         assert basic_game.current_betting_round == BettingRound.PREFLOP

#     def test_full_betting_rounds_sequence(self, basic_game):
#         """Test advancing through all betting rounds"""
#         # Setup
#         basic_game.deal_hole_cards()
#         basic_game.post_blinds()

#         # Preflop
#         basic_game.process_player_action(0, PlayerAction.CALL, 20)
#         basic_game.process_player_action(1, PlayerAction.CHECK)
#         basic_game.advance_betting_round()

#         # Flop
#         basic_game.deal_community_cards()
#         assert len(basic_game.community_cards) == 3
#         basic_game.process_player_action(0, PlayerAction.CHECK)
#         basic_game.process_player_action(1, PlayerAction.CHECK)
#         basic_game.advance_betting_round()

#         # Turn
#         basic_game.deal_community_cards()
#         assert len(basic_game.community_cards) == 4
#         basic_game.process_player_action(0, PlayerAction.CHECK)
#         basic_game.process_player_action(1, PlayerAction.CHECK)
#         basic_game.advance_betting_round()

#         # River
#         basic_game.deal_community_cards()
#         assert len(basic_game.community_cards) == 5
#         basic_game.process_player_action(0, PlayerAction.CHECK)
#         basic_game.process_player_action(1, PlayerAction.CHECK)

#         assert basic_game.current_betting_round == BettingRound.RIVER

#     def test_complex_betting_scenario(self, full_game):
#         """Test a complex betting scenario with multiple raises"""
#         full_game.deal_hole_cards()
#         full_game.post_blinds()

#         # Preflop action with raises
#         actions = [
#             (2, PlayerAction.RAISE, 60),  # Raise to 60
#             (3, PlayerAction.CALL, 60),  # Call 60
#             (4, PlayerAction.RAISE, 120),  # Re-raise to 120
#             (5, PlayerAction.FOLD, 0),  # Fold
#             (0, PlayerAction.CALL, 120),  # Call 120
#             (1, PlayerAction.FOLD, 0),  # Fold
#             (2, PlayerAction.CALL, 60),  # Call additional 60
#             (3, PlayerAction.CALL, 60),  # Call additional 60
#         ]

#         for player_idx, action, amount in actions:
#             full_game.process_player_action(player_idx, action, amount)

#         # Verify pot size and active players
#         expected_pot = 540  # Calculate total based on all actions
#         assert full_game.get_pot() == expected_pot
#         active_players = [p for p in full_game.players if p.is_active]
#         assert len(active_players) == 4

#     @pytest.mark.skip(reason="Implement once WinningHandSelector is complete")
#     def test_hand_resolution(self, basic_game):
#         """Test complete hand resolution with predetermined cards"""
#         # This test would need to mock the deck to deal specific cards
#         # and verify the correct winner is selected
#         pass
