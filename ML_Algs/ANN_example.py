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
sys.path.append('../Back_End/')
sys.path.append('../Data_Management/')
import CSVInterface
import song_result_interface

print('Initializing Data Management interface...')
# reads the data from the csv
reader = CSVInterface.featRead()

# D = { X | Y }
# D[X][Y]
D = {}
print('reading all features. NOTE using placeholder functionality for DataManagements interface. We are just given features and return a distribution of probalities.')
# print('We also score our prediction and provide a threshold for how large a list you need to construct of the sorted predictions to have a 100% gurantee of having the y_actual.')
# print('Our prediction is part of a pipeline that sets the prediction field from the back ends interface, the field backend/song_result_interface.result[predictions].')

# result = {
#  # data team
#	'song_id' : int(),
#	'title': 'Song Title From Front End',
#
#	## add more info like year or record label
#	'metadata': {  # for front end team
#		'artist': str()
#	},
#
#	## get data for ml prediction
#	'subset': str(), # small, medium, full...
#	'X': [[]], # the features for the song with matching title, use pd.DataFrame.values
#	'top_genre':  str(), # from tracks.csv
#
#	# the result of the ml team's prediction
#	# ml team interface
#	'prediction': {
#		'threshold': int(), # build a list of threshold length to guarantee it will contain the answer
#		'genres': {  # list of 16 of genre probabilities sorted by most likely to least likely
#		},
#		'score': int() # position the actual top_genre is in the list of  prediction.genres
#	},
#
#	# back end team
#	'error': '' # init to empty string. front end team will have to handle: error, 1 result, more than 1 results.
#}

# X
D['X'] =  {
	'small'	: reader.getSubset(
				reader.getFrame('features'),
				sub='small'
			),
	'cleanLarge' : reader.getSubset(
				reader.getFrame('features'),
				sub='cleanLarge'
			)
}

# Y
D['Y'] = {
	'small'	: reader.getSubset(
		reader.getFrame('track')['genre_top'],
		sub='small'
	),
	'cleanLarge': reader.getSubset(
		reader.getFrame('track')['genre_top'],
		sub='cleanLarge'
	),
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

print('train/validation split')
# Test and train split using encoded Y labels (vector of 0s with one 1)
trainx, valx, trainy, valy = train_test_split(
	X.values,
	encode(Y), # one hot encoder, see ANN_encode.py
	test_size=0.10,	# validation size
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
		num_hidden_layers=2,
		nodes_per_hidden=16,
		num_output=NUM_GENRES,
		hidden_activation='relu',
		output_activation='softmax',
		initialize=False,
		loss_function='categorical_crossentropy'
	))

	# Show the weights
	# net.show_weights(net.num_hidden_layers + 1)

	# Train the network
	# returns history of training process, and a callback object that can
	# extract information about the model at the end of events ANN_callbacks.py
	history, callback = net.train(
		trainx,
		trainy,
		num_iter=100,
		test_ratio=0.34,
		batch=100,
		interactive=False
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

if samples >= valx.shape[0]:
	samples = valx.shape[0]
	print('Too bad... you wanted too many samples. Using the max:\t{}'.format(samples))
	input('Press enter to continue...')

print('\n')

total_score = {
	'iterations': 0,
	'sum': 0
}

def predict(sample_index=0, sample=song_result_interface.result.copy(), interactive=False):
	# ignore these commands back end's job
	total_score['iterations'] = total_score['iterations'] + 1
	X = pd.DataFrame([np.array(valx[sample_index].copy())])
	sample['X'] = X.values
	sample['top_genre'] = decode(valy[sample_index])
	#####

	# ML & Al job, just updates sample['prediction']
	sample = net.predict(sample)

	# ignore this
	total_score['sum'] = sample['prediction']['score'] + total_score['sum']
	######

	# showing results
	if interactive:
		print('\n\n')
		prediction = sample['prediction']
		genres = prediction['genres']
		score = prediction['score']
		answer = sample['top_genre']
		result = prediction['result']

		print('Title:\t{}'.format(sample['title']))
		print('Artist:\t{}'.format(sample['metadata']['artist']))
		print('Answer:\t{0}\nResult:\t{1}'.format(answer, result))
		print('Score : {0}/{1}\t{2}'.format(score, 16, score/16))
		counter = 1
		for genre in genres:
			if counter <= 8:
				print('{0}\t {1}:\t{2:.4f}'.format(counter, genre, genres[genre]))
			counter = counter +  1
		input('Press enter to continue...')
	return sample

results = []

for index in range(0, samples):
	if samples <= 8 and samples >= 1:
		results.append(predict(index, interactive=True))
	else:
		results.append(predict(index, interactive=False))

tot_score = total_score['sum'] / (16*total_score['iterations'])

print('Total score:\t{}'.format(tot_score))

## Save the Model
# For the ML team: copy and paste this file and name it one word, <your name>
# ANN_<your name>.py
if MODEL_NAME == '':
	g = input("Save model? (y/n)\t") 
	if g == 'Y' or g == 'y':
		g = input('model name: ')
		net.save_to_disk(g)