# ANN_example.py
# author(s) - matt, chance, nick
## Description
## This file loads a trained network that's stored in ML_algs/trained_models. If a model
## isn't loaded, then this script will create a model specified by the default parameters.
## After a trained model is in memory predictions will be made on the model. To see detailed
## information about predictions enter a small sample size.
## A histogram will display the 

import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from tensorflow.keras.metrics import categorical_accuracy
import numpy as np
import pandas as pd
from genres import classes, NUM_GENRES
from ANN_parameter import Parameter
from ANN_class import ANN
from ANN_encode import encode, decode
import random
from scipy.stats import sem, t
from scipy import mean

# set your experiment seed for train test split
# These parameters correspond to the parameters used for Matt's model.
EXPERIMENT_SEED = 42
VALIDATION_PERCENT = 0.1
# num of hidden layers
DEFAULT_LAYERS = 1
# num of nodes per layer
DEFAULT_NODES = 189 + 1
# activation function
DEFAULT_H_ACTIVATION = 'relu'
# output function
DEFAULT_O_ACTIVATION = 'softmax'
# loss metric
DEFAULT_LOSS = 'categorical_crossentropy'
# batch size
DEFAULT_BATCH = 200
# num of training epochs
DEFAULT_EPOCHS = 100
TEST_RATIO = 0.34
# data set for training
DATA_SET = 'cleanLarge'
# num features for mrmr
FEATURE_COUNT = 200
MRMR = False

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
import pandasDB

print('Initializing Data Management interface...')
# reads the data from the csv
reader = CSVInterface.featRead()

# Data manegement interface
DB = pandasDB.DataBase()

# D = { X | Y }
# D[X][Y]
D = {}
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

#get the features
indepent_features = ['mfcc', 'spectral_contrast']

print('Constructing datasets')
print('X')
# the ind vars
X =  pd.DataFrame(D['X'][DATA_SET][indepent_features])

print('Y')
# the dependent var
Y = pd.DataFrame(D['Y'][DATA_SET], columns=['genre_top'])

print('train/validation split')
# Test and train split using encoded Y labels (vector of 0s with one 1)
trainx, valx, trainy, valy = train_test_split(
	X.values,
	encode(Y), # one hot encoder, see ANN_encode.py
	test_size=VALIDATION_PERCENT,	# validation size
	random_state=EXPERIMENT_SEED
)

sample = trainx[0].copy()

print('Data done!\n\n********')

## Build the neural network
print('\nBuilding neural net')
print('input : {}'.format(len(sample)))
print('output: {}\n'.format(NUM_GENRES))

# the neural network
net = 0
# the history object from training
history = 0
# the callback function from training
callback = 0

# Use this for pre trained models
if MODEL_NAME != '':
	net = ANN(trained_model=MODEL_NAME)
else:
	# Use this to test your own architecture
	net = ANN(p=Parameter(
		num_input=len(sample),
		num_hidden_layers=DEFAULT_LAYERS,
		nodes_per_hidden=DEFAULT_NODES,
		num_output=NUM_GENRES,
		hidden_activation=DEFAULT_H_ACTIVATION,
		output_activation=DEFAULT_O_ACTIVATION,
		initialize=False,
		loss_function=DEFAULT_LOSS,
		features = indepent_features
	))

	# Train the network
	# returns history of training process, and a callback object that can
	# extract information about the model at the end of events ANN_callbacks.py
	history, callback = net.train(
		trainx,
		trainy,
		num_iter=DEFAULT_EPOCHS,
		test_ratio=TEST_RATIO,
		batch=DEFAULT_BATCH,
		interactive=False
	)

# The number of test samples to check
samples = int(input('Begin prediction on test set. <= 8 samples will run in interactive mode.\nNumber of samples:\t'))

# Check if user input is within array bounds
if samples > valx.shape[0]:
	samples = valx.shape[0]
	print('Too bad... you wanted too many samples. Using the max:\t{}'.format(samples))
	input('Press enter to continue...')

print('\n')

val_scores = []
val_accuracy = []

# wrapper to do a prediction on the neural network
# input
## sample: the song sample from the back end pipeline
## interactive: bool to display information interactively
# output
## sample: the song sample with a modified 'prediction' field
def predict(sample, interactive=False):
	# ML & Al job, just updates sample['prediction']
	sample = net.predict(sample)
	val_scores.append(sample['prediction']['score'])
	#accuracy = 1 iff score ==1, else = 0
	if(sample['prediction']['score'] == 1):
		val_accuracy.append(1)
	else:
		val_accuracy.append(0)
	# showing results
	if interactive:
		print('\n\n')
		prediction = sample['prediction']
		genres = prediction['genres']
		score = prediction['score']
		answer = sample['genre_top']
		result = prediction['result']

		print('Title:\t{}'.format(sample['song_title']))
		print('Artist:\t{}'.format(sample['artist_name']))
		print('Answer:\t{0}\nResult:\t{1}'.format(answer, result))
		print('Score : {0}/{1}\t{2}'.format(score, 16, score/16))
		counter = 1
		for genre in genres:
			if counter <= 8:
				print('{0}\t {1}:\t{2:.4f}'.format(counter, genre, genres[genre]))
			counter = counter +  1
		input('Press enter to continue...')
	return sample

for index in range(0, samples):
	# Get a random song
	song = DB.query()['track_data']
	# Select the features for the model
	if MRMR:
		song['X'] = song['X'].iloc[:, indepent_features].values
	else:
		song['X'] = song['X'][indepent_features].values
	if samples <= 8 and samples >= 1:
		song = predict(sample=song, interactive=True)
	else:
		song = predict(sample=song, interactive=False)

#calculate the mean accuracy where
#accuracy = 1 iff genre_top == 1st prediction genre, else = 0
totalAcc = 0
for value in val_accuracy:
	totalAcc += value
meanAcc = totalAcc/len(val_accuracy)
print("Mean Accuracy: {}\n", meanAcc)
print('Average Rank of Actual Genre:\t{}',net.get_mean_score())

#histogram of validation scores
n_bins = 16

plt.hist(val_scores, bins=n_bins)
plt.title('Histogram of ranks on {}'.format(DATA_SET))

plt.show()

#confidence interval
confidence = 0.95
n = len(val_scores)
m = mean(val_scores)
std_err = sem(val_scores)
h = std_err * t.ppf((1 + confidence) / 2, n - 1)

start = m - h
end = m + h

print("95% Confidence Interval: {0} to {1}".format(start, end))

if(MODEL_NAME == ''):
	#plot of training accuracy over time
	training_error = []
	testing_error = []
	for x in history.history['val_categorical_accuracy']:
		testing_error.append(x)

	for x in history.history['categorical_accuracy']:
		training_error.append(x)

	plt.plot(training_error, label = "training accuracy")
	plt.plot(testing_error, label = "testing accuracy")
	plt.xlabel("epoch")
	plt.ylabel("accuracy")
	plt.title("accuracy vs epoch on {}".format(DATA_SET))
	plt.legend()

	plt.show()


## Save the Model
# For the ML team: copy and paste this file and name it one word, <your name>
# ANN_<your name>.py
if MODEL_NAME == '':
	g = input("Save model? (y/n)\t") 
	if g == 'Y' or g == 'y':
		g = input('model name: ')
		net.save_to_disk(g)
	elif g == "N" or g == 'n':
		print("Discarded Model")