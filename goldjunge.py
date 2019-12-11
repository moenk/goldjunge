#
#   file: goldjunge.py
#
#   coder: moenk
#
#   purpose: simple backtest with expert advisor for strategies like golden cross and death cross
#
#   using: stockstats for trading KPI
#

import pandas as pd
from pandas.plotting import register_matplotlib_converters
from stockstats import StockDataFrame
import matplotlib.pyplot as plt
register_matplotlib_converters()


# Expert Advisor: 1 = kaufen, 0 = halten, -1 = verkaufen
def expert_advisor(day):
    result=0
    if stocks['close_50_sma'][day] > stocks['close_200_sma'][day]:
        result = 1
    if stocks['close_50_sma'][day] < stocks['close_200_sma'][day]:
        result = -1
    return result

# Lade CSV von: https://www.ariva.de/goldpreis-gold-kurs/historische_kurse
df=pd.read_csv("wkn_965515_historic.csv",delimiter=";",thousands=".",decimal=",")
df.columns = ['date', 'open', 'high', 'low', 'close', 'volume', 'amount']

# Datum korrigieren als Index
df['date'] = pd.to_datetime(df['date'])
df=df.sort_values('date', ascending=True)
df.set_index('date', inplace=True)

# Umwandeln in StockDataFrame
stocks = StockDataFrame.retype(df)

# Plot Chart
plt.plot(stocks['close'])

# Backtest
investiert=False
saldo=0
for day in range(len(df)):
    # verkaufen?
    if investiert and (expert_advisor(day)<0):
        kurs = df['close'][day]
        print ("Verkauf:",kurs)
        plt.plot((df.index[day]),kurs,'ro')
        saldo = saldo + kurs
        investiert=False
    # kaufen?
    if not(investiert) and (expert_advisor(day)>0):
        kurs = df['close'][day]
        print ("Kauf:",kurs)
        plt.plot((df.index[day]),kurs,'go')
        saldo = saldo - kurs
        investiert=True
if investiert:
    kurs = df['close'][day]
    saldo = saldo + kurs
    print("Verkauf:", kurs)

# Ergebnis
print ("Saldo:",saldo)
plt.savefig("goldjunge.png")
plt.show()
