# ANN_class.py
# author nick s.
## from hw2

import numpy as np
from tensorflow import keras
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense
import pandas as pd
from tensorflow.keras.optimizers import SGD

from genres import classes
from ANN_parameter import Parameter
from ANN_callback import Callback
from ANN_encode import encode
from ANN_result import Result

TRAINED_MODEL_DIR = './trained_models/'

# ANN - Artificial Neural Network
# constructor
# ANN
#   input:
# 	- trained_model: name of the model. There should be a _paramters.csv and _weights.csv associated with the name
# 	- p: the parameters. See ANN_Parameter.py for info on how to change the parameters
# 	- init: should the model have it's weights initialized. TODO: set the initialization
#
# Methods
#	X is a Pandas data frame, Y the dependent columumn in the dataframe, encode() is a onehotencoder see ANN_encode.py
#	returns the history, and the callback (callback defined in ANN_callback.py)
#	ANN.train(X, encode(Y), num_iter=100, testing=(), batch=-1):

# 	Num is the number of layers to print starting from the last layer
#	ANN.show_weights(num=1)

#	Sample is a pandas dataframe with one row. That's how I made it for the homework but an array of arrays might work, too.
#	Returns a result object, see ANN_result.py
# 	ANN.predict(sample)

class ANN():
	# The constructor
	def __init__(
		self,
		# File name of a .csv with a trained neural network
		trained_model='',
		# Default parameters, see ANN_parameters.py for class definition
		p=Parameter(),
		# Initialize the network's weights prior to training
		init=False):

		self.trained = False
		# Check if the user provided an already trained model and set the hyperparameters
		if trained_model != '':
			print('Loading a model from disk!')
			parameter_frame = pd.read_csv(
				TRAINED_MODEL_DIR + str(trained_model) + '_parameters.csv',
			 	names=Parameter.keys
			)
			# Adjust the parameters for construction
			for feature in parameter_frame:
				string = str(feature) + ': ' + str(parameter_frame[feature][0])
				print(string)
				p.parameters[feature] = parameter_frame[feature][0]
			print('\n\n')

		# Set the parameters that are visible outside of the class's methods
		self.num_hidden_layers 	= p.parameters['num_hidden_layers']
		self.nodes_per_hidden 	= p.parameters['nodes_per_hidden']
		self.num_input 			= p.parameters['num_input']
		self.num_output 		= p.parameters['num_output']
		self.hidden_activation 	= p.parameters['hidden_activation']
		self.output_activation 	= p.parameters['output_activation']
		self.initialize 		= p.parameters['initialize']
		self.learning_rate 		= p.parameters['learning_rate']
		self.loss_function 		= p.parameters['loss_function']

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

		# If the model is being loaded from disk then load the weights
		if trained_model != '':
			print('Loading trained weights!')
			# Load weights from disk
			w = np.load(TRAINED_MODEL_DIR + str(trained_model) + "_weights.npy", allow_pickle=True)

			# Set each layer's weights
			for i in range(0, len(m.layers)):
				m.layers[i].set_weights(w[i])

			# Set the trained flag
			self.trained = True

		self.model = m

	# trains the network on the provided parameters
	# if testing is empty then no validation is done
	# returns the history and weights
	def train(self, X, Y, num_iter=100, testing=(), batch=-1):
		# The callback object.
		c = Callback()

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
		if num < 1:
			num = len(self.model.layers) - 1
			return

		index = len(self.model.layers) - 1
		for _ in range(0, num):
			if index < 0: break
			print("\n****\nLayer L - {}".format(index))
			print("Bias")
			print(self.model.layers[index].get_weights()[1])
			print("Weights")
			print(self.model.layers[index].get_weights()[0])
			index = index - 1

	# performs a prediction based on the sample
	# assume that the model is trained
	# returns an instance of Result(), see ANN_result.py
	def predict(self, sample):
		if not self.trained:
			print("ERROR! Trained to predict on an untrained network.\nSample\n{0}".format(sample))
			exit()

		result = Result(
			title='',
			artist=''
		)

		prediction = self.model.predict(sample)[0]
		print('Results')
		max_category = [0, 0.00]
		max_hist = []
		for i in range(0, len(classes)):
			if max_category[1] < prediction[i]:
				max_hist.append(max_category)
				max_category = [i, prediction[i]]

		i = len(max_hist) - 1
		result.res['prediction'] = dict()
		while len(result.res['prediction']) < len(Result.interface['prediction']) and i >= 0:
			top_result = max_hist[i]
			index = top_result[0]
			probability = top_result[1]
			result.res['prediction'][classes[index]] = probability
			i = i - 1
		
		return result

	def save_to_disk(self, model_name='test'):
		# Save the parameters to disk
		parameter_file = open(TRAINED_MODEL_DIR + model_name + '_parameters.csv', "w")
		p = str(self.num_input) + ',' + str(self.num_hidden_layers) + ',' + str(self.nodes_per_hidden) + ',' + str(self.num_output) + ',' + self.hidden_activation + ',' + self.output_activation + ',' + str(self.initialize) + ',' + str(self.learning_rate) + ',' + self.loss_function
		parameter_file.write(p)
		parameter_file.close()

		# Save the weights to disk
		w = []
		for i in range(0, len(self.model.layers)):
			w.append(self.model.layers[i].get_weights())
		w = np.array(w)
		np.save(TRAINED_MODEL_DIR + model_name + '_weights', w)


test = True

if test:
	# Load a trained model
	net = ANN(trained_model='test_0')
	# Show the last two layers of weights
	net.show_weights(2)
