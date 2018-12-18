from exchanges.exchange import Exchange
from binance.client import Client
from poloniex import Poloniex as PoloniexAPI
from utilities import create_user_symbol

class Poloniex(Exchange):
    """Class that models the Poloniex exchange"""

    def __init__(self, api_key, api_secret):
        Exchange.__init__(self, api_key, api_secret)
        self.client = PoloniexAPI(api_key,api_secret)
        self.name = "Poloniex"

    @staticmethod
    def create_exchange_symbol(base_ccy, asset):
        """In format BASECCY_ASSET"""
        return (base_ccy+'_'+asset).upper()

    def create_test_buy_order(self, quantity, asset, base_ccy):
        """ Uses API library to place test order"""


    def create_buy_order(self, quantity, asset, base_ccy):
        """ Uses API library to place real order"""

    def create_sell_order(self, quantity, asset, base_ccy):
        pass

    def get_current_prices(self):
        """ Gets current prices"""
        prices = self.client.returnTicker()

        price_dict = {}
        for assets in prices:
            base_ccy, asset = assets.split('_')
            user_symbol = create_user_symbol(asset,base_ccy)
            price_dict[user_symbol] = prices[assets]['last']

        #print(prices)
        return price_dict
