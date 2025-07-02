import random
import pandas as pd
face = ["King", "Queen", "Jack"]


class Player:
    def __init__(self, name, strategy=None, balance=1000):
        self.strategy = strategy
        self.balance = balance
        self.name = name

        self.hands = [[]]
        self.wants_to_hit = [True]
        self.has_blackjack = [False]
        self.bet = 0
        self.loss_streak = 0
        self.win_streak = 0

        self.das_allowed = False

    def get_score(self, hand_index=0):
        if hand_index >= len(self.hands):
            return 0
        
        values = []
        for card in self.hands[hand_index]:
            rank = card.split("_")[1]
            if rank in ["Jack", "Queen", "King"]:
                values.append(10)
            elif rank == "Ace":
                values.append(11)
            else:
                values.append(int(rank))
        total = sum(values)
        # Adjust for Aces
        while total > 21 and 11 in values:
            values[values.index(11)] = 1
            total = sum(values)
        return total

    def add_card(self, card, hand_index=0):
        if hand_index >= len(self.hands):
            return 
        self.hands[hand_index].append(card)

    def reset_hands(self):
        self.hands = [[]]
        self.wants_to_hit = [True]
        self.has_blackjack = [False]
        self.bet = 0

    def stand(self, hand_index=0):
        if hand_index >= len(self.wants_to_hit):
            return 
        self.wants_to_hit[hand_index] = False

    

