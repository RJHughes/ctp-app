from binance.client import Client
from exchanges.binance.binance import Binance
import pandas as pd


class BinanceLive(Binance):
    """ Class that abstracts the live Binance exchange into
    a common framework"""

    def __init__(self, api_key, api_secret):
        Binance.__init__(self, api_key, api_secret)

        # Creating the Client object tries to connect to the exchange
        try:
            self.client = Client(self.api_key, self.api_secret)
            print('### Connected to Binance client successfully')
        except:
            print('### Could not connect to Binance client')

    def get_historic_data(self, symbol, start_date, end_date):
        """ Gets historical data """
        # Get historical Klines from the exchange
        # Interval is hardcoded just now. More options for intervals on
        # https://github.com/binance-exchange/binance-official-api-docs/blob/master/rest-api.md
        klines = self.client.get_historical_klines(symbol, self.client.KLINE_INTERVAL_6HOUR, start_date, end_date)

        # Format the klines as a pandas DataFrame using the column names from the SuperClass
        return pd.DataFrame(klines, columns=self.kline_columns)

    def test_buy(self, quantity, asset, base_ccy):
        """Uses Binance API library to place test order"""

        symbol = self.create_symbol(base_ccy, asset)

        order = self.client.create_test_order(
            symbol=symbol,
            side=Client.SIDE_BUY,
            type=Client.ORDER_TYPE_MARKET,
            quantity=quantity)

        print(order)

    def test_sell(self, quantity, asset, base_ccy):
        """Uses Binance API library to place test order"""

        symbol = self.create_symbol(base_ccy, asset)

        order = self.client.create_test_order(
            symbol=symbol,
            side=Client.SIDE_SELL,
            type=Client.ORDER_TYPE_MARKET,
            quantity=quantity)

    def buy(self, quantity, asset, base_ccy):
        """ Uses Binance API library to place real order"""

        symbol = self.create_symbol(base_ccy, asset)

        order = self.client.create_order(
            symbol=symbol,
            side=self.client.SIDE_BUY,
            type=self.client.ORDER_TYPE_LIMIT,
            timeInForce=self.client.TIME_IN_FORCE_GTC,
            quantity=quantity,
            price='0.0017')

        print(order)
        self.add_to_tradereg(order)

    def get_orders(self, symbol):
        orders = self.client.get_all_orders(symbol=symbol, limit=10)
        return orders

    def sell(self,quantity, asset, base_ccy):

        order = self.client.create_test_order(
            symbol='BNBBTC',
            side=SIDE_BUY,
            type=ORDER_TYPE_LIMIT,
            timeInForce=TIME_IN_FORCE_GTC,
            quantity=100,
            price='0.00001')
