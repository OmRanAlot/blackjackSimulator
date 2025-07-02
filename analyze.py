import pandas as pd
import matplotlib.pyplot as plt


#100 rounds to 10000 rounds
df = pd.read_csv("scatter_data.csv")

plt.scatter(df['rounds'], df['final_balance'])
plt.axhline(y=1000, color='r', linestyle='-')
plt.xlabel("Rounds")
plt.ylabel("Final Balance")
plt.title("Final Balance vs Rounds")
plt.show()




# df = pd.read_csv("blackjack_stats4.csv")

# win_count = (df['won'] == 1).sum()

# adt1 = df[df['name'] == 'Adaptive Betting1']
# adt2 = df[df['name'] == 'Adaptive Betting2']
# adt3 = df[df['name'] == 'Adaptive Betting3']
# adt4 = df[df['name'] == 'Adaptive Betting4']
# adt5 = df[df['name'] == 'Adaptive Betting5']
# adt6 = df[df['name'] == 'Adaptive Betting6']
# adt7 = df[df['name'] == 'Adaptive Betting7']
# adt8 = df[df['name'] == 'Adaptive Betting8']
# adt9 = df[df['name'] == 'Adaptive Betting9']
# adt10 = df[df['name'] == 'Adaptive Betting10']

# plt.figure(figsize=(15, 5))

# plt.plot(adt1['round'], adt1['balance'])
# plt.plot(adt2['round'], adt2['balance'])
# plt.plot(adt3['round'], adt3['balance'])
# plt.plot(adt4['round'], adt4['balance'])
# plt.plot(adt5['round'], adt5['balance'])
# plt.plot(adt6['round'], adt6['balance'])
# plt.plot(adt7['round'], adt7['balance'])
# plt.plot(adt8['round'], adt8['balance'])
# plt.plot(adt9['round'], adt9['balance'])
# plt.plot(adt10['round'], adt10['balance'])

# plt.xlabel("Rounds")
# plt.ylabel("Balance")
# plt.title("Balance Over Time")

# plt.legend(['1', '2', '3', '4', '5', '6', '7', '8', '9', '10'])

# plt.tight_layout()
# plt.show()




'''

change number of decks
number of players

GOAL:PULL A Profit

'''
