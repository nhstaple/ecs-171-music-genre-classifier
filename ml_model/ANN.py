import tensorflow as tf

#returns a 4 layers FFNN: 2 hidden layers with numNodes neurons and an output layer with numClasses neurons
def buildModel(numClasses, numNodes):
    # create a sequential model with 2 hidden layers with sigmoid activation and 3 neurons
    # the output layer uses sigmoid and numClasses nodes
    model = tf.keras.models.Sequential([
        tf.keras.layers.Dense(numNodes, activation='sigmoid', input_shape=(8,), use_bias=True),
        tf.keras.layers.Dense(numNodes, activation='sigmoid'),
        tf.keras.layers.Dense(numClasses, activation='sigmoid')
    ])

    # compile the model with Stochastic Gradient Descent, Mean Squared Error, and using accuracy to measure error
    model.compile(optimizer='SGD',
                  loss='mean_squared_error',
                  metrics=['accuracy'])

    return model