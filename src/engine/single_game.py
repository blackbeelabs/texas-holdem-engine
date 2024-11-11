from enum import Enum
from typing import List, Dict


class BettingRound(Enum):
    PREFLOP = "preflop"
    FLOP = "flop"
    TURN = "turn"
    RIVER = "river"


class SingleGame:
    def __init__(self, players: List[str], small_blind: int, big_blind: int):
        self.players = players
        self.small_blind = small_blind
        self.big_blind = big_blind
        self.pot = 0
        self.community_cards = []
        self.current_betting_round = BettingRound.PREFLOP
        self.player_hands: Dict[str, List[str]] = {}
        self.current_bets: Dict[str, int] = {player: 0 for player in players}
        self.active_players = players.copy()

    def deal_hole_cards(self, deck):
        """Deal two cards to each player"""
        for player in self.players:
            self.player_hands[player] = [deck.draw() for _ in range(2)]

    def post_blinds(self):
        """Post small and big blinds"""
        if len(self.players) < 2:
            raise ValueError("Not enough players to start a round")

        self.current_bets[self.players[0]] = self.small_blind
        self.current_bets[self.players[1]] = self.big_blind
        self.pot = self.small_blind + self.big_blind

    def deal_community_cards(self, deck):
        """Deal community cards based on current betting round"""
        if self.current_betting_round == BettingRound.FLOP:
            self.community_cards.extend([deck.draw() for _ in range(3)])
        elif self.current_betting_round in [BettingRound.TURN, BettingRound.RIVER]:
            self.community_cards.append(deck.draw())

    def process_action(self, player: str, action: str, amount: int = 0):
        """Process a player's action (fold, check, call, raise)"""
        if action == "fold":
            self.active_players.remove(player)
        elif action in ["call", "raise"]:
            self.current_bets[player] += amount
            self.pot += amount

    def advance_betting_round(self):
        """Advance to the next betting round"""
        if self.current_betting_round == BettingRound.PREFLOP:
            self.current_betting_round = BettingRound.FLOP
        elif self.current_betting_round == BettingRound.FLOP:
            self.current_betting_round = BettingRound.TURN
        elif self.current_betting_round == BettingRound.TURN:
            self.current_betting_round = BettingRound.RIVER

    def get_winners(self):
        """Determine the winner(s) of the round"""
        # This would implement poker hand evaluation logic
        # Returns list of winning players
        pass