class Game:
    def __init__(self, number_of_players, decks=6, players=None, double_after_split=True):
        self.number_of_decks = decks
        self.deck = self.generate_decks(decks)
        self.reshuffle_threshold = 52*2  # Reshuffle when fewer than 1 deck remains
        self.dealer = Player(name="Dealer")
        self.players = players if players is not None else [Player(f"Player {i+1}") for i in range(number_of_players)]
        self.number_of_players = len(self.players)
        self.running_count = 0
        self.stats = []
        self.round_number = 0
        self.double_after_split = double_after_split
        
        for player in self.players:
            player.bets = [0]  # Initialize bets list
            if double_after_split:
                player.das_allowed = True
    
    def generate_decks(self, number_of_decks):
        deck = [
            f"{suit}_{rank}" for suit in ["Spade", "Heart", "Diamond", "Club"]
            for rank in ["Ace", "2", "3", "4", "5", "6", "7", "8", "9", "10", "Jack", "Queen", "King"]
        ] * number_of_decks

        random.shuffle(deck)
        return deck

    def deal_cards(self):
        self.dealer.add_card(self.deck.pop()) #Hole card

        for player in self.players:
            card1 = self.deck.pop()
            card2 = self.deck.pop()
            self.update_running_count(card1)
            self.update_running_count(card2)
            player.add_card(card1)
            player.add_card(card2)

        dealerCard = self.deck.pop()
        self.dealer.add_card(dealerCard)
        self.update_running_count(dealerCard)

    def update_running_count(self, card):
        if card.split("_")[1] in ["2", "3", "4", "5", "6"]:
            self.running_count += 1
        elif card.split("_")[1] in ["10", "Jack", "Queen", "King", "Ace"]:
            self.running_count -= 1

    def reset_game(self):
        self.dealer.reset_hands()
        for player in self.players:
            player.reset_hands()
        self.running_count = 0
        self.deck = self.generate_decks(1)

    def record_stats(self):
        """Record statistics for all players after a game round"""
        self.round_number += 1
        dealer_score = self.dealer.get_score()
        dealer_bust = dealer_score > 21
        
        for player in self.players:
            for hand_index in range(len(player.hands)):
                if hand_index >= len(player.bets):  # Ensure we have a bet for this hand
                    player.bets.append(player.bet)  # Default to player's base bet if no specific bet for this hand
                player_score = player.get_score(hand_index)
                player_bust = player_score > 21
                
                # Check for blackjack (natural 21 with first two cards)
                is_blackjack = (player_score == 21 and len(player.hands[hand_index]) == 2)
                
                # Determine outcome and update balance
                if player_bust:
                    # Player busts, always lose
                    bet_lost = player.bets[hand_index] if hand_index < len(player.bets) else 0
                    player.balance -= bet_lost
                    won, lost, tied = 0, 1, 0
                    player.loss_streak += 1
                    player.win_streak = 0
                elif is_blackjack and not (dealer_score == 21 and len(self.dealer.hands[0]) == 2):
                    # Player has blackjack and dealer doesn't - 3:2 payout
                    bet_won = int(player.bets[hand_index] * 1.5) if hand_index < len(player.bets) else 0
                    player.balance += bet_won
                    won, lost, tied = 1, 0, 0
                    player.win_streak += 1
                    player.loss_streak = 0
                elif player_score == dealer_score:
                    # Push - return bet
                    won, lost, tied = 0, 0, 1
                    # No change to balance or streaks on tie
                elif dealer_bust or (player_score > dealer_score):
                    # Player wins
                    bet_won = player.bets[hand_index] if hand_index < len(player.bets) else 0
                    player.balance += bet_won
                    won, lost, tied = 1, 0, 0
                    player.win_streak += 1
                    player.loss_streak = 0
                else:
                    # Player loses
                    bet_lost = player.bets[hand_index] if hand_index < len(player.bets) else 0
                    player.balance -= bet_lost
                    won, lost, tied = 0, 1, 0
                    player.loss_streak += 1
                    player.win_streak = 0
                
                # Record stats
                self.stats.append({
                    'round': self.round_number,
                    'name': player.name,
                    'balance': player.balance,
                    'won': won,
                    'lost': lost,
                    'tied': tied,
                    'split': 1 if len(player.hands) > 1 else 0,
                    'doubled_down':  1 if player.bets[hand_index] == 2 * (player.bet if len(player.hands) == 1 else player.bets[hand_index]) else 0,
                    'bet': player.bets[hand_index] if hand_index < len(player.bets) else player.bet,
                    'player_score': player_score,
                    'dealer_score': dealer_score,
                    'dealer_bust': 1 if dealer_bust else 0,
                    'player_bust': 1 if player_bust else 0,
                    'blackjack': 1 if player_score == 21 and len(player.hands[hand_index]) == 2 else 0
                })
    
    def get_stats_dataframe(self):
        """Return the collected statistics as a pandas DataFrame"""
        return pd.DataFrame(self.stats)
    
    def save_stats_to_csv(self, filename='blackjack_stats.csv'):
        """Save the collected statistics to a CSV file"""
        if not self.stats:
            print("No statistics to save.")
            return
        df = self.get_stats_dataframe()
        df.to_csv(filename, index=False)
        print(f"Statistics saved to {filename}")
        return df

    def split_hand(self, player, hand_index=0):
        """Split player's hand into two hands"""
        # Create new hand with second card
        new_hand = [player.hands[hand_index].pop()]
        player.hands.append(new_hand)
        
        # Double the bet for the new hand
        player.bets.append(player.bets[hand_index])
        
        # Add new card to each hand
        player.add_card(self.deck.pop(), hand_index)
        player.add_card(self.deck.pop(), hand_index + 1)
        
        # Update hitting status for both hands
        player.wants_to_hit = [True, True]

    def can_split(self, player, hand_index=0):
        if len(player.hands[hand_index]) != 2:
            return False
        
        # Get ranks of both cards
        rank1 = player.hands[hand_index][0].split("_")[1]
        rank2 = player.hands[hand_index][1].split("_")[1]
        
        # Check if ranks are the same (including treating 10 and face cards as equal)
        if rank1 in ["10", "Jack", "Queen", "King"] and rank2 in ["10", "Jack", "Queen", "King"]:
            return True
        return rank1 == rank2

    def add_card_to_player(self, player, card, hand_index=0):
        player.add_card(card, hand_index)
        self.update_running_count(card)

    def can_double_down(self, player, hand_index=0):
        if hand_index > 0 and not self.double_after_split:
            return False
        return len(player.hands[hand_index]) == 2 and player.balance >= player.bets[hand_index]

    def check_reshuffle(self):
        """Reshuffle if fewer cards than threshold remain"""
        if len(self.deck) < self.reshuffle_threshold:
            self.deck = self.generate_decks(self.number_of_decks)
            self.running_count = 0

    def play(self):
        # Check if we need to reshuffle before starting a new round
        self.check_reshuffle()
        
        self.deal_cards()

        # players place a bet
        for player in self.players:
            bet_amount = player.strategy.place_bet(player=player, true_count=self.running_count)
            player.bet = bet_amount
            player.bets = [bet_amount]  # Initialize bets list with the initial bet

        #players play their turn
        for player in self.players:
            for hand_index in range(len(player.hands)):
                while player.get_score(hand_index=hand_index) <= 21 and player.wants_to_hit[hand_index]:
                    
                    choice = player.strategy.play_turn(player=player, dealer_card=self.dealer.hands[0], true_count=self.running_count, hand_index=hand_index)

                    ''' options are hit, stand, double down, split '''

                    if choice == "hit":
                        self.add_card_to_player(player, self.deck.pop(), hand_index)
                    elif choice == "stand":
                        player.stand(hand_index)
                    elif choice == "double down":
                        # Double the bet for this hand and deduct from balance
                        if hand_index < len(player.bets):
                            player.balance -= player.bets[hand_index]  # Deduct the additional bet
                            player.bets[hand_index] *= 2  # Double the bet for this hand
                        else:
                            player.balance -= player.bet  # Fallback to base bet
                            player.bets.append(player.bet * 2)  # Add new bet amount
                        self.add_card_to_player(player, self.deck.pop(), hand_index)
                        player.stand(hand_index)
                    elif choice == "split":
                        self.split_hand(player, hand_index)

        #dealer plays their turn
        while self.dealer.get_score() < 17:
            self.add_card_to_player(self.dealer, self.deck.pop())

        # Record stats for this round
        self.record_stats()
        
        # Reset hands for next round
        self.reset_game()

        








