import blackjack2 as bj
import strategies as strats
import pandas as pd

all_results = []



rounds_per_game_count = 100 #Number of games per round count
round_counts = range(100, 10001, 100) #Round counts

for rounds in round_counts:
    for game_num in range(rounds_per_game_count):
        players = [
            bj.Player("Adaptive Betting1", strategy=strats.AdaptativeBetting()),
            # bj.Player("Adaptive Betting2", strategy=strats.AdaptativeBetting()),
            # bj.Player("Adaptive Betting3", strategy=strats.AdaptativeBetting()),
            # bj.Player("Adaptive Betting4", strategy=strats.AdaptativeBetting()),
            # bj.Player("Adaptive Betting5", strategy=strats.AdaptativeBetting()),
            # bj.Player("Adaptive Betting6", strategy=strats.AdaptativeBetting()),
            # bj.Player("Adaptive Betting7", strategy=strats.AdaptativeBetting()),
            # bj.Player("Adaptive Betting8", strategy=strats.AdaptativeBetting()),
            # bj.Player("Adaptive Betting9", strategy=strats.AdaptativeBetting()),
            # bj.Player("Adaptive Betting10", strategy=strats.AdaptativeBetting()),
        ]

        blackjack = bj.Game(number_of_players=len(players), decks=6, players=players)
        for _ in range(rounds):
            blackjack.play()
        
        final_balance = players[0].balance
        all_results.append({"rounds": rounds, "final_balance": final_balance, "game number": game_num})

        if (game_num+1) % 100 == 0:
            print(f"Completed {game_num} games...")

    print(f"Completed {rounds_per_game_count} games of {rounds} rounds")

all_results_df = pd.DataFrame(all_results)
all_results_df.to_csv("scatter_data.csv", index=False)



#regular simulation

# for i in range(1000):
#     blackjack.play()
#     if i % 100 == 0:
#         print(f"Completed {i} rounds...")

# blackjack.save_stats_to_csv("blackjack_stats4.csv")

