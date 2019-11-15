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

# Load the Data Management's interface
import sys
sys.path.append('../DataManagement/')
import CSVInterface

print('Initializing...')
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

# print(D['X']['small'].shape)
# print(D['X']['small'].head(5))
# print(D['Y']['small'].shape)
# print(D['Y']['small'].head(5))

# Show all the weights prior to training
# net.show_weights(net.num_hidden_layers + 1)

# The data after removing outliers
# data = outlier_method(RawData)

indepent_features = 'mfcc'
X =  pd.DataFrame(D['X']['small'][
		indepent_features]
	)
Y = pd.DataFrame(D['Y']['small'], columns=['genre_top'])

# Test and train split using encoded Y labels (vector of 0s with one 1)
trainx, testx, trainy, testy = train_test_split(
	X.values,
	encode(Y), # one hot encoder, see ANN_encode.py
	test_size=0.34,
	random_state=0
)

sample = trainx[0].copy()

print('\ntesting data')
print('testx element len')
print(len(sample))
print('testx len')
print(len(testx))
print('testy element len')
print(len(testy[0]))
print('testy len')
print(len(testy))
# print('test_set')
# print(test_set)

print('\n\nBuilding neural net')
print('input : {}'.format(len(sample)))
print('output: {}'.format(NUM_GENRES))
# paramterize if you want
# see ANN_parameters.py
net = ANN(p=Parameter(
	num_input=len(sample),
	num_hidden_layers=1,
	nodes_per_hidden=8,
	num_output=NUM_GENRES,
	hidden_activation='sigmoid',
	output_activation='sigmoid',
	initialize=False,
	learning_rate=10,
	loss_function='mean_squared_error'
))

# net.show_weights(net.num_hidden_layers + 1)

#config = net.model.layers[net.num_hidden_layers].get_config()
#print('L-1')
#print(config)
#print('\n\n')

#config = net.model.layers[net.num_hidden_layers-1].get_config()
#print('L-2')
#print(config)
#print('\n\n')


# Train the network
# returns history of training process, and a callback object that can extract information about the model at the end of events
history, callback = net.train(
	trainx,
	trainy,
	num_iter=1500,
	testing=(testx, np.array(testy)),
	batch=300
)

# for i in range(0, len(sample)):
# 	sample[i] = random.uniform(-100, 100)

result = net.predict(pd.DataFrame([sample]))
result.res['title'] = 'Dummy Title'
result.res['artist'] = 'Dummy Artist'
print(result.res['title'])
print(result.res['artist'])
for genre in result.res['prediction']:
	print("{0}: {1}".format(genre, result.res['prediction'][genre]))

print('\nActual Result:')
sample_category = trainy[0]
print(decode(sample_category))
# net.save_to_disk('test_1')