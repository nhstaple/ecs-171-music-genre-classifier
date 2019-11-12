# ANN_class.py
# author nick s.
## from hw2

import numpy as np
from tensorflow import keras
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense
import pandas as pd
from tensorflow.keras.optimizers import SGD

class CallBack(keras.callbacks.Callback):
	# add variables to keep track of parameters

	def on_train_begin(self, logs={}):
		return

	def on_train_end(self, logs={}):
		return
 
	def on_epoch_begin(self, logs={}):
		return
 
	def on_epoch_end(self, epoch, logs={}):
		return
 
	def on_batch_begin(self, batch, logs={}):
		return
 
	def on_batch_end(self, batch, logs={}):
		return

# Placeholder classes
classes = ['Genre 1', 'Genre 2', 'Genre 3', 'Genre 4']

# Make a parameter object to be passed to the constructor of the ANN
def make_p(
		num_input=10,
		num_hidden_layers=2,
		nodes_per_hidden=3,
		num_output=len(classes),
		hidden_activation='sigmoid',
		output_activation='sigmoid',
		initialize=True,
		learning_rate=10,
		loss_function='mean_squared_error'):

	parameters = {
		'num_input': num_input,
		'num_hidden_layers': num_hidden_layers,
		'nodes_per_hidden': nodes_per_hidden,
		'num_output': num_output,
		'hidden_activation': hidden_activation,
		'output_activation': output_activation,
		'initialize': initialize,
		'learning_rate':learning_rate,
		'loss_function': loss_function
	}

	return parameters

class ANN():
	def __init__(
		self,
		p=dict(),
		num_in=10,
		num_hidden=2,
		nodes_per_hid=3,
		num_out=4,
		hidden_a='sigmoid',
		output_a='sigmoid',
		init=False,
		lamb=10,
		loss_func='mean_squared_error'):

		# If the network was passed a paramter object
		if len(p):
			num_in = p['num_input']
			num_in = p['num_input']
			num_hidden = p['num_hidden_layers']
			nodes_per_hid = p['nodes_per_hidden']
			num_out = p['num_output']
			hidden_a = p['hidden_activation']
			output_a = p['output_activation']
			init = p['initialize']
			lamb = p['learning_rate']
			loss_func = p['loss_function']

		self.hidden = num_hidden
		self.nodehiddden = nodes_per_hid
		self.output = num_out
		self.activ = hidden_a
		self.init = init
		self.input = num_in

		m = Sequential()
		# If init is set then initialize the weights and biases
		if init:
			# First hidden layer connected to input layer
			m.add(Dense(
				input_dim=num_in,
				units=nodes_per_hid,
				activation=hidden_a,
				kernel_initializer='zeros',
				bias_initializer='zeros'
			))
			
			# Remaining hidden layers
			for _ in range(1, num_hidden):
				m.add(Dense(
					input_dim=nodes_per_hid,
					units=nodes_per_hid,
					activation=hidden_a,
					kernel_initializer='zeros',
					bias_initializer='zeros'
				))

			if num_hidden == 1:
				m.add(Dense(
					input_dim=num_hidden,
					units=num_out,
					activation=output_a,
					kernel_initializer='zeros',
					bias_initializer='zeros'
				))
			else:
				# Last hidden layer that leads to output Layer
				m.add(Dense(
					units=num_out,
					activation=output_a,
					kernel_initializer='zeros',
					bias_initializer='zeros'
				))

			## TODO set desired weights to 1

		# Else use a random distribution to initalize (implicit)
		else:
			# First hidden layer
			m.add(Dense(nodes_per_hid, input_dim=num_in, activation=hidden_a))
			
			# Remaining hidden layers
			for _ in range(1, num_hidden):
				m.add(Dense(nodes_per_hid, activation=hidden_a))
			
			if num_hidden == 1:
				m.add(Dense(num_out, input_dim=nodes_per_hid, activation=output_a))
			else:
				# Last hidden layer that leads to output
				m.add(Dense(num_out, activation=output_a))

		m.compile(loss=loss_func, optimizer=SGD(lr=lamb), metrics=['accuracy'])
		self.model = m

	# trains the network on the provided parameters
	# if testing is empty then no validation is done
	# returns the history and weights
	def train(self, X, Y, num_iter=100, testing=(), batch=-1):
		# The callback object.
		c = CallBack()

		# The accuracy record
		hist = 0

		# If there was a testing set
		if len(testing) and batch < 0:
			hist = self.model.fit(X, np.array(Y), epochs=num_iter, callbacks=[c], validation_data=testing)
		elif len(testing) and batch >= 0:
			hist = self.model.fit(X, np.array(Y), epochs=num_iter, callbacks=[c], validation_data=testing, batch_size=batch)
		# Else don't validate
		elif batch < 0:
			hist = self.model.fit(X, np.array(Y), epochs=num_iter, callbacks=[c])
		else:
			hist = self.model.fit(X, np.array(Y), epochs=num_iter, callbacks=[c], validation_data=testing, batch_size=batch)

		return hist, c
	
	# Print the weights of the network
	def show_weights(self, num=1):
		## TODO make general
		print("\n****\nLayer L - 3")
		print("Bias")
		print(self.model.layers[0].get_weights()[1])
		print("Weights")
		print(self.model.layers[0].get_weights()[0])
		# print("\n****\nLayer L - 2")
		# print(self.model.layers[1].get_weights()[1])
		# print(self.model.layers[1].get_weights()[0])
		# print("\n****\nLayer L - 1")
		# print(self.model.layers[2].get_weights()[1])
		# print(self.model.layers[2].get_weights()[0])

	# performs a prediction based on the sample
	# assume that the model is trained
	def predict(self, sample):
		prediction = self.model.predict(sample)[0]
		print('Results')
		max_category = [0, 0.00]
		for i in range(0, 10):
			if max_category[1] < prediction[i]:
				max_category = [i, prediction[i]]
			print("{0}:\t{1:.4f}%".format(classes[i], 100 * prediction[i]))
			
		print('\n{0}\n\nMost likely: {1}'.format(sample, classes[max_category[0]]))


test = True

if test:
	net = ANN(p=make_p(
		# paramterize if you want
	))

	# TODO make this a general function for showin n layers or a specific layer
	net.show_weights()

	# The data after removing outliers
	# data = outlier_method(RawData)

	# Test and train split using encoded Y labels (vector of 0s with one 1)
	# trainx, testx, trainy, testy = train_test_split(
	# 	data.drop(columns=[dep]),
	#	encode(data), # one hot encoder
	#	test_size=0.34,
	#	random_state=EXPERIMENT_SEED
	#)

	# Ordered pair for validating the ANN
	# test_set = (testx, np.array(testy))

	# Train the network
	# returns history of training process, and a callback object that can extract information about the model at the end of events
	# h, w = net.train(
	#	trainx,
	#	trainy,
	#	num_iter=NUM_EPOCHS,
	#	testing=test_set
	#)
