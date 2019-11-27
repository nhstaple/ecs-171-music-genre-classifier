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

# the directory where the trained models are stored
TRAINED_MODEL_DIR = '../ML_Algs/trained_models/'

import sys
sys.path.append('../Back_End/')
import song_result_interface

from random import randint

# ANN - Artificial Neural Network
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

		self.scores = []
		self.trained = False
		# Check if the user provided an already trained model and set the hyperparameters
		if trained_model != '':
			print('Loading a model from disk!\nParameters loaded from disk:')
			parameter_frame = pd.read_csv(
				TRAINED_MODEL_DIR + str(trained_model) + '_parameters.csv',
			 	names=Parameter.keys,
			)
			# Adjust the parameters for construction
			for feature in parameter_frame:
				string = str(feature) + ': ' + str(parameter_frame[feature][0])
				print(string)
				p.parameters[feature] = parameter_frame[feature][0]

		print("\nbuilt using:\n{0}\n".format(p.parameters))

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
		self.features			= p.parameters['features']

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

		# m.compile(loss=self.loss_function, optimizer=SGD(lr=self.learning_rate), metrics=['accuracy'])
		m.compile(loss=self.loss_function, optimizer='adam', metrics=['categorical_accuracy'])


		# If the model is being loaded from disk then load the weights
		if trained_model != '':
			print('\nLoading trained weights!')
			# Load weights from disk
			w = np.load(TRAINED_MODEL_DIR + str(trained_model) + "_weights.npy", allow_pickle=True)

			# Set each layer's weights
			for i in range(0, len(m.layers)):
				m.layers[i].set_weights(w[i])

			# Set the trained flag
			self.trained = True
		
		# If the model is being loaded from disk, then load the features list
		if trained_model != '':
			print('\nLoading feature set!')
			self.features = np.load(TRAINED_MODEL_DIR + str(trained_model) + "_features.npy", allow_pickle=True)

		self.model = m
		print('ANN() constructor finished\n********\n')

	# trains the network on the provided parameters
	# if testing is empty then no validation is done
	# returns the history and weights
	def train(self, X, Y, num_iter=100, testing=(), batch=1, test_ratio=0.00, interactive=False):
		print('Training model with {0} epochs, batch size {1}'.format(num_iter, batch))

		if interactive:
			self.show_weights(self.num_hidden_layers + 1)
			input('Press enter to train the model...')

		# The callback object.
		c = Callback()

		# The accuracy record
		hist = 0

		# Flag that indicates if a testing set was provided
		test_provided = False

		if batch < 1:
			print('error bad batch size:\t{}'.format(batch))

		# if there wasn't a test
		if len(testing) == 0:
			test_provided = False

			# If there was a testing set
			if test_ratio < 0.00:
				print('error invalid ratio {}'.format(test_ratio))

			if not (test_ratio > 0.00 and test_ratio <= 2/3):
				print('error invalid ratio {}'.format(test_ratio))
				test_ratio = 1/3
		# else there was a test
		else:
			if test_ratio != 0.00:
				print('warning invalided param when test set provided {}'.format(test_ratio))
			test_provided = True
			
		if test_provided and batch < 0:
			print('Training with provided data and default batch size.')
			hist = self.model.fit(X, np.array(Y), epochs=num_iter, callbacks=[c], validation_data=testing)
		elif test_provided and batch >= 1:
			print('Training with provided data and batch size of {}.'.format(batch))
			hist = self.model.fit(X, np.array(Y), epochs=num_iter, callbacks=[c], validation_data=testing, batch_size=batch)
		elif (not test_provided) and batch < 0:
			print('Training with validation ratio of {} default bath size.'.format(test_ratio))
			hist = self.model.fit(X, np.array(Y), epochs=num_iter, callbacks=[c], validation_split=test_ratio)
		elif (not test_provided) and batch >= 1:
			print('Training with validation ratio of {0} and batch size of {1}.'.format(test_ratio, batch))
			hist = self.model.fit(X, np.array(Y), epochs=num_iter, callbacks=[c], validation_split=test_ratio, batch_size=batch)

		if interactive:
			self.show_weights(self.num_hidden_layers + 1)
			input('Press enter to continue...')

		self.trained = True
		return hist, c
	
	# Print the weights of the network
	def show_weights(self, num=1):
		print('Displaying the weights for {} layers.'.format(num))

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

	# guesses uniformly on each genre of a song's prediction
	def naive_predict(self, sample, num_predictions=16):
		if not self.trained:
			print("ERROR! Trained to predict on an untrained network.\nSample\n{0}".format(sample))
			exit()

		result = sample

		vector = dict()
		for i in range(0, len(classes)):
			vector[classes[i]] = randint(1, num_predictions)/16

		vector_vals = vector.values()
		vector = sorted(vector, key = lambda i: vector[i],reverse=True)

		new_vector = dict()
		counter = 0
		for i in range(0, len(vector)):
			prediction = list(vector_vals)[counter]
			new_vector[vector[i]] = prediction
			counter = counter + 1
		vector = new_vector

		score = 16
		for i in range(0, len(classes)):	
			if list(vector.keys())[i] in sample['genre_top']:
				score = i + 1
				break

		result['prediction'] = dict()
		result['prediction']['genres'] = vector
		result['prediction']['score'] = score
		result['prediction']['result'] = list(vector.keys())[0]

		self.scores.append(result['prediction']['score'])
		return result

	# performs a prediction based on the sample
	# assume that the model is trained
	# returns an instance of Result(), see ANN_result.py
	def predict(self, sample):
		num_predictions = 16
		if not self.trained:
			print("ERROR! Trained to predict on an untrained network.\nSample\n{0}".format(sample))
			exit()

		result = sample
		X = sample['X']
		prediction = self.model.predict(X)[0]

		# print('Showing Results for Prediction')

		max_category = {
			'index': 0,		# the index the item is in the classes list
			'value': -1.00	# the value of the prediction
		}

		max_hist = []
		for i in range(0, len(classes)):
			# string = str(classes[i]) + ': ' + str(prediction[i])
			# print(string)
			max_category['index'] = i
			max_category['value'] = prediction[i]
			max_hist.append(max_category)
			max_category = max_category.copy()

		max_hist = sorted(max_hist, key = lambda i: i['value'],reverse=True) 

		result['prediction'] = dict()
		result['prediction']['genres'] = dict()
		initial = False
		for i in range(0, num_predictions):
			if not initial: initial = True; result['prediction']['result'] = classes[max_hist[i]['index']]
			index = max_hist[i]['index']
			probability = max_hist[i]['value']
			result['prediction']['genres'][classes[index]] = probability

		for i in range(0, len(max_hist)):
			pred = classes[max_hist[i]['index']]
			# check if sample['genre_top'] is a list
			# go through list and see if pred is in the list and set the score
			if pred in sample['genre_top']:
				result['prediction']['score'] = i+1 #score [1,16]
		self.scores.append(result['prediction']['score'])
		return result

	# save the model to disk into the ML_Algs/trained_models/ directory
	# save parameters, weights, and features
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

		# Save independent feature indices to disk
		np.save(TRAINED_MODEL_DIR + model_name + '_features',self.get_features())

		f1 = TRAINED_MODEL_DIR + model_name + '_parameters.csv'
		f2 = TRAINED_MODEL_DIR + model_name + '_weights.npy'
		f3 = TRAINED_MODEL_DIR + model_name + '_features.npy'
		print('Saved\n\t{0}\n\t{1}\n\t{2}\n'.format(f1, f2, f3))
	
	#Returns the mean score of the model
	def get_mean_score(self):
		total_score = 0.0
		for i in range(0,len(self.scores)):
			total_score += self.scores[i]
		return total_score/(len(self.scores))

	# returns the features used for training the model
	def get_features(self):
		return self.features

