# ANN_class.py
# author nick s.
## from hw2

import numpy as np
from tensorflow import keras
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense
import pandas as pd
from tensorflow.keras.optimizers import SGD

from ANN_helpers import ANN_Parameter, CallBack

class ANN():
	# The constructor
	def __init__(
		self,
		# File name of a .csv with a trained neural network
		trained_model='',
		# Default parameters
		p=ANN_Parameter(),
		# Initialize the network's weights prior to training
		init=False):

		self.trained = False
		# TODO Check if the user provided an already trained model
		if trained_model != '':
			# Set the paramters
			self.trained = True
			# parameter_frame = pd.read_csv(
			# 	str(trained_model) + '_paramters.csv',
			# 	col=ANN_Parameter.keys
			# )
			# Set the hyperparemters for the constructorß
			# for feature in parameter_frame:
			#	p.parameters[feature] = parameter_frame[feature].values()[0]
			#
			# TODO
			# Set the weights 
			# w := [ [], [] , ..., [] ]
			# w = read list of lists from file: str(trained_model) + "_weights.csv"
			# m.set_weights(w)

		self.num_hidden_layers = p.parameters['num_hidden_layers']
		self.nodes_per_hidden = p.parameters['nodes_per_hidden']
		self.num_input = p.parameters['num_input']
		self.num_output = p.parameters['num_output']
		self.hidden_activation = p.parameters['hidden_activation']
		self.output_activation = p.parameters['output_activation']
		self.initialize = p.parameters['initialize']
		self.learning_rate = p.parameters['learning_rate']
		self.loss_function = p.parameters['loss_function']

		m = Sequential()
		# If init is set then initialize the weights and biases
		if init:
			# First hidden layer connected to input layer
			m.add(Dense(
				input_dim=self.num_input,
				units=self.nodes_per_hidden,
				activation=self.hidden_activation,
				kernel_initializer='zeros',
				bias_initializer='zeros'
			))
			
			# Remaining hidden layers
			for _ in range(1, self.num_hidden_layers):
				m.add(Dense(
					input_dim=self.nodes_per_hidden,
					units=self.nodes_per_hidden,
					activation=self.hidden_activation,
					kernel_initializer='zeros',
					bias_initializer='zeros'
				))

			if self.num_hidden_layers == 1:
				m.add(Dense(
					input_dim=self.num_hidden_layers,
					units=self.num_output,
					activation=self.output_activation,
					kernel_initializer='zeros',
					bias_initializer='zeros'
				))
			else:
				# Last hidden layer that leads to output Layer
				m.add(Dense(
					units=self.num_output,
					activation=self.output_activation,
					kernel_initializer='zeros',
					bias_initializer='zeros'
				))

		# Else use a random distribution to initalize (implicit)
		else:
			# First hidden layer
			m.add(Dense(self.nodes_per_hidden, input_dim=self.num_input, activation=self.hidden_activation))
			
			# Remaining hidden layers
			for _ in range(1, self.num_hidden_layers):
				m.add(Dense(self.nodes_per_hidden, activation=self.hidden_activation))
			
			if self.num_hidden_layers == 1:
				m.add(Dense(self.num_output, input_dim=self.nodes_per_hidden, activation=self.output_activation))
			else:
				# Last hidden layer that leads to output
				m.add(Dense(self.num_output, activation=self.output_activation))

		m.compile(loss=self.loss_function, optimizer=SGD(lr=self.learning_rate), metrics=['accuracy'])

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

		self.trained = True

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
		if not self.trained:
			print("ERROR! Trained to predict on an untrained network.\nSample\n{0}".format(sample))
			exit()

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
	net = ANN(p=ANN_Parameter(
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
	# history, callback = net.train(
	#	trainx,
	#	trainy,
	#	num_iter=NUM_EPOCHS,
	#	testing=test_set
	#)
