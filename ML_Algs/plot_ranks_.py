# plot_ranks_.py

import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
import numpy as np
import pandas as pd
from genres import classes, NUM_GENRES
from ANN_parameter import Parameter
from ANN_result import Result
from ANN_class import ANN
from ANN_encode import encode, decode
import random

# set your experiment seed for train test split
EXPERIMENT_SEED = 42
VALIDATION_PERCENT = 0.1
DATA_SET = 'cleanLarge'

#get input for loaded model
MODEL_NAME = 'optimal_param_sweep'
#second model can be loaded to create a plot comparing both models
MODEL_NAME_2 = 'matt'

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

print('Data done!\n\n********')

# Use this for pre trained models

net = ANN(trained_model=MODEL_NAME)
if(MODEL_NAME_2 != ''):
	net2 = ANN(trained_model=MODEL_NAME_2)

samples = 0
# The number of test samples to check
samples = 1000

print('\n')

val_scores = []
val_scores2 = []
naive = []

#calculate the avg rank of all predictions every time a new prediction is made
for index in range(0, samples):
	song = DB.query()['track_data']
	song['X'] = song['X'][indepent_features].values
	song = net.predict(song)
	val_scores.append(song['prediction']['score'])
	
	if MODEL_NAME_2 != '':
		song = net2.predict(song)
		val_scores2.append(song['prediction']['score'])
	
	song = net.naive_predict(song)
	naive.append(song['prediction']['score'])

#print average per prediction
plt.plot(val_scores, label = "model 1")
if MODEL_NAME_2 != '':
	plt.plot(val_scores2, label = "model 2")
plt.plot(naive, label='naive model')
plt.xlabel("prediction")
plt.ylabel("rank")
plt.title("rank of predictions on {}".format(DATA_SET))
plt.legend()

plt.show()