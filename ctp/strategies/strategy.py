import threading


class Strategy(threading.Thread):
    """Superclass for defining common elements of every strategy
    developers are free to create a strategy using whatever constructs they want.
    Strategies can combine multiple exchanges. Strategy also inherits from threading.Thread
    allowing each strategy to be ran asynchronously of each other
    """

    def __init__(self, id_value, base_ccy):
        threading.Thread.__init__(self)
        """ Every strategy has common elements that are assigned here"""
        self.id_value = id_value
        self.base_ccy = base_ccy
        self.run_condition = True
