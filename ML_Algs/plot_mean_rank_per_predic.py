# ANN_example.py
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
FEATURE_COUNT = 200
VALIDATION_PERCENT = 0.1
DATA_SET = 'cleanLarge'


MODEL_NAME = input('Name of model to load: \t')

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

# Show all the weights prior to training
# net.show_weights(net.num_hidden_layers + 1)

# The data after removing outliers
# data = outlier_method(RawData)

#get the features
# indepent_features = reader.selectN(n=FEATURE_COUNT)
indepent_features = ['mfcc', 'spectral_contrast']

print('Constructing datasets')
print('X')
# the ind vars
# X =  pd.DataFrame(D['X'][DATA_SET].iloc[:, indepent_features])
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

samples = 0
# The number of test samples to check
samples = int(input('Begin prediction on test set.\nNumber of samples:\t'))

if samples > valx.shape[0]:
	samples = valx.shape[0]
	print('Too bad... you wanted too many samples. Using the max:\t{}'.format(samples))
	input('Press enter to continue...')

print('\n')

val_scores = []

def predict(sample=song_result_interface.result.copy(), interactive=False):
	# ML & Al job, just updates sample['prediction']
	sample = net.predict(sample)
	val_scores.append(sample['prediction']['score'])

	# showing results
	if interactive:
		print('\n\n')
		prediction = sample['prediction']
		genres = prediction['genres']
		score = prediction['score']
		answer = sample['top_genre']
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

results = []
avg_per_predic = []

#calculate the avg rank of all predictions every time a new prediction is made
for index in range(0, samples):
	song = DB.query()['track_data']
	song['X'] = song['X'][indepent_features].values
	# song['X'] = song['X'].iloc[:, indepent_features].values
	if samples <= 8 and samples >= 1:
		results.append(predict(sample=song, interactive=True))
	else:
		results.append(predict(sample=song, interactive=False))
	avg_per_predic.append(net.get_mean_score())

#print average per prediction
plt.plot(avg_per_predic, label = "average rank per prediction")
plt.xlabel("prediction")
plt.ylabel("average rank")
plt.title("average rank vs prediction on {}".format(DATA_SET))
plt.legend()

plt.show()