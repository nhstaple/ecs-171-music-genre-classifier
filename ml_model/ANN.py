import tensorflow as tf

def buildModel(numFeatures, numLayers, numNodes, actFunc, numClasses):
    model = tf.keras.models.Sequential()
    # add the first hidden layer
    model.add(tf.keras.layers.Dense(numNodes, activation=actFunc, input_dim=numFeatures))
    # add additional hidden layers as requested
    for x in range(numLayers-1):
        model.add(tf.keras.layers.Dense(numNodes, activation=actFunc))
    # add the output layer
    model.add(tf.keras.layers.Dense(numClasses, activation='softmax'))
    # compile the model with adam optimizer, categorical_crossentropy for multi-class classification
    # and using binary_accuracy to measure error
    model.compile(optimizer='adam',
                  loss='categorical_crossentropy',
                  metrics=['accuracy'])

    return model
