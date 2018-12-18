from .binance import Binance


class BinanceBacktest(Binance):
    """ Models the Binance exchange using previous saved values """

    def __init__(self, api_key, api_secret):
        Binance.__init__(self, api_key, api_secret)

    def buy(self, quantity, asset, base_ccy):
        """ Uses """

        return order
