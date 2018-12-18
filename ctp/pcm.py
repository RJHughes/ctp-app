from binance.client import Client
import numpy as np
import matplotlib.pyplot as plt

client = Client('1','1')

klines = client.get_historical_klines("BNBBTC", Client.KLINE_INTERVAL_1MINUTE, "1 day˓→ago UTC")

open_prices = [row[1] for row in klines]

plt.plot(open_prices[-10:])
plt.show()
