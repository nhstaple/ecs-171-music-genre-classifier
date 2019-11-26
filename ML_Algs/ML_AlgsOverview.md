# Machine Learning
+ **Model used:** Feed forward neural net with one hidden layer and 190 active nodes. Softmax 
+ **Training:** 
+ **Prediction:** 
+ **Metrics:**

## File: results.py 
### Libraries:** None  

#### NAME: Result (class) 
+ **SYNOPSIS:** Object returned by the trained model 
+ **DESCRIPTION:** The object consists of dictionary with title: str, artist: str, prediciton: dict. The prediction dictionary contains variables corresponding to the top 4 genres the song will be in with each variable being its probability of being that genre. 

## File: genres.py 
### Libraries: None 

#### NAME: Genres (class) 
+ **SYNOPSIS:** Contains Genres of possible outputs 
+ **DESCRIPTION:** See Synopsis

## File: ANN_parameter.py 
### Libraries: Tensorflow, Numpy, Keras, genres 

#### NAME: Parameters (class) 
+ **SYNOPSIS:** Contains object of parameters to feed to the model
+ **DESCRIPTION:** See synposis

## File: ANN_encode.py
### Libraries: Tensorflow, Numpy, Keras, genres 

#### NAME: encode(data, string=False)
+ **SYNOPSIS:** Manual one hot encoder 
+ **DESCRIPTION:** Encodes datagrames dependent variables into a vector of zero's and one's 

## File: ANN_callback.py 
### Libraries:** Tensorflow, Numpy, Keras, genres 

#### NAME: class Callback(keras.callbacks.Callback)
+ **SYNOPSIS:**  Call back function used to extract info from the model
+ **DESCRIPTION:** Call back function used to extract info from the model, returns stuff on beginning of training, end of training, epoch end and batch begin and end 

#### NAME: class Callback(keras.callbacks.Callback):
+ **SYNOPSIS:**  Call back function used to extract info from the model
+ **DESCRIPTION:** Call back function used to extract info from the model, returns stuff on beginning of training, end of training, epoch end and batch begin and end 

## File: ANN_paramsweep.py 
### Libraries: Tensorflow, Numpy, Keras, pandasDB, song_result_interface, CSV_interface 

#### NAME: make_and_train_model(h_layers, h_nodes) 
+ **SYNOPSIS:**  Makes model with specified parameters 
+ **DESCRIPTION:** This file script more generally takes in the data from the "database", make a model and run a grid sweep to get the best parameters. Also make plots of the models 

## File: ANN_class.py 
### Libraries: Tensorflow, Numpy, Keras 

#### NAME: train(self, X, Y, num_iter=100, testing=(), batch=1, test_ratio=0.00, interactive=False) 
+ **SYNOPSIS:**  Trains the model 
+ **DESCRIPTION:** Trains the model based on the input given the parameters. Returns history and weights. Will validate if given input in test() otherwise will not. 

#### NAME: train(self, X, Y, num_iter=100, testing=(), batch=1, test_ratio=0.00, interactive=False)
+ **SYNOPSIS:**  Trains the model 
+ **DESCRIPTION:** Trains the model based on the input given the parameters. Returns history and weights. Will validate if given input in test() otherwise will not. 

#### NAME: show_weights(self, num=1)
+ **SYNOPSIS:** Prints weights of model 
+ **DESCRIPTION:** Refer to synopsis

#### NAME: predict(self, sample)
+ **SYNOPSIS:** Predicts based on sample 
+ **DESCRIPTION:** Assums model is trained, returns an instant of Result() from ANN_result.py

#### NAME: get_mean_score(self)
+ **SYNOPSIS:** Returns mean score of the model 
+ **DESCRIPTION:** Refer to synopsis

#### NAME: get_features(self)
+ **SYNOPSIS:** Returns features of self class 
+ **DESCRIPTION:** Refer to synopsis
