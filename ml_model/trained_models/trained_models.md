# Trained Models

This directory holds all trained models. Trained models are stored on disk in two files:

* a) `<model name>_parameters.csv`

Hold all the hyperparameter values for the model. See `ANN_parameters.csv` for the interface of the csv file.

* b) `<model name>_weights.npy`

Holds the weights for the neural network with the specified parameters in its `_parameters.csv` file.

For example,

`test_parameters.csv`

`num_input, num_hidden_layers, noder_per_hidden, num_output, hidden_activation, output_activation, initialize, learning_rate, loss_function`

```
2,2,3,16,'sigmoid','softmax',False,10,'mean_squared_error'
```

# How to save a model

`ANN.save_to_disk(model_name='my_model')`

This saves the following files to disk:

* `/ml_model/trained_models/my_model_parameters.csv`
* `/ml_model/trained_models/my_model_weights.npy`

# How to load a model _after_ it's saved to disk

`net = ANN(trained_model='my_model')`
