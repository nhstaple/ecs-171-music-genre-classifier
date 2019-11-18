# ANN_example.py

from sklearn.model_selection import train_test_split
import numpy as np
import pandas as pd
from genres import classes, NUM_GENRES
from ANN_parameter import Parameter
from ANN_result import Result
from ANN_class import ANN
from ANN_encode import encode, decode
import random

# TODO change to a list of features
indepent_features = ['mfcc', 'spectral_contrast']

# set your experiment seed for train test split
EXPERIMENT_SEED = 42

# Load model or train model?
g = input("Load a model from disk? (y/n)\t") 
MODEL_NAME = ''
if g == 'y' or g == 'Y':
	MODEL_NAME = input('Name of your model: \t')
elif g == 'n' or g == 'n':
	print('Generating a new model')
else:
	MODEL_NAME = g
	print('Model name: {}\n'.format(MODEL_NAME))

## Process Data
# Load the Data Management's interface
import sys
sys.path.append('../Data_Management/')
import CSVInterface

print('Initializing Data Management interface...')
# reads the data from the csv
reader = CSVInterface.featRead()

# D = { X | Y }
# D[X][Y]
D = {}
print('reading all features')
# X
D['X'] =  {
	'small'	: reader.getSubset(
				reader.getFrame('features')
			),
	'full'	: reader.getFrame('features')
}

D['Y'] = {
	'small'	: reader.getSubset(
		reader.getFrame('track')['genre_top']
	),
	'full'	: reader.getFrame('track')['genre_top']
}

# Show all the weights prior to training
# net.show_weights(net.num_hidden_layers + 1)

# The data after removing outliers
# data = outlier_method(RawData)

print('Constructing datasets')
print('X')
# the ind vars
X =  pd.DataFrame(D['X']['small'][
		indepent_features]
	)

print('Y')
# the dependent var
Y = pd.DataFrame(D['Y']['small'], columns=['genre_top'])

print('train/test split')
# Test and train split using encoded Y labels (vector of 0s with one 1)
trainx, testx, trainy, testy = train_test_split(
	X.values,
	encode(Y), # one hot encoder, see ANN_encode.py
	test_size=0.34,
	random_state=EXPERIMENT_SEED
)

sample = trainx[0].copy()
print('Data done!\n\n********')

## Build the neural network
print('\nBuilding neural net')
print('input : {}'.format(len(sample)))
print('output: {}\n'.format(NUM_GENRES))

net = 0
history = 0
callback = 0

# Use this for pre trained models
if MODEL_NAME != '':
	net = ANN(trained_model=MODEL_NAME)
else:
	# Use this to test your own architecture
	net = ANN(p=Parameter(
		num_input=len(sample),
		num_hidden_layers=8,
		nodes_per_hidden=16,
		num_output=NUM_GENRES,
		hidden_activation='relu',
		output_activation='softmax',
		initialize=False,
		loss_function='categorical_crossentropy'
	))

	# Show the weights
	# net.show_weights(net.num_hidden_layers + 1)

	input('Press enter to train the model...')

	# Train the network
	# returns history of training process, and a callback object that can
	# extract information about the model at the end of events ANN_callbacks.py
	history, callback = net.train(
		trainx,
		trainy,
		num_iter=500,
		testing=(testx, np.array(testy)),
		batch=10
	)

# Set the sample to a specific value. I recommend producing a synthetic sample
# from the data set. Look into pandas.DataFrame.quantile(0, 1.00) to get the min and max to to
# a standard the bounds for the distribution
# for i in range(0, len(sample)):
# 	sample[i] = random.uniform(-100, 100)

# The software engineering team makes this ANN.predict() call, then
# add missing information to ANN_result.Result, then adds it to a wrapper
# to send to the front end!

## Predicting
# Let's see how accurate the model is for the top @num_to_check many categories
# the number of test samples to predict
samples = 0
# The number of test samples to check
samples = int(input('Begin prediction on test set.\nNumber of samples:\t'))
# the number of results to check
num_to_check = int(input('Number of predictions to check:\t'))

print('\n')
top_predictions = '\nResults\n'
for num in range(1, num_to_check + 1):
	print('Computing top {}'.format(num))
	# keeps track of number of matches
	matches = 0
	for i in range(0, samples):
		sample = np.array(testx[i].copy())
		sample = pd.DataFrame([sample], columns=X.columns)
		result = net.predict(sample.values)
		counter = 0
		sample_category = decode(testy[i])

		for genre in result.res['prediction']:
			if genre == sample_category and counter < num:
				matches = matches + 1
			# print("{0}: {1}".format(genre, result.res['prediction'][genre]))
			if counter >= num: break
			else: counter = counter + 1
	top_predictions = top_predictions + 'Classification for top {0} predictions:\t{1}\n'.format(num, matches / samples)

print(top_predictions)

## Save the Model
# For the ML team: copy and paste this file and name it one word, <your name>
# ANN_<your name>.py
if MODEL_NAME == '':
	g = input("Save model? (y/n)\t") 
	if g == 'Y' or g == 'y':
		g = input('model name: ')
		net.save_to_disk(g)