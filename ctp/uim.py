import strategies.test_strategy as test

import time

strategy_1 = test.TestStrategy(id_value="1", base_ccy="BTC")

strategy_1.start()

for i in range(0, 1000):
    print(i)
    time.sleep(1)
#strategy_2 = arbitrage.Arbitrage(id_value = "2", base_ccy="BTC")



#strategy_2.run()
