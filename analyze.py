import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv("blackjack_stats2.csv")

win_count = (df['won'] == 1).sum()

hilo = df[df['name'] == 'HiLo']
hilo_martingale = df[df['name'] == 'HiLo Martingale']
hilo_paroli = df[df['name'] == 'HiLo Paroli']

plt.figure(figsize=(15, 5))

plt.plot(hilo_martingale['round'], hilo_martingale['bet'])
plt.plot(hilo_martingale['round'], hilo_martingale['balance'])

plt.plot(hilo_paroli['round'], hilo_paroli['balance'])
plt.plot(hilo_paroli['round'], hilo_paroli['bet'])


plt.xlabel("Rounds")
plt.ylabel("Balance")
plt.title("Balance Over Time")

plt.legend(['HiLo martingale bets','HiLo Martingale', 'HiLo Paroli', "hilo paroli bet"])

plt.tight_layout()
plt.show()




'''

change number of decks
number of players

GOAL:PULL A Profit

'''
