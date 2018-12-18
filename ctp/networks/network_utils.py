import numpy as np


class DataHandler(object):
    """ This class is assosciated with the training data for a network"""
    def __init__(self, data, train_fraction=0.7, val_fraction=0.15):
        self.data = np.array(data)
        self.train_fraction = train_fraction
        self.val_fraction = val_fraction
        self.train, self.val, self.test = self._split_data(self.data, self.train_fraction, self.val_fraction)
        print('### Data handler object created')
        print('###', len(self.data), ' data points')
        print('###', round(self.train_fraction*100), '% for Training (', len(self.train), ') points')
        print('###', round(self.val_fraction * 100), '% for Validation (', len(self.val), ') points')
        print('###', round((1.0-self.val_fraction-self.train_fraction)*100), '% for Test (', len(self.test), ') points')

    def _split_data(self, data, train_perc, val_perc):
        """ Splits the historical data for training, validation and test"""

        train_val_split = int(train_perc*len(data))
        val_test_split = int((train_perc + val_perc)*len(data))

        train, val, test = np.split(self.data, [train_val_split, val_test_split])
        return train, val, test
