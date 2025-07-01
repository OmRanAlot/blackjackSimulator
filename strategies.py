import math
#Strategies
#https://www.qfit.com/card_counting_systems.htm

class BaseStrategy:
    def place_bet(self, player, true_count):
        return 10  # default flat bet

    def decide_hit(self, player, dealer_card, hand_index=0, true_count=None):
        return player.get_score(hand_index) < 17  # default: hit under 17

    def decide_split(self, player, dealer_card, hand_index=0): #Always Split on double aces
        if len(player.hands) <= hand_index or len(player.hands[hand_index]) != 2:
            return False
        return player.get_score(hand_index) == 12

    def decide_double_down(self, player, dealer_card, hand_index=0):
        return False

    def play_turn(self, player, dealer_card, true_count=0, hand_index=0):
        if self.decide_split(player, dealer_card, hand_index):
            return "split"
        if self.decide_hit(player, dealer_card, hand_index, true_count):
            return "hit"
        if self.decide_double_down(player, dealer_card, hand_index):
            return "double down"
        return "stand"

class HiLoStrategy(BaseStrategy): #Linear - Basic Card Counting
    def place_bet(self, player, true_count):
        bet = 10 + (true_count - 2) * 5 
        return 0 if bet < 0 else bet

    def decide_hit(self, player, dealer_card, true_count, hand_index=0):
        return true_count > 2
    
    def play_turn(self, player, dealer_card, true_count=0, hand_index=0):
        if self.decide_split(player, dealer_card, hand_index):
            return "split"
        if self.decide_hit(player, dealer_card, true_count, hand_index):
            return "hit"
        return "stand"

class HiLoStarategyAdvanced(HiLoStrategy): #Controlled Betting
    def place_bet(self, player, true_count):
        max_bet = 200
        bet = 10 + (true_count - 2) * 5 
        return min(min(player.balance*0.05,bet), max_bet)
    
    def decide_hit(self, player, dealer_card, true_count, hand_index=0):
        return true_count > 2

class HiLoStarategyAgressive(HiLoStrategy): #Exponential Betting
    def place_bet(self, player, true_count):
        bet = 10 * 2** (true_count - 2)
        return 0 if bet < 0 else bet

class MartingaleStrategy(BaseStrategy): #Martingale Betting
    def place_bet(self, player, true_count=None):
        if player.loss_streak == 0:
            return 10
        return min(player.bet * 2, player.balance)

class ParoliStarategy(BaseStrategy): #Paroli
    def place_bet(self, player, true_count=None):
        if player.win_streak == 0:
            return 10
        return min(player.bet * 2, player.balance)

class AlwaysHitUnderX(BaseStrategy):
    def __init__(self, x):
        self.x = x              
    def decide_hit(self, player, dealer_card, true_count, hand_index=0):
        return player.get_score() < self.x

class AlwaysSplit(BaseStrategy):
    def decide_split(self, player, dealer_card, true_count, hand_index=0):
        return True

class BasicStrategyTables(BaseStrategy):
    def _get_card_rank(self, card):
        return card.split("_")[1]
    
    def _get_card_value(self, card):
        rank = self._get_card_rank(card)
        if rank in ["Jack", "Queen", "King"]:
            return 10
        elif rank == "Ace":
            return 11
        return int(rank)
    
    def _is_soft_hand(self, hand):
        has_ace = any(self._get_card_rank(card) == "Ace" for card in hand)
        values = [self._get_card_value(card) for card in hand]
        total = sum(values)
        
        # Adjust for Aces if needed
        while total > 21 and 11 in values:
            values[values.index(11)] = 1
            total = sum(values)
            
        return has_ace and total <= 21 and 11 in values
    
    def _get_hand_value(self, hand):
        values = [self._get_card_value(card) for card in hand]
        total = sum(values)
        
        # Adjust for Aces if needed
        while total > 21 and 11 in values:
            values[values.index(11)] = 1
            total = sum(values)
            
        return total

    def decide_split(self, player, dealer_card, hand_index=0, true_count=0):
        if len(player.hands[hand_index]) != 2:
            return False
            
        card1 = self._get_card_rank(player.hands[hand_index][0])
        card2 = self._get_card_rank(player.hands[hand_index][1])
        
        # If cards don't have same rank, can't split
        if card1 != card2 and not (card1 in ["10", "Jack", "Queen", "King"] and 
                                  card2 in ["10", "Jack", "Queen", "King"]):
            return False
            
        dealer_rank = self._get_card_rank(dealer_card[0])
        
        # Always split Aces and 8s
        if card1 in ["Ace", "8"]:
            return True
        
        # Never split 5s or tens (10, J, Q, K)
        if card1 in ["10", "Jack", "Queen", "King", "5"]:
            return False
        
        # Handle 9s
        if card1 == "9":
            if dealer_rank in ["7", "10", "Ace"]:
                return False
            return True  # split for dealer 2-6, 8, 9
        
        # Handle 7s
        if card1 == "7":
            return dealer_rank in ["2", "3", "4", "5", "6", "7"]
        
        # Handle 6s
        if card1 == "6":
            if dealer_rank == "2":
                return player.das_allowed  # Y/N on dealer 2
            return dealer_rank in ["3", "4", "5", "6"]
        
        # Handle 4s
        if card1 == "4":
            return dealer_rank in ["5", "6"] and player.das_allowed
        
        # Handle 3s and 2s (same logic)
        if card1 in ["2", "3"]:
            if dealer_rank in ["2", "3"]:
                return player.das_allowed
            return dealer_rank in ["4", "5", "6"]
        
        return False
    
    def decide_double_down(self, player, dealer_card, hand_index=0, true_count=0):
        # Check if hand exists and has exactly 2 cards (can only double on first two cards)
        if hand_index >= len(player.hands) or len(player.hands[hand_index]) != 2:
            return False
            
        hand = player.hands[hand_index]
        dealer_rank = self._get_card_rank(dealer_card[0] if isinstance(dealer_card, list) else dealer_card)
        is_soft = self._is_soft_hand(hand)
        total = self._get_hand_value(hand)
        
        if is_soft:
            # Soft hands (Ace counted as 11)
            if total == 20:  # A,9
                return dealer_rank in ["5", "6"]
            elif total in [15, 16]:
                return dealer_rank in ["4", "5", "6"]
            elif total == 17:
                return dealer_rank in ["3", "4", "5", "6"]
            elif total == 18:
                return dealer_rank in ["3", "4", "5", "6"]
            elif total == 19:
                return dealer_rank == "6"
            else:
                return False
        else:
            if total == 9:
                return dealer_rank in ["3", "4", "5", "6"]
            elif total == 10:
                return dealer_rank in ["2", "3", "4", "5", "6", "7", "8", "9"]
            elif total == 11:
                return dealer_rank != "A"
            else:
                return False

    def decide_hit(self, player, dealer_card, hand_index=0, true_count=0):
        hand = player.hands[hand_index]
        dealer_rank = self._get_card_rank(dealer_card[0]) if dealer_card else '2'  # Default to '2' if no dealer card
        is_soft = self._is_soft_hand(hand)
        total = self._get_hand_value(hand)
        
        # Get dealer's upcard value (A=11, face=10)
        if dealer_rank in ["10", "Jack", "Queen", "King"]:
            dealer_value = 10
        elif dealer_rank == "Ace":
            dealer_value = 11
        else:
            dealer_value = int(dealer_rank)

        # Basic strategy for hitting/standing
        if is_soft:
            # Soft hands (Ace counted as 11)
            if total >= 19:
                return False  # Stand on A,8 or better
            elif total == 18:
                # Stand on A,7 against 2-8, hit against 9,10,A
                return dealer_value in [9, 10, 11]
            else:
                return True  # Always hit soft 17 or less
        else:
            # Hard hands
            if total >= 17:
                return False  # Always stand on 17 or higher
            elif total >= 13:
                # Stand on 13-16 against 2-6, hit against 7+
                return dealer_value >= 7
            elif total == 12:
                # Hit 12 against 2,3,7+
                # Stand on 12 against 4,5,6
                return dealer_value in [2, 3, 7, 8, 9, 10, 11]
            else:
                # Always hit 11 or less
                return True

        return False

    def decide_stand(self, player, dealer_card, true_count, hand_index=0):
        return not self.decide_hit(player, dealer_card, true_count, hand_index)

    def decide_double_or_hit(self, player, dealer_card, true_count, hand_index=0):
        """Use if game rules require trying double and fallback to hit"""
        return self.decide_double_down(player, dealer_card, true_count, hand_index) or self.decide_hit(player, dealer_card, true_count, hand_index)

    def decide_double_or_stand(self, player, dealer_card, true_count, hand_index=0):
        """Use if game rules require trying double and fallback to stand"""
        return self.decide_double_down(player, dealer_card, true_count, hand_index) or not self.decide_hit(player, dealer_card, true_count, hand_index)

    def play_turn(self, player, dealer_card, true_count=0, hand_index=0):
        # Safety check for hand index
        if hand_index >= len(player.hands) or not player.hands[hand_index]:
            return "stand"  # Default to stand if hand doesn't exist or is empty
            
        # Check if player wants to hit for this hand
        if hand_index >= len(player.wants_to_hit) or not player.wants_to_hit[hand_index]:
            return "stand"
            
        # Make decisions in order of priority
        if self.decide_split(player, dealer_card, hand_index, true_count):
            return "split"
        if self.decide_double_down(player, dealer_card, hand_index, true_count):
            return "double down"
        if self.decide_hit(player, dealer_card, hand_index, true_count):
            return "hit"
        return "stand"

    def place_bet(self, player, true_count):
        return 10
        