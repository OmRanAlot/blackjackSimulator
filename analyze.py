import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv("blackjack_stats.csv")

win_count = (df['won'] == 1).sum()

control = df[df['name'] == 'Control']
Conservative = df[df['name'] == 'Conservative']
Aggressive = df[df['name'] == 'Aggressive']
HiLo = df[df['name'] == 'HiLo']
HiLo_Agressive = df[df['name'] == 'HiLo Agressive']
Paroli = df[df['name'] == 'Paroli']
Martingale = df[df['name'] == 'Martingale']
Basic_Tables = df[df['name'] == 'Basic Tables']

plt.figure(figsize=(15, 5))
# plt.plot(control['round'], control['balance'])
# plt.plot(Conservative['round'], Conservative['balance'])
# plt.plot(Aggressive['round'], Aggressive['balance'])
# plt.plot(HiLo['round'], HiLo['balance'])
# plt.plot(HiLo_Agressive['round'], HiLo_Agressive['balance'])
plt.plot(Paroli['round'], Paroli['balance'])
plt.plot(Martingale['round'], Martingale['balance'])
# plt.plot(Basic_Tables['round'], Basic_Tables['balance'])

plt.xlabel("Rounds")
plt.ylabel("Balance")
plt.title("Control Player")

plt.legend(['Paroli', 'Martingale'])

plt.tight_layout()
plt.show()




'''

change number of decks
number of players



'''
