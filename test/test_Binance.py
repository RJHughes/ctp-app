import unittest
#from binance.exceptions import BinanceAPIException
import sys
sys.path.append('..')

from ctp.exchanges.binance.binance import Binance
from ctp.exchanges.binance.binance_bt import BinanceBacktest
from ctp.exchanges.binance.binance_live import BinanceLive

class TestBinanceMethods(unittest.TestCase):

    def setUp(self):
        # These keys are sample keys from
        # https://github.com/binance-exchange/binance-official-api-docs/blob/master/rest-api.md
        self.key = "vmPUZE6mv9SD5VNHk4HlWFsOr6aKE2zvsw0MuIgwCIPy6utIco14y7Ju91duEh8A"
        self.secret = "NhqPtmdSJYdKjVHjA7PZj4Mge3R5YNiP1e3UZjInClVN65XAbvqqM6A7H5fATj0j"
        self.binance_super = Binance(self.key, self.secret)
        self.binance_backtest = BinanceBacktest(self.key, self.secret)
        self.binance_live = BinanceLive(self.key, self.secret)

    def tearDown(self):
        # Closes the connection to the exchange,
        # Not a necessary line of code but gets rid of warnings
        self.binance_live.client.session.close()

    def test_that_Binance_exchange_is_live(self):
        """ Generic test that the exchange is live """
        status = self.binance_live.client.get_system_status()
        self.assertEqual(status,{'msg': 'normal', 'status': 0})

    def test_setup_for_Binance_super(self):
        self.assertEqual(self.binance_super.api_key, self.key)

    def test_setup_for_Binance_backtest(self):
        self.assertEqual(self.binance_backtest.api_key, self.key)

    def test_setup_for_Binance_live(self):
        self.assertEqual(self.binance_live.api_key, self.key)

    def test_buy_order_on_Binance_exchange(self):
        """ Uses test buy function to place a dummy order """
        order = self.binance_live.create_test_buy_order(1,"BCH","BTC")
        # Dummy order should return an empty json
        self.assertEqual(order,{})
