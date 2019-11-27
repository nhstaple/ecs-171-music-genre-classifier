# Machine Learning

## results.py 
### Libraries:** None  

#### NAME: Result (class) 
+ **SYNOPSIS:** Object returned by the trained model 
+ **DESCRIPTION:** The object consists of dictionary with title: str, artist: str, prediciton: dict. The prediction dictionary contains variables corresponding to the top 4 genres the song will be in with each variable being its probability of being that genre. 

## genres.py 
### Libraries: None 

#### NAME: Genres (class) 
+ **SYNOPSIS:** Contains Genres of possible outputs 
+ **DESCRIPTION:** See Synopsis <br /> <br />

## ANN_parameter.py 
### Libraries: Tensorflow, Numpy, Keras, genres 

#### NAME: Parameters (class) 
+ **SYNOPSIS:** Contains object of parameters to feed to the model
+ **DESCRIPTION:** See synposis <br /> <br />

## ANN_encode.py
### Libraries: Tensorflow, Numpy, Keras, genres 

#### NAME: encode(data, string=False)
+ **SYNOPSIS:** Manual one hot encoder 
+ **DESCRIPTION:** Encodes dataframe of dependent variables into a vector of zero's and one's in order to properly conduct classification in a quantitative matter.  <br /> <br />

## ANN_callback.py 
### Libraries:** Tensorflow, Numpy, Keras, genres 

#### NAME: class Callback(keras.callbacks.Callback)
+ **SYNOPSIS:**  Call back function used to extract info from the model
+ **DESCRIPTION:** Call back function used to extract information from the model, returns information on beginning of training, end of training, epoch end and batch begin and end <br /> <br />

#### NAME: class Callback(keras.callbacks.Callback):
+ **SYNOPSIS:**  Call back function used to extract info from the model
+ **DESCRIPTION:** Call back function used to extract info from the model, returns stuff on beginning of training, end of training, epoch end and batch begin and end <br /> <br />

## ANN_paramsweep.py 
### Libraries: Tensorflow, Numpy, Keras, pandasDB, song_result_interface, CSV_interface 

#### NAME: make_and_train_model(h_layers, h_nodes) 
+ **SYNOPSIS:**  Makes model with specified parameters 
+ **DESCRIPTION:** This file script more generally takes in the data from the "database", make a model and run a grid search to get the best parameters. It also make plots of the models <br /> <br />

## ANN_class.py 
### Libraries: Tensorflow, Numpy, Keras 

#### NAME: train(self, X, Y, num_iter=100, testing=(), batch=1, test_ratio=0.00, interactive=False) 
+ **SYNOPSIS:**  Trains the model 
+ **DESCRIPTION:** Trains the model based on the input given the parameters. Returns history and weights. Will validate if given input in test() otherwise will not. <br /> <br />

#### NAME: train(self, X, Y, num_iter=100, testing=(), batch=1, test_ratio=0.00, interactive=False)
+ **SYNOPSIS:**  Trains the model 
+ **DESCRIPTION:** Trains the model based on the input given the parameters. Returns history and weights. Will validate if given input in test() otherwise will not. <br /> <br />

#### NAME: show_weights(self, num=1)
+ **SYNOPSIS:** Prints weights of model 
+ **DESCRIPTION:** Refer to synopsis <br /> <br />

#### NAME: predict(self, sample)
+ **SYNOPSIS:** Predicts based on sample 
+ **DESCRIPTION:** Assumes model is trained, returns an instant of Result() from ANN_result.py <br /> <br />

#### NAME: get_mean_score(self)
+ **SYNOPSIS:** Returns mean score of the model
+ **DESCRIPTION:** Can only be used if model is trained and predicted so there is a score to get the mean of. <br /> <br />

#### NAME: get_features(self)
+ **SYNOPSIS:** Returns features of class 
+ **DESCRIPTION:** Refer to synopsis <br /> <br />

#### NAME: naive_predict(self, sample, num_predictions=16)
+ **SYNOPSIS:** Uniform prediction of a model
+ **DESCRIPTION:** Prediction that guess uniformly instead of calling predict function on the neural network <br /> <br />

##### Example code
Loading a trained network
```
from ANN_class import ANN

# load a model from disc in folder './trained_models'
trained_net = ANN(model_name='name')
```

Creating a new untrained network
```
from ANN_class import ANN, Parameter
from ANN_encode import encode
import numpy as np


# create a new network parameterized by a ANN_parameter.Parameter() object
untrained_net=ANN(p=Parameter())
X = dataframe.drop(columns=['dependent variable']).values
Y = encode(dataframe['dependent variable])

```
