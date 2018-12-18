from .. exchange import Exchange


class Binance(Exchange):
    """Superclass that model common features of the Binance exchange"""

    def __init__(self, api_key, api_secret):
        Exchange.__init__(self, api_key, api_secret)
        self.name = "Binance"
        # Binance fees are 0.1%
        self.fee = 0.001

        # The names of the fields returned from the historical binance API
        self.kline_columns = ['Open time',
                              'Open',
                              'High',
                              'Low',
                              'Close',
                              'Volume',
                              'Close Time',
                              'Quote asset volume',
                              'Number of Trades',
                              'Taker buy base asset volume',
                              'Taker buy quote asset volume',
                              'Ignore']

    def create_symbol(self, base_ccy, asset):
        """Binance uses the symbol format ASSETBASE_CCY"""
        asset = self.user_to_exchange(self.name, asset)
        return (asset+base_ccy).upper()


"""

    def get_current_prices(self):
        """""" Gets current prices on Binance """"""

        prices = (self.client.get_all_tickers())
        price_dict = {}

        # Format the tickers to the general format
        for asset in prices:
            asset['symbol'] = self.exchange_to_user(self.name, asset['symbol'])
            price_dict[asset['symbol']] = asset['price']

        return price_dict
"""
