# ECS171 music genre classifier
This is a Music Genre Classifier built as a website for ECS 171 - Introduction to Machine Learning.
Users can enter in a song title and the result will be a predicted genre. 

## Installation for Local Machine:
+ **Required Libraries**
+ &nbsp;&nbsp;&nbsp;&nbsp;Keras ('pip3 install keras')
+ &nbsp;&nbsp;&nbsp;&nbsp;Tensorflow ('pip3 install tensorflow')
+ &nbsp;&nbsp;&nbsp;&nbsp;Pandas ('pip3 install pandas')
+ &nbsp;&nbsp;&nbsp;&nbsp;Flask ('pip3 install flask')
+ **Insert Instructions**
+ &nbsp;&nbsp;&nbsp;&nbsp;**Step 1:** download https://os.unil.cloud.switch.ch/fma/fma_metadata.zip
+ &nbsp;&nbsp;&nbsp;&nbsp;**Step 2:** Move all downloaded files to the Data directory
+ &nbsp;&nbsp;&nbsp;&nbsp;**Step 3:** Navigate to the Data_Management folder and run 'python3 Make_DB.py' and 'python3 makePick.py' in terminal
+ &nbsp;&nbsp;&nbsp;&nbsp;**Step 4:** Navigate to the backend folder and run 'python3 backend.py' (IMPORTANT: make sure you run it while you are in the Back_End folder or else it won't work)
+ &nbsp;&nbsp;&nbsp;&nbsp;**Step 5:** Open a new terminal tab and navigate to the Front_End folder and run 'npm install' and then 'npm start'

### Languages
+ **Front end programming languages:** JavaScript (ES6), HTML, CSS
+ **Back end programming languages:** Python (version >= 3)

### Front End
+ **Frameworks:** React
+ **Modules:** node.js, webpack, npm

### Back End
+ **Frameworks:** Flask
+ **NAME:** findOneSong(name, randomFlag)
+ **DESCRIPTION:** The function will take the song tiel as @name and the random pick sonf feature as @randomFlag from the url, which front-end triggers. Both @name and @randomFlag are string datatype. @name can be anything inside a string, but @randomFlag should be 'True' or 'False' only. The function will return a json message, which contaions one object 'error' only when there is no this song title in database or result with objects, 'songName','artist', 'songGenre', 'predictedScore', 'actualGenre, 'songScore', 'modelScore', 'error', when the song is in the database.
+ **EXAMPLES:** For example, 'http://localhost:8080/song/enter song/True', @name is 'enter song' and @randomFlag is 'True'

### Data Managment
+ [Data Overview](Data_Management/DataOverview.md)
+ [Data Format](Data_Management/dataCheck.ipynb)

### Machine Learning Group
+ **Model used:** insert what model we used
+ **Training:** how to train?
+ **Prediction:** how to predict?
+ **Metrics:**

+ **File: results.py **
+ **Libraries: None **
+ **NAME: Result (class) **
+ **SYNOPSIS:** Object returned by the trained model 
+ **DESCRIPTION:** The object consists of dictionary with title: str, artist: str, prediciton: dict. The prediction dictionary contains variables corresponding to the top 4 genres the song will be in with each variable being its probability of being that genre. 

+ **File: genres.py **
+ **Libraries: None **
+ **NAME: Genres (class) **
+ **SYNOPSIS:** Contains Genres of possible outputs 
+ **DESCRIPTION:** See Synopsis

+ **File: ANN_parameter.py **
+ **Libraries: Tensorflow, Numpy, Keras, genres **
+ **NAME: Parameters (class) **
+ **SYNOPSIS:** Contains object of parameters to feed to the model
+ **DESCRIPTION:** See synposis

+ **File: ANN_encode.py**
+ **Libraries: Tensorflow, Numpy, Keras, genres **
+ **NAME: encode(data, string=False)**
+ **SYNOPSIS:** Manual one hot encoder 
+ **DESCRIPTION:** Encodes datagrames dependent variables into a vector of zero's and one's 

+ **File: ANN_callback.py **
+ **Libraries: Tensorflow, Numpy, Keras, genres **
+ **NAME: class Callback(keras.callbacks.Callback)**
+ **SYNOPSIS:**  Call back function used to extract info from the model
+ **DESCRIPTION:** Call back function used to extract info from the model, returns stuff on beginning of training, end of training, epoch end and batch begin and end 

+ **File: ANN_callback.py
+ **Libraries: Tensorflow, Numpy, Keras, genres 
+ **NAME: class Callback(keras.callbacks.Callback):
+ **SYNOPSIS:**  Call back function used to extract info from the model
+ **DESCRIPTION:** Call back function used to extract info from the model, returns stuff on beginning of training, end of training, epoch end and batch begin and end 

+ **File: ANN_paramsweep.py **
+ **Libraries: Tensorflow, Numpy, Keras, pandasDB, song_result_interface, CSV_interface **
+ **NAME: make_and_train_model(h_layers, h_nodes) **
+ **SYNOPSIS:**  Makes model with specified parameters 
+ **DESCRIPTION:** This file script more generally takes in the data from the "database", make a model and run a grid sweep to get the best parameters. Also make plots of the models 

+ **File: ANN_class.py **
+ **Libraries: Tensorflow, Numpy, Keras **
+ **NAME: train(self, X, Y, num_iter=100, testing=(), batch=1, test_ratio=0.00, interactive=False) **
+ **SYNOPSIS:**  Trains the model 
+ **DESCRIPTION:** Trains the model based on the input given the parameters. Returns history and weights. Will validate if given input in test() otherwise will not. 

 **File: ANN_class.py **
+ **Libraries: Tensorflow, Numpy, Keras **
+ **NAME: train(self, X, Y, num_iter=100, testing=(), batch=1, test_ratio=0.00, interactive=False)**
+ **SYNOPSIS:**  Trains the model 
+ **DESCRIPTION:** Trains the model based on the input given the parameters. Returns history and weights. Will validate if given input in test() otherwise will not. 

 **File: ANN_class.py**
+ **Libraries: Tensorflow, Numpy, Keras**
+ **NAME: show_weights(self, num=1)**
+ **SYNOPSIS:** Prints weights of model 
+ **DESCRIPTION:** Refer to synopsis

 **File: ANN_class.py**
+ **Libraries: Tensorflow, Numpy, Keras**
+ **NAME: predict(self, sample)**
+ **SYNOPSIS:** Predicts based on sample 
+ **DESCRIPTION:** Assums model is trained, returns an instant of Result() from ANN_result.py

 **File: ANN_class.py**
+ **Libraries: Tensorflow, Numpy, Keras**
+ **NAME: get_mean_score(self)**
+ **SYNOPSIS:** Returns mean score of the model 
+ **DESCRIPTION:** Refer to synopsis

 **File: ANN_class.py**
+ **Libraries: Tensorflow, Numpy, Keras **
+ **NAME: get_features(self)**
+ **SYNOPSIS:** Returns features of self class 
+ **DESCRIPTION:** Refer to synopsis









