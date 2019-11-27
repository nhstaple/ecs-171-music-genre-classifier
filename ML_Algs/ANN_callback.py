# ANN_callback.py
# author - nick
## Description
## The callback function passed to keras's neural network train call

import numpy as np
import keras
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense
import pandas as pd
from tensorflow.keras.optimizers import SGD

# Call back function used to extract info from the model
# during training
class Callback(keras.callbacks.Callback):
	# add variables to keep track of parameters
	def __init__(self):
		# The weights of the network
		self.weights = []
	
	def on_train_begin(self, logs={}):
		return

	def on_train_end(self, logs={}):
		return
 
	#def on_epoch_begin(self, logs={}):
	#	return
 
	def on_epoch_end(self, epoch, logs={}):
		m = self.model
		self.weights.append(m.layers[0].get_weights())
		return
 
	def on_batch_begin(self, batch, logs={}):
		return
 
	def on_batch_end(self, batch, logs={}):
		return