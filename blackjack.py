import random
import pandas as pd

class Hand:
    def __init__(self):
        self.cards = []
        self.bet = 0
        self.is_active = True
        self.doubled = False

    def add_card(self, card):
        self.cards.append(card)

    def can_split(self) -> bool:
        return len(self.cards) == 2 and (self.cards[0].split("_")[1] == self.cards[1].split("_")[1])

    def can_double(self) -> bool:
        return len(self.cards) == 2

    def is_blackjack(self) -> bool:
        return self.get_score() == 21 and len(self.cards) == 2

    def is_busted(self) -> bool:
        return self.get_score() > 21 
    
    def get_score(self):
        score = 0
        aces = 0
        
        for card in self.cards:
            rank = card.split('_')[1]
            if rank in ['Jack', 'Queen', 'King']:
                score += 10
            elif rank == 'Ace':
                score += 11
                aces += 1
            else:
                score += int(rank)
        
        # Adjust for aces if needed
        while score > 21 and aces > 0:
            score -= 10
            aces -= 1
            
        return score

    def get_bet(self):
        return self.bet

    def __str__(self):
        return f"Cards: {self.cards}, Score: {self.get_score()}, Bet: {self.bet}, Active?: {self.is_active}"

class Player:
    def __init__(self,  name, strategy=None, balance=1000):
        if name.lower() == "dealer":
            raise ValueError("This name is reserved")
        
        self.name = name
        self.balance = balance
        self.stats = {}
        self.strategy = strategy
        self.hands = [Hand()]

        self.win_streak = 0
        self.loss_streak = 0
        
    def reset_hands(self):
        self.hands = [Hand()]

    def can_split_hand(self, hand_index=0) -> bool:
        if hand_index >= len(self.hands):
            return False
        return self.hands[hand_index].can_split()

    def hit(self, card, hand_index=0):
        if hand_index >= len(self.hands) or not self.hands[hand_index].is_active:
            return False
        self.hands[hand_index].add_card(card)
        return True
    
    def split(self, hand_index=0):
        if not self.can_split_hand(hand_index):
            return False

        hand = self.hands[hand_index]

        if hand.bet > self.balance:
            return False

        # Create new hand with one of the cards
        new_hand = Hand()
        new_hand.add_card(hand.cards.pop())
        new_hand.bet = hand.bet
        
        # Insert new hand after current hand
        self.hands.insert(hand_index + 1, new_hand)

        self.balance -= hand.bet
        return True

    def stand(self, hand_index=0):
        if hand_index < len(self.hands):
            self.hands[hand_index].is_active = False

    def double_down(self, card, hand_index=0):
        if hand_index >= len(self.hands):
            return False
            
        hand = self.hands[hand_index]
        if not hand.can_double() or hand.bet > self.balance:
            return False

        self.balance -= hand.bet
        hand.bet *= 2
        hand.is_active = False
        hand.add_card(card)

        hand.doubled = True

        return True

    def place_bet(self, bet, hand_index=0):
        if bet > self.balance or hand_index >= len(self.hands):
            return False
        self.hands[hand_index].bet = bet
        
        self.balance -= bet
        return True
    
    def add_balance(self, amount):
        """Add balance to the player."""
        self.balance += amount

    def has_active_hands(self):
        """Check if the player has any active hands."""
        return any(hand.is_active for hand in self.hands)

    def __str__(self):
        return f"{self.name} - Balance: ${self.balance}"

