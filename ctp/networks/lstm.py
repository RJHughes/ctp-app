import tensorflow as tf
import pandas as pd
import numpy as np


class LSTMTrader(object):
    """ Trader object that trains and deploys a LSTM prediction network """
    def __init__(self,
                 exchange,
                 training_data,
                 validation_data,
                 test_data,
                 lookback_period,
                 num_hidden):

        self.exchange = exchange
        self.training_data = training_data
        self.validation_data = validation_data
        self.test_data = test_data
        self.num_hidden = num_hidden
        self.lookback_period = lookback_period
        self.num_features = np.shape(self.training_data)[-1]


        self.inputs = tf.placeholder(tf.float32, [None, lookback_period, np.size(self.training_data, 1)])
        self.outputs = tf.placeholder(tf.float32, [None, 1])


        print('### LSTMTrader object created')

    def create_targets(self, data):
        """ This function takes a data sequence and splits it into the input
         to the network and the output data based on the intended input
         size given by the lookback period """

        print('### Creating targets')
        # A sample is defined as a sequence of length 'lookback_period'
        number_of_samples = len(data) - self.lookback_period - 1
        print('### Number of samples: ', number_of_samples)
        input = []
        output = []

        # Use a moving sample index to create X and Y
        # The input is a series of values
        # The output is the next value in the corresponding input series
        for sample in range(0, number_of_samples):
            input.append(data[sample:sample+self.lookback_period,:])
            output.append(data[sample+self.lookback_period,:])

        # Convert the lists to numpy arrays
        input = np.array(input, dtype='float64')
        output = np.array(output, dtype='float64')

        return input, output

    def build_lstm_layers(lstm_sizes, inputs, keep_prob_, batch_size):
        """
        Create the LSTM layers
        """
        lstms = [tf.contrib.rnn.BasicLSTMCell(size) for size in lstm_sizes]
        # Add dropout to the cell
        drops = [tf.contrib.rnn.DropoutWrapper(lstm, output_keep_prob=keep_prob_) for lstm in lstms]

        # Stack up multiple LSTM layers, for deep learning
        cell = tf.contrib.rnn.MultiRNNCell(drops)

        # Getting an initial state of all zeros
        initial_state = cell.zero_state(batch_size, tf.float32)
        lstm_outputs, final_state = tf.nn.dynamic_rnn(cell, inputs, initial_state=initial_state)

        return initial_state, lstm_outputs, cell, final_state

    def build_cost_fn_and_opt(lstm_outputs, labels_, learning_rate):
        """
        Create the Loss function and Optimizer
        """
        predictions = tf.contrib.layers.fully_connected(lstm_outputs[:, -1], 1, activation_fn=tf.sigmoid)
        loss = tf.losses.mean_squared_error(labels_, predictions)
        optimzer = tf.train.AdadeltaOptimizer(learning_rate).minimize(loss)

        return predictions, loss, optimzer


    def build_and_train_network(lstm_sizes, vocab_size, embed_size, epochs, batch_size,
                                learning_rate, keep_prob, train_x, val_x, train_y, val_y):

        inputs_ = self.inputs
        labels_ = self.labels
        keep_prob_ = tf.placeholder(tf.float32, name='keep_prob')

        initial_state, lstm_outputs, lstm_cell, final_state = build_lstm_layers(lstm_sizes, inputs_, keep_prob_,
                                                                                batch_size)
        predictions, loss, optimizer = build_cost_fn_and_opt(lstm_outputs, labels_, learning_rate)

        saver = tf.train.Saver()

        with tf.Session() as sess:

            sess.run(tf.global_variables_initializer())
            n_batches = len(train_x) // batch_size
            for e in range(epochs):
                state = sess.run(initial_state)

                train_acc = []
                for ii, (x, y) in enumerate(utl.get_batches(train_x, train_y, batch_size), 1):
                    feed = {inputs_: x,
                            labels_: y[:, None],
                            keep_prob_: keep_prob,
                            initial_state: state}
                    loss_, state, _ = sess.run([loss, final_state, optimizer], feed_dict=feed)
                    #train_acc.append(batch_acc)

                    if (ii + 1) % n_batches == 0:

                        val_acc = []
                        val_state = sess.run(lstm_cell.zero_state(batch_size, tf.float32))
                        for xx, yy in utl.get_batches(val_x, val_y, batch_size):
                            feed = {inputs_: xx,
                                    labels_: yy[:, None],
                                    keep_prob_: 1,
                                    initial_state: val_state}
                            val_batch_acc, val_state = sess.run([accuracy, final_state], feed_dict=feed)
                            val_acc.append(val_batch_acc)

                        print("Epoch: {}/{}...".format(e + 1, epochs),
                              "Batch: {}/{}...".format(ii + 1, n_batches),
                              "Train Loss: {:.3f}...".format(loss_),
                              "Train Accruacy: {:.3f}...".format(np.mean(train_acc)),
                              "Val Accuracy: {:.3f}".format(np.mean(val_acc)))

            saver.save(sess, "checkpoints/sentiment.ckpt")
