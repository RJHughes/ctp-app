import tensorflow as tf
from networks.network_utils import DataHandler
from networks.lstm import LSTMTrader
from exchanges.binance.binance_live import BinanceLive
import numpy as np
import matplotlib.pyplot as plt

# Pickle for debug and speed
import pickle


# Exchange instance
#binance = BinanceLive('abc', 'abc')

# Choose training options
symbol = "ETHBTC"
start_date = "1 Aug 2017"
end_date = "1 Aug 2018"

# Get the historic data
pkl_file = open('ETHBTC-Aug17-18.pkl', 'rb')
# historic_data = binance.get_historic_data(symbol, start_date, end_date)
historic_data = pickle.load(pkl_file)


# Set up the data handler
data = DataHandler(historic_data)

lstm = LSTMTrader(None,data.train,data.val,data.test,lookback_period=10,num_hidden=100)

X, Y = lstm.create_targets(data.train)

print(np.shape(Y))

plt.plot(X[2,0:10,1],'g')
plt.plot(X[1,0:10,1],'r')
plt.plot(X[0,0:10,1],'b')
plt.plot(10,Y[1,1],'rx')
plt.plot(10,Y[0,1],'bx')
plt.show()


"""lstm.build_and_train_network(lstm_sizes=1,
                             vocab_size=1,
                             embed_size=1,
                             epochs=5,
                             batch_size=4,
                             learning_rate=0.01,
                             keep_prob=0.5)"""
