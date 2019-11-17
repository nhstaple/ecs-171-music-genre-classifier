import CSVInterface
import sys
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
indepent_features = 'mfcc'

# set your experiment seed for train test split
EXPERIMENT_SEED = 42
EPOCHS = 250
BATCH_SIZE = 100
SAMPLES_TO_PREDICT = 100
TOP_CAT_COUNT = 1

# Process Data
# Load the Data Management's interface
sys.path.append('../DataManagement/')

print('Initializing Data Management interface...')
# reads the data from the csv
reader = CSVInterface.featRead()

# D = { X | Y }
# D[X][Y]
D = {}
print('reading all features')
# X
D['X'] = {
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

print('Constructing datasets')
print('X')
# the ind vars
X = pd.DataFrame(D['X']['small'][
    indepent_features]
)

print('Y')
# the dependent var
Y = pd.DataFrame(D['Y']['small'], columns=['genre_top'])

print('train/test split')
# Test and train split using encoded Y labels (vector of 0s with one 1)
trainx, testx, trainy, testy = train_test_split(
    X.values,
    encode(Y),  # one hot encoder, see ANN_encode.py
    test_size=0.34,
    random_state=EXPERIMENT_SEED
)

sample = trainx[0].copy()
print('Data done!\n\n********')

# Build the neural network
print('\nBuilding neural net')
print('input : {}'.format(len(sample)))
print('output: {}\n'.format(NUM_GENRES))


def make_and_train_model(h_layers, h_nodes, h_activation, o_activation, loss):

    # create an ANN with specified parameters
    net = ANN(p=Parameter(
        num_input=len(sample),
        num_hidden_layers=h_layers,
        nodes_per_hidden=h_nodes,
        num_output=NUM_GENRES,
        hidden_activation=h_activation,
        output_activation=o_activation,
        initialize=False,
        loss_function=loss
    ))

    # Train the network
    # returns history of training process, and a callback object that can
    # extract information about the model at the end of events ANN_callbacks.py
    history, callback = net.train(
        trainx,
        trainy,
        num_iter=EPOCHS,
        testing=(testx, np.array(testy)),
        batch=BATCH_SIZE
    )
    print("\nMade and Trained model with {} layers and {} nodes".format(h_layers, h_nodes))
    return net


startLayers = int(input("Enter the starting # of layers: "))
endLayers = int(input("Enter the last # of layers: "))
startNodes = int(input("Enter the start # of nodes: "))
endNodes = int(input("Enter the end # of nodes: "))

#dataframe to hold results of grid search
grid_vect = np.empty([(endLayers-startLayers+1),(endNodes-startNodes+1)])
# grid search for num of hidden layers and num of hidden nodes per layer
for num_layers in range(startLayers,endLayers+1):
    for num_nodes in range(startNodes, endNodes+1):

        # make and train the model
        model = make_and_train_model(num_layers, num_nodes, "relu", "softmax", "categorical_crossentropy")

        print("\nLayers: {0}\nNodes: {1}".format(num_layers,num_nodes))
        # Predicting
        # Let's see how accurate the model is for the top @num_to_check many categories
        top_predictions = '\nResults\n'
        for num in range(1, TOP_CAT_COUNT+1):
            print('Computing top {}'.format(num))
            # keeps track of number of matches
            matches = 0
            for i in range(0, SAMPLES_TO_PREDICT):
                this_sample = np.array(testx[i].copy())
                this_sample = pd.DataFrame([this_sample], columns=X.columns)
                result = model.predict(this_sample.values)
                counter = 0
                sample_category = decode(testy[i])

                for genre in result.res['prediction']:
                    if genre == sample_category and counter < num:
                        matches = matches + 1
                    if counter >= num:
                        break
                    else:
                        counter = counter + 1
            top_predictions = top_predictions + \
                'Classification for top {0} predictions:\t{1}\n'.format(
                    num, matches / SAMPLES_TO_PREDICT)
        print(top_predictions)
        grid_vect[num_layers-startLayers][num_nodes-startNodes] = (matches / SAMPLES_TO_PREDICT)

grid = pd.DataFrame(grid_vect, index = range(startLayers,endLayers+1), columns = range(startNodes, endNodes+1))
print(grid)