class Game:
    def __init__(self, number_of_decks, players: list):
        self.deck = self.generate_deck(number_of_decks)
        self.players = players
        self.dealer_card = ""
        self.dealer = Player(name="Dealer_NPC", balance=1000000)
        self.running_count = 0
        self.total_cards = number_of_decks * 52
        self.cards_dealt = 0
        

        self.stats = []

        self.percent_needed_reshuffle = .25
    
    def generate_deck(self, number_of_decks):
        """Create a shuffled deck with the specified number of decks."""
        ranks = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'Jack', 'Queen', 'King', 'Ace']
        suits = ['Hearts', 'Diamonds', 'Clubs', 'Spades']
        deck = []
        for _ in range(number_of_decks):
            for suit in suits:
                for rank in ranks:
                    deck.append(f"{suit}_{rank}")
        random.shuffle(deck)
        return deck

    def deal_cards(self):
        """Deal initial cards to all players and dealer"""
   
        # Deal dealer's up card
        up_card = self.deck.pop()
        self.dealer_card = up_card
        self.update_count(up_card)
        self.dealer.hands[0].add_card(up_card)
        
        # Deal two cards to each player
        for player in self.players:
            card1 = self.deck.pop()
            card2 = self.deck.pop()

            self.update_count(card1)
            self.update_count(card2)

            player.hands[0].add_card(card1)
            player.hands[0].add_card(card2)
        
        # Deal dealer's hole card
        hole_card = self.deck.pop()
        self.update_count(hole_card)
        self.dealer.hands[0].add_card(hole_card)
    
    def place_bets(self):
        for player in self.players:
            player.place_bet(
                bet=player.strategy.place_bet(
                    player=player, 
                    true_count=self.get_true_count()
                ),
                hand_index=0
            )
    
    def update_count(self, card):
        rank = card.split('_')[1]
        if rank in ['2', '3', '4', '5', '6']:
            self.running_count += 1
        elif rank in ['10', 'Jack', 'Queen', 'King', 'Ace']:
            self.running_count -= 1
        self.cards_dealt += 1

    def get_true_count(self):
        """Calculate true count based on running count and remaining decks"""
        remaining_decks = (self.total_cards - self.cards_dealt) / 52
        if remaining_decks <= 0:
            return 0
        return self.running_count / remaining_decks

    def true_count(self):
        
        return self.get_true_count()

    def determine_winners(self):
        """Determine winners and pay out"""
        dealer_score = self.dealer.hands[0].get_score()
        dealer_busted = self.dealer.hands[0].is_busted()
        dealer_blackjack = self.dealer.hands[0].is_blackjack()
            
        results = {}
            
        for player in self.players:
            player_results = []
                
            for i, hand in enumerate(player.hands):
                
                hand_score = hand.get_score()
                hand_busted = hand.is_busted()
                hand_blackjack = hand.is_blackjack()
                
                
                if hand_busted:
                    result = "lose"
                    player.loss_streak += 1
                    player.win_streak = 0
                   
                elif dealer_busted and not hand_busted:
                    result = "win"
                    player.add_balance(hand.bet * 2)
                    player.loss_streak = 0
                    player.win_streak += 1
                elif hand_blackjack and not dealer_blackjack:
                    result = "win"
                    player.loss_streak = 0
                    player.win_streak += 1
                    player.add_balance(int(hand.bet * 2.5))
                elif hand_score > dealer_score:
                    result = "win"
                    player.loss_streak = 0
                    player.win_streak += 1
                    player.add_balance(hand.bet * 2)
                elif hand_score == dealer_score:
                    result = "push"  # Changed from "tie" to standard "push"
                    player.add_balance(hand.bet)
                else:
                    result = "lose"
                    player.loss_streak += 1
                    player.win_streak = 0
                    player.add_balance(0)
                

                player_results.append({
                    'hand': i,
                    'score': hand_score,
                    'bet': hand.bet,
                    'result': result,
                })                
                
            results[player.name] = player_results
            
        return results, dealer_score

    def needs_new_deck(self, percent):
        """Check if we need to reshuffle (less than 25% of cards remaining)"""
        return len(self.deck) < self.total_cards * percent

    def reshuffle(self):
        """Reshuffle the deck and reset count"""
        self.deck = self.generate_deck(self.total_cards // 52)
        self.running_count = 0
        self.cards_dealt = 0

    def play_round(self, round_num):
        """Play a complete round of blackjack"""
        if self.needs_new_deck(self.percent_needed_reshuffle):
            self.reshuffle()

        #clear any exisiting hands
        for player in self.players:
            # print(f"{player.balance}")
            player.reset_hands()
        self.dealer.reset_hands()

        # Place bets first
        self.place_bets()
        
        # Deal cards
        self.deal_cards()

       
        # Players play their hands
        for player in self.players:
            hand_index = 0
            while hand_index < len(player.hands):
                hand = player.hands[hand_index]
               
                while hand.is_active and not hand.is_busted():
                    
                    choice = player.strategy.play_turn(
                        hand=hand,
                        dealer_card=self.dealer_card,
                        true_count=self.get_true_count()
                        )
                    
                    if choice == "double":
                        card = self.deck.pop()
                        if player.double_down(card, hand_index):
                            self.update_count(card)
                        
                    elif choice == "split":
                        if player.split(hand_index):
                            # Give one card to each split hand
                            card1 = self.deck.pop()
                            player.hit(card1, hand_index)
                            self.update_count(card1)
                            
                            card2 = self.deck.pop()
                            player.hit(card2, hand_index + 1)
                            self.update_count(card2)
                        else:
                            # Can't split, treat as hit
                            card = self.deck.pop()
                            player.hit(card, hand_index)
                            self.update_count(card)
                    elif choice == "hit":
                        card = self.deck.pop()
                        player.hit(card, hand_index)
                        self.update_count(card)
                    else:  # stand
                        player.stand(hand_index)
                        
                    
                hand_index += 1

        # Dealer plays
        dealer_hand = self.dealer.hands[0]
        while dealer_hand.get_score() < 17:
            card = self.deck.pop()
            self.update_count(card)
            self.dealer.hit(card, 0)
                
        # Determine winners and pay out
        results, dealer_score = self.determine_winners()
        
        for player in self.players:
            

            for i, hand in enumerate(player.hands):
                # print((results[player.name][i]["result"]))
                # print(f"{player.name} - Balance: ${player.balance}")
                self.stats.append(
                    {"round": round_num,
                    "name": player.name,
                    "balance": player.balance,
                    "hand": hand.cards,
                    "score": hand.get_score(),
                    "betAmount": hand.bet,

                    "win": 1 if results[player.name][i]["result"]=="win" else 0,
                    "loss": 1 if results[player.name][i]["result"]=="lose" else 0,
                    "tie": 1 if results[player.name][i]["result"]=="push" else 0,
                    "double":1 if hand.doubled else 0,
                    "blackjack":1 if ((hand.get_score() == 21 and len(hand.cards)==2) and (dealer_score!=21)) else 0,
                    "bust":1 if (hand.get_score() > 21) else 0,

                    "dealer_bust": 1 if dealer_score >21 else 0,
                    "dealer_score":dealer_score,
                    "dealer_hand": dealer_hand.cards,

                    "decks": self.total_cards/52,
                    "running_count":self.running_count,
                    "true_count": round(self.get_true_count(),3)
                    }
                )

    def get_stats(self):
        return self.stats



if __name__ == "__main__":
    # Import your strategies here
    from strategies import BaseStrategy  
    
    # Create players with your strategies
    players = [
        Player(strategy=BaseStrategy(), name="Alice", balance=1000),
        Player(strategy=BaseStrategy(), name="Bob", balance=1000),
    ]
    
    # Create game with 6 decks
    game = Game(6, players)
    results = []
    # Play 5 rounds
    for round_num in range(1, 6):
        print(f"\n--- Round {round_num} ---")
        game.play_round(round_num)
        # print(game.get_stats())
        
    result = game.get_stats()
   
    df = pd.DataFrame(data=result)
    print(df)