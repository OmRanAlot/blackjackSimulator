import blackjack2 as bj
import strategies as strats

players = [
    bj.Player("HiLo", strategy=strats.HiLoStrategy()),
    bj.Player("HiLo Martingale", strategy=strats.HiLoStrategyMartingale()),
    bj.Player("HiLo Paroli", strategy=strats.HiLoStrategyParoli()),
]


blackjack = bj.Game(number_of_players=len(players), decks=6, players=players)


for i in range(100000):
    blackjack.play()
    if i % 100 == 0:
        print(f"Completed {i} rounds...")

blackjack.save_stats_to_csv("blackjack_stats2.csv")

