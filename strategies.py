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

class HiLo_bettingOnly(BaseStrategy):
    """
    Hi-Lo Betting Strategy
    ----------------------
    Uses a simple card counting system to adjust betting.
    The true count is calculated based on the number of high cards remaining in the deck.
    """
    def place_bet(self, player, true_count):
        if true_count >= 5:
            return round(player.balance * 0.1, 2)
        elif true_count >= 4:
            return round(player.balance * 0.05, 2)
        elif true_count >= 2:
            return round(player.balance * 0.025, 2)
        return round(player.balance * 0.01, 2)

    def decide_double(self, hand, dealer_card, true_count):
        return False

class HiLo_decisionOnly(BaseStrategy):
    """
    Hi-Lo Decision Strategy
    ----------------------
    Uses a simple card counting system to adjust playing decisions.
    The true count is calculated based on the number of high cards remaining in the deck.
    """
    def decide_double(self, hand, dealer_card, true_count):
        return False
    
    def decide_hit(self, hand, dealer_card, true_count):
        return hand.get_score() < 12 or true_count >= 2
    
    def decide_split(self, hand, dealer_card, true_count):
        return False

class HiLoStrategy(HiLo_bettingOnly, HiLo_decisionOnly):
    """
    Hi-Lo Card Counting Strategy
    -----------------------------
    Uses a simple card counting system to adjust betting and playing decisions.
    The true count is calculated based on the number of high cards remaining in the deck.
    """
    def place_bet(self, player, true_count):
        return HiLo_bettingOnly.place_bet(self, player, true_count)
    
    def decide_double(self, hand, dealer_card, true_count):
        return HiLo_decisionOnly.decide_double(self, hand, dealer_card, true_count)
    
    def decide_hit(self, hand, dealer_card, true_count):
        return HiLo_decisionOnly.decide_hit(self, hand, dealer_card, true_count)
    
    def decide_split(self, hand, dealer_card, true_count):
        return HiLo_decisionOnly.decide_split(self, hand, dealer_card, true_count)


class BasicStrategyCharts(HiLo_bettingOnly):
    """
    https://www.blackjackapprenticeship.com/blackjack-strategy-charts/
    Using charts based on the website ^
    """
    #Assuming Doubling After Split IS NOT Allowed
    #Using True Count betting Style
    def place_bet(self, player, true_count):
        return super().place_bet(player, true_count)
    
    def decide_double(self, card1, card2, is_Soft, dealer_card, hand_value):
        if is_Soft:
            if dealer_card in ["2", "3", "4", "5", "6"]:
                if dealer_card == "8" and hand_value == 19:
                    return True
                if hand_value == 18:
                    return True
                if hand_value ==  17 and dealer_card in ["3", "4", "5", "6"]:
                    return True
                if (hand_value == 16 or hand_value == 15) and dealer_card in ["4", "5", "6"]:
                    return True
                if (hand_value == 14 or hand_value == 13) and dealer_card in ["5", "6"]:
                    return True
            return False
        else:
            if hand_value == 11:
                return True
            if hand_value == 10 and dealer_card in ["2", "3", "4", "5", "6", "7", "8", "9"]:
                return True
            if hand_value==9 and dealer_card in ["3", "4", "5", "6"]:
                return True
            return False
                
      
    def decide_stand(self, card1, card2, is_Soft, dealer_card, hand_value):
        if is_Soft:
            if hand_value == 20:
                return True
            if hand_value == 19 and dealer_card != "6":
                return True
            if hand_value == 18 and dealer_card in [ "7", "8"]:
                return True
            return False
        else:
            if hand_value >= 17:
                return True
            if hand_value in [13,14,15,16] and dealer_card in ["2","3", "4", "5", "6"]:
                return True
            if hand_value in [12] and dealer_card in ["4", "5", "6"]:
                return True
            return False

    def decide_split(self, card1, card2, is_Soft, dealer_card, hand_value):
        if card1 != card2:
            return False
        if card1 in ["Ace", "8"]:
            return True
        if card1 in ["2", "3", "6","7", "9"]:
            if (card1 == "2" or card1=="3") and dealer_card in ["4", "5", "6", "7"]:
                return True
            if card1 in ["7", "6", "9"] and dealer_card in ["2", "3", "4", "5", "6"]:
                return False if card1 =="6" and dealer_card == "2" else True
            
            if card1 == "9" and dealer_card in ["8", "9"]:
                return True

            if card1 == dealer_card:
                return True
            
        return False

    def play_turn(self, hand, dealer_card, true_count=0):

        hand_value = hand.get_score()
        card1 = hand.cards[0].split("_")[1]
        card2 = hand.cards[1].split("_")[1]
        is_Soft = card1 == "Ace" or card2 == "Ace"
        dealer_card = dealer_card.split("_")[1]

        if self.decide_split(card1, card2, is_Soft, dealer_card, hand_value):
            return "split"
        elif self.decide_double(card1, card2, is_Soft, dealer_card, hand_value):
            return "double"
        elif self.decide_stand(card1, card2, is_Soft, dealer_card, hand_value):
            return "stand"
        else:
            return "hit"

    
        