from math import ceil
from plistlib import Dict
import psycopg2

from ctp.utilities import *
import time


class Exchange(object):
    def __init__(self, api_key, api_secret):
        self.api_key = api_key
        self.api_secret = api_secret
        """This dictionary defines naming conversions for specific sites"""
        self.user_to_exchange_ticker: Dict[Tuple[str, str], str] = {("Binance", "BCH"): "BCC",("Binance","BCHBTC"):"BCCBTC"}
        self.exchange_to_user_ticker = {}
        self.db = 'localhost/tradereg.trade_table'
        """This dictionary converts the site naming conversion to the general one"""
        for items in self.user_to_exchange_ticker:
            self.exchange_to_user_ticker[(items[0],self.user_to_exchange_ticker[items])] = items[1]

    def user_to_exchange(self, exchange, asset):
        """ Converts user tickers to exchange specific ones """
        if self.user_to_exchange_ticker.get((exchange, asset), None) is None:
            return asset
        else:
            return self.user_to_exchange_ticker[exchange, asset]

    def exchange_to_user(self, exchange, asset):
        """ Converts specific exchange tickers to user ones """
        if self.exchange_to_user_ticker.get((exchange, asset), None) is None:
            return asset
        else:
            return self.exchange_to_user_ticker[exchange, asset]

    def add_to_tradereg(self, order):

        # Connect to trade register database
        conn = create_connection(self.db)
        # Add order details to trade register database
        #with conn:
        table_entry = (ceil(time.time()),
                       order['symbol'],
                       order['price'],
                       order['executedQty'])

        print(table_entry)
        """ Adds trade details to register """
        sql = " INSERT INTO trade_table(time, symbol, price, quantity) VALUES(%s ,%s ,%s  ,%s ); "

        # Add the data to the database
        cur = conn.cursor()
        print(cur)
        cur.execute(sql, table_entry)
        conn.commit()
        conn.close()
        cur.close()
        # Returns the id of the last row in  the database
        return cur.lastrowid
