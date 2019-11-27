# ANN_parameter.py
# author nick s.
## Description
## this class acts as a parameter for the ANN_class constructor

import numpy as np
from tensorflow import keras
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense
import pandas as pd
from tensorflow.keras.optimizers import SGD
from genres import classes

DEF_INPUT_NODES = 8
DEF_OUTPUT_NODES = len(classes)
DEF_HIDDEN_LAYERS = 2
DEF_NODES_PER_LAYER = 3
DEF_HIDDEN_ACTIVATION = 'sigmoid'
DEF_OUTPUT_ACTIVATION = 'sigmoid'
DEF_LEARNING_RATE = 10
DEF_LOSS_FUNCTION = 'mean_squared_error'
DEF_FEATURES = [0]

# Make a parameter object to be passed to the constructor of the ANN
# Interface for the .csv file
class Parameter():
	# interface
	keys = [
		'num_input',
		'num_hidden_layers',
		'nodes_per_hidden',
		'num_output',
		'hidden_activation',
		'output_activation',
		'initialize',
		'learning_rate',
		'loss_function'
	]

	# cosntructor
	def __init__(
		self,
		num_input=DEF_INPUT_NODES,
		num_hidden_layers=DEF_HIDDEN_LAYERS,
		nodes_per_hidden=DEF_NODES_PER_LAYER,
		num_output=DEF_OUTPUT_NODES,
		hidden_activation=DEF_HIDDEN_ACTIVATION,
		output_activation=DEF_OUTPUT_ACTIVATION,
		initialize=True,
		learning_rate=DEF_LEARNING_RATE,
		loss_function=DEF_LOSS_FUNCTION,
		features = DEF_FEATURES):

		self.parameters = {
			'num_input': num_input,
			'num_hidden_layers': num_hidden_layers,
			'nodes_per_hidden': nodes_per_hidden,
			'num_output': num_output,
			'hidden_activation': hidden_activation,
			'output_activation': output_activation,
			'initialize': initialize,
			'learning_rate':learning_rate,
			'loss_function': loss_function,
			'features':features
		}