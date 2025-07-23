"""
Blackjack Strategy Implementations
---------------------------------
This module contains various blackjack playing strategies, including:
- Basic strategy
- Card counting systems (Hi-Lo)
- Betting strategies (Martingale, Paroli, etc.)
- Adaptive strategies that adjust based on game state

Reference: https://www.qfit.com/card-counting-systems.htm
"""
import math
from blackjack import Hand

class BaseStrategy:
    def __init__(self):
        pass
    """
    Base class for all blackjack strategies.
    Provides default implementations for all strategy decisions.
    Subclasses should override these methods to implement specific strategies.
    """
    def place_bet(self, player, true_count=0):
        return round(player.balance * 0.01, 2)
    
    def decide_split(self, hand, dealer_card, true_count):
        return hand.cards[0].split("_")[0] in ["Ace", "8"] and (hand.cards[0].split("_")[1] == hand.cards[0].split("_")[0])
            
    def decide_hit(self, hand, dealer_card, true_count):  
        return hand.get_score()<17

    def decide_double(self, hand, dealer_card, true_count):
        return hand.get_score() <12

    def play_turn(self, hand, dealer_card, true_count=0):
        if self.decide_split(hand, dealer_card, true_count):
            return "split"
        elif self.decide_double(hand, dealer_card, true_count):
            return "double"
        elif self.decide_hit(hand, dealer_card, true_count):
            return "hit"
        else:
            return "stand"


class MartingaleStrategy(BaseStrategy):
    """
    Martingale Betting Strategy
    --------------------------
    Doubles the bet after each loss, resets to base bet after a win.
    This is a progressive betting system where losses are recouped by doubling bets.
    Note: High risk of large losses during losing streaks.
    """
    def place_bet(self, player, true_count=None):
        if player.loss_streak == 0:
            return 10
        return min(player.bet * 2, player.balance)

class ParoliStarategy(BaseStrategy):
    """
    Paroli Betting Strategy
    ----------------------
    Also known as the Reverse Martingale. Doubles the bet after each win,
    resets to base bet after a loss. Aims to capitalize on winning streaks
    while limiting losses during losing streaks.
    """
    def place_bet(self, player, true_count=None):
        if player.win_streak == 0:
            return 10
        return min(player.bet * 2, player.balance)

class HiLoStrategy(BaseStrategy):
    """
    Hi-Lo Card Counting Strategy
    -----------------------------
    Uses a simple card counting system to adjust betting and playing decisions.
    The true count is calculated based on the number of high cards remaining in the deck.
    """
    def place_bet(self, player, true_count):
        if true_count >= 2:
            return round(player.balance * 0.05, 2)
        return round(player.balance * 0.01, 2)
    
    def decide_hit(self, hand, dealer_card, true_count):
        if true_count >= 2:
            return hand.get_score() < 16
        return hand.get_score() < 17