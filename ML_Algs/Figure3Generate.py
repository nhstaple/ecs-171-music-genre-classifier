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

# return data containing training accuracy per epoch
def getHistory(data_set_size):    
    # set your experiment seed for train test split
    EXPERIMENT_SEED = 42
    FEATURE_COUNT = 200
    VALIDATION_PERCENT = 0.1
    DEFAULT_LAYERS = 1
    DEFAULT_NODES = len(classes) + 1
    DEFAULT_H_ACTIVATION = 'relu'
    DEFAULT_O_ACTIVATION = 'softmax'
    DEFAULT_LOSS = 'categorical_crossentropy'
    DEFAULT_BATCH = 200
    DEFAULT_EPOCHS = 200
    TEST_RATIO = 0.34
    DATA_SET = data_set_size
    
    # use the best model
    MODEL_NAME = 'matt'

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

    D = {}
    D['X'] =  {
        'small'	: reader.getSubset(
                    reader.getFrame('features'),
                    sub='small'
                ),
        'medium': reader.getSubset(
                    reader.getFrame('features'),
                    sub='medium'
                ),
        'cleanLarge' : reader.getSubset(
                    reader.getFrame('features'),
                    sub='cleanLarge'
                )
    }

    D['Y'] = {
        'small'	: reader.getSubset(
            reader.getFrame('track')['genre_top'],
            sub='small'
        ),
        'medium': reader.getSubset(
            reader.getFrame('track')['genre_top'],
            sub='medium'
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
    trainx, testx, trainy, testy = train_test_split(
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

    net = 0
    history = 0
    callback = 0

    # Use this for pre trained models
    net = ANN(p=Parameter(
        num_input=len(sample),
        num_hidden_layers=1,
        nodes_per_hidden=len(sample) + 1,
        num_output=NUM_GENRES,
        hidden_activation=DEFAULT_H_ACTIVATION,
        output_activation=DEFAULT_O_ACTIVATION,
        initialize=False,
        loss_function=DEFAULT_LOSS,
        features = indepent_features
    ))


    # Show the weights
    # net.show_weights(net.num_hidden_layers + 1)

    # Train the network
    # returns history of training process, and a callback object that can
    # extract information about the model at the end of events ANN_callbacks.py
    h, callback = net.train(
        trainx,
        trainy,
        num_iter=DEFAULT_EPOCHS,
        testing=(testx, np.array(testy)),
        batch=DEFAULT_BATCH,
        interactive=False
    )
    
    return h

#get training accuracy over time for clean large, medium, and small
cleanLargeHistoryList = getHistory('cleanLarge')
mediumHistoryList = getHistory('medium')
smallHistoryList = getHistory('small')

large_training_error = []
for x in cleanLargeHistoryList.history['categorical_accuracy']:
    large_training_error.append(x)
    
large_testing_error = []
for y in cleanLargeHistoryList.history['val_categorical_accuracy']:
    large_testing_error.append(y)

medium_training_error = []
for x in mediumHistoryList.history['categorical_accuracy']:
    medium_training_error.append(x)
    
medium_testing_error = []
for y in mediumHistoryList.history['val_categorical_accuracy']:
    medium_testing_error.append(y)
    
small_training_error = []
for x in smallHistoryList.history['categorical_accuracy']:
    small_training_error.append(x)
    
small_testing_error = []
for y in smallHistoryList.history['val_categorical_accuracy']:
    small_testing_error.append(y)
    

#Plot figure
fig = plt.figure(figsize=(8, 6))
fig.set_size_inches(18.5, 10.5)
fig.subplots_adjust(hspace=0.3)

# Clean Large subplot
plt.subplot(2, 2, 1)
plt.plot(large_training_error, label = "training accuracy")
plt.plot(large_testing_error, label = "testing accuracy")
plt.xlabel("epoch")
plt.ylabel("accuracy")
plt.title("accuracy vs epoch on clean Large")

# Medium subplot
plt.subplot(2, 2, 2)
plt.plot(medium_training_error, label = "training accuracy")
plt.plot(medium_testing_error, label = "testing accuracy")
plt.xlabel("epoch")
plt.ylabel("accuracy")
plt.title("accuracy vs epoch on medium")

# Small subplot
plt.subplot(2, 2, 3)
plt.plot(small_training_error, label = "training accuracy")
plt.plot(small_testing_error, label = "testing accuracy")
plt.xlabel("epoch")
plt.ylabel("accuracy")
plt.title("accuracy vs epoch on small")

plt.legend()

plt.show() 