# plot_mean_rank_per_predic.py
# authors: Chance Stewart
# based on code written in ANN_example.py

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
MODEL_NAME = input('Name of model to load: \t')
#second model can be loaded to create a plot comparing both models
g = input("Load second model for comparison? (y/n)\t") 
MODEL_NAME_2 = ''
if g == 'y' or g == 'Y':
	MODEL_NAME_2 = input('Name of second model: \t')
elif g == 'n' or g == 'n':
	print('Plotting 1 model')

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

sample = trainx[0].copy()

print('Data done!\n\n********')

net = 0
history = 0
callback = 0

# Use this for pre trained models

net = ANN(trained_model=MODEL_NAME)
if(MODEL_NAME_2 != ''):
	net2 = ANN(trained_model=MODEL_NAME_2)

samples = 0
# The number of test samples to check
samples = int(input('Begin prediction on test set.\nNumber of samples:\t'))

if samples > valx.shape[0]:
	samples = valx.shape[0]
	print('Too bad... you wanted too many samples. Using the max:\t{}'.format(samples))
	input('Press enter to continue...')

print('\n')

val_scores = []
val_scores2 = []

def predict(pred_model, score_arr, sample=song_result_interface.result.copy()):
	# ML & Al job, just updates sample['prediction']
	sample = pred_model.predict(sample)
	score_arr.append(sample['prediction']['score'])

	#return results
	return sample

results = []
results2 = []
avg_per_predic = []
avg_per_predic2 = []

#calculate the avg rank of all predictions every time a new prediction is made
for index in range(0, samples):
	song = DB.query()['track_data']
	song['X'] = song['X'][indepent_features].values
	results.append(predict(pred_model=net, score_arr=val_scores, sample=song))
	avg_per_predic.append(net.get_mean_score())
	if(MODEL_NAME_2 != ''):
		results2.append(predict(pred_model=net2, score_arr=val_scores2, sample=song))
		avg_per_predic2.append(net2.get_mean_score())

#print average per prediction
plt.plot(avg_per_predic, label = "model 1")
if(MODEL_NAME_2 != ''):
	plt.plot(avg_per_predic2, label = "model 2")
plt.xlabel("prediction")
plt.ylabel("average rank")
plt.title("average rank vs prediction on {}".format(DATA_SET))
plt.legend()

plt.show()