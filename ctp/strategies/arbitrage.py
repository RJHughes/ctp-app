from .. strategies.strategy import Strategy
from .. exchanges.binance.binance_bt import Binance
from .. exchanges.poloniex import Poloniex
import pandas as pd
import operator


class Arbitrage(Strategy):
    """Implements an arbitrage trading strategy"""
    def __init__(self, id_value, base_ccy, backtest=False):
        Strategy.__init__(self, id_value, base_ccy)

        # percentage change permissable for triggering orders
        self.buy_threshold = 0.4

        # Set up Binance exchange
        binance_key = 'add-key'
        binance_secret = 'add-secret-key'
        self.binance = Binance(binance_key, binance_secret, backtest)

        # Set up Poloniex exchange
        poloniex_key = 'add-key'
        poloniex_secret = 'add-secret-key'
        self.poloniex = Poloniex(poloniex_key, poloniex_secret)

    def run(self):
        arbitrage_dict = {}

        binance_prices, polo_prices = self.get_current_prices()

        #print(binance_prices)
        #binance_prices = pd.DataFrame(binance_prices)
        #polo_prices = pd.DataFrame(polo_prices)

        #Get the common pairs between the exchanges
        for pairs in binance_prices:
            if polo_prices.get(pairs) != None:
                arbitrage_dict[pairs] = [binance_prices[pairs], polo_prices[pairs]]

        # Get the percentage change of prices
        for pairs in arbitrage_dict:
            arbitrage_dict[pairs] = (
            (float(arbitrage_dict[pairs][0])-float(arbitrage_dict[pairs][1]))/float(arbitrage_dict[pairs][0])*100)

        # Sort the prices in ascending order
        sorted_dict = dict(sorted(arbitrage_dict.items(),key=operator.itemgetter(1)))

        # Arrange buys and sells
        for pairs in sorted_dict:
            # Trigger if the difference is above the buy threshold
            if abs(sorted_dict[pairs]) > self.buy_threshold:
                if sorted_dict[pairs] > 0:
                    Strategy.trader.buy(1,pairs,self.poloniex)
                    Strategy.trader.sell(1,pairs,self.binance)
                if sorted_dict[pairs] < 0:
                    Strategy.trader.buy(1,pairs,self.binance)
                    Strategy.trader.sell(1,pairs,self.poloniex)

        #balance funds between exchanges

    def get_current_prices(self):
        """
        Returns the current live prices of all tickers from the exchanges
        """
        binance_prices = self.binance.get_current_prices()
        polo_prices = self.poloniex.get_current_prices()

        return binance_prices, polo_prices

    def find_common_pairs(self,prices):
        pass
