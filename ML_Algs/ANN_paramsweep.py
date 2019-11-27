# ANN_paramsweep.py
# author - matt

#import packages
import sys
sys.path.append('../Back_End/')
sys.path.append('../Data_Management/')

import pandasDB
import song_result_interface
import CSVInterface

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

#set the features we're going to use
indepent_features = ['mfcc', 'spectral_contrast']

# set your experiment seed for train test split
EXPERIMENT_SEED = 42
VALIDATION_PERCENT = 0.1
DEFAULT_H_ACTIVATION = 'relu'
DEFAULT_O_ACTIVATION = 'softmax'
DEFAULT_LOSS = 'categorical_crossentropy'
DEFAULT_BATCH = 200
DEFAULT_EPOCHS = 200
TEST_RATIO = 0.34
DATA_SET = 'cleanLarge'

# Process Data
# Load Data
print('Initializing Data Management interface...')
# reads the data from the csv
reader = CSVInterface.featRead()

DB = pandasDB.DataBase()

# D = { X | Y }
# D[X][Y]
D = {}
# X
D['X'] = {
    'cleanLarge': reader.getSubset(
        reader.getFrame('features'),
        sub='cleanLarge'
    )
}

# Y
D['Y'] = {
    'cleanLarge': reader.getSubset(
        reader.getFrame('track')['genre_top'],
        sub='cleanLarge'
    ),
}

# get the features
indepent_features = ['mfcc', 'spectral_contrast']

print('Constructing datasets')
print('X')
# the ind vars
X = pd.DataFrame(D['X'][DATA_SET][indepent_features])

print('Y')
# the dependent var
Y = pd.DataFrame(D['Y'][DATA_SET], columns=['genre_top'])

print('train/validation split')
# Test and train split using encoded Y labels (vector of 0s with one 1)
trainx, valx, trainy, valy = train_test_split(
    X.values,
    encode(Y),  # one hot encoder, see ANN_encode.py
    test_size=VALIDATION_PERCENT,  # validation size
    random_state=EXPERIMENT_SEED
)

#pull a sample to get the number of features
sample = trainx[0].copy()

print('Data done!\n\n********')

# Build the neural network
print('\nBuilding neural net')
print('input : {}'.format(len(sample)))
print('output: {}\n'.format(NUM_GENRES))

net = 0
history = 0
callback = 0

#a function that create a model with the given number of
#hiddenlayers and nodes per layer
def make_model(h_layers, h_nodes):
    # create an ANN with specified parameters
    net = ANN(p=Parameter(
        num_input=len(sample),
        num_hidden_layers=h_layers,
        nodes_per_hidden=h_nodes,
        num_output=NUM_GENRES,
        hidden_activation=DEFAULT_H_ACTIVATION,
        output_activation=DEFAULT_O_ACTIVATION,
        initialize=False,
        loss_function=DEFAULT_LOSS,
        features=indepent_features
    ))
    return net

#set up the parameters we want to sweep over
layers = [1,2,3,4,5,6]
nodes = [4,8,16,32]
minScore = 16
#number of samples to predict on
samples = 500

# create a grid to store parameter sweep scores in
grid_vect = np.empty([len(layers), len(nodes)])

# grid search for num of hidden layers and num of hidden nodes per layer
for num_layers in layers:
    for num_nodes in nodes:

        # make the model
        model = make_model(num_layers, num_nodes)
        # Train the network
        # returns history of training process, and a callback object that can
        # extract information about the model at the end of events ANN_callbacks.py
        history, callback = model.train(
            trainx,
            trainy,
            num_iter=DEFAULT_EPOCHS,
            test_ratio=TEST_RATIO,
            batch=DEFAULT_BATCH,
            interactive=False
        )

        print("\nLayers: {0}\nNodes: {1}".format(num_layers, num_nodes))

        # Predicting
        # Let's see how accurate the model is according to the mean score
        print("\nRunning predictions on {} samples.".format(samples))
        #for each sample
        for index in range(0, samples):
            #calculate the genre prediction vector
	        song = DB.query()['track_data']
	        song['X'] = song['X'][indepent_features].values
	        model.predict(song)

        #after running predictions, print out the mean score achieved
        print(model.get_mean_score())

        #add this model's score to the grid
        grid_vect[layers.index(num_layers)][nodes.index(num_nodes)] = model.get_mean_score()

        #if this model is the best, save it
        if(model.get_mean_score() < minScore):
            minScore = model.get_mean_score()
            model.save_to_disk("paramsweep_model")
        
        #plot of training/testing accuracy and error over time
        training_accuracy = []
        testing_accuracy = []
        training_error = []
        testing_error = []

        #build the lists to be plotted
        for x in history.history['val_categorical_accuracy']:
            testing_accuracy.append(x)
        for x in history.history['categorical_accuracy']:
            training_accuracy.append(x)
        for x in history.history['val_loss']:
            testing_error.append(x)
        for x in history.history['loss']:
            training_error.append(x)

        #plot the training/testing accuracy
        plt.figure(1)
        plt.plot(training_accuracy, label = "training accuracy")
        plt.plot(testing_accuracy, label = "testing accuracy")
        plt.xlabel("epoch")
        plt.ylabel("categorical accuracy")
        plt.title("categorical accuracy vs epoch on {}".format(DATA_SET))
        plt.legend()

        #plot the training/testing error
        plt.figure(2)
        plt.plot(training_error, label = "training error")
        plt.plot(testing_error, label = "testing error")
        plt.xlabel("epoch")
        plt.ylabel("error")
        plt.title("error vs epoch on {}".format(DATA_SET))
        plt.legend()
        #save the error plots to disk
        plt.savefig("../Figures/Parameter_Sweep/{0}x{1}_error.png".format(num_layers, num_nodes))
        plt.clf()

#create a dataframe from the grid to better display it
grid = pd.DataFrame(grid_vect, index=layers, columns=nodes)
#print the grid of mean scores for each model
print(grid)
