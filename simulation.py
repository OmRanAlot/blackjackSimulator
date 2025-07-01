import blackjack2 as bj
import strategies as strats

players = [
    bj.Player("HiLo", strategy=strats.HiLoStrategy()),
    bj.Player("Basic Tables", strategy=strats.BasicStrategyTables()),
    bj.Player("HiLo Agressive", strategy=strats.HiLoStarategyAgressive()),
    bj.Player("Paroli", strategy=strats.ParoliStarategy()),
    bj.Player("Martingale", strategy=strats.MartingaleStrategy()),
    bj.Player("Aggressive", strategy=strats.AlwaysHitUnderX(19)),
    bj.Player("Conservative", strategy=strats.AlwaysHitUnderX(10)),
    bj.Player("Control", strategy=strats.BaseStrategy()),
]


blackjack = bj.Game(number_of_players=len(players), decks=6, players=players)


for i in range(100000):
    blackjack.play()
    if i % 100 == 0:
        print(f"Completed {i} rounds...")

blackjack.save_stats_to_csv("blackjack_stats.csv")

