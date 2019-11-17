import pandas as pd
import numpy as np
from sklearn.neighbors import LocalOutlierFactor
import tensorflow as tf
from tensorflow import keras
import matplotlib.pyplot as plt


#Loads Data
def load_data():
    file_path = "C:/Users/kevin/Classes/ECS171/HW2/yeast.data"
    raw_data = pd.read_csv(file_path, names = ["Sequence Name", "mcg", "gvh", "alm", "mit", "erl", "pox", "vac", "nuc", "class"], delim_whitespace = True)
    return raw_data


#Performs IsolationForest outlier detection on the numerical parts of the data and returns a list containing indices of outliers
def iso_forest(data):
    clf = IsolationForest(behaviour='new', contamination='auto')
    y_pred = clf.fit_predict(data)
    
    outlier_indices = []
    for i in range(0, len(y_pred)):
        if y_pred[i] == -1:
            outlier_indices.append(i)
            
    return outlier_indices


def load_and_remove_outliers():
    raw_data = load_data()
    outlier_data = raw_data[["mcg", "gvh", "alm", "mit", "erl", "pox", "vac", "nuc"]]
    lof_outliers = LOF(outlier_data)
    data = raw_data.drop(lof_outliers, axis=0)
    
    return data.reset_index(drop = True)


#Returns the training and testing features and labels
def train_test_set(data):
    #Randomize data
    data = data.sample(frac = 1, random_state = 21).reset_index(drop = True)
    
    #Split into 66% training, 33% testing
    train_set = data.iloc[0:980]
    test_set = data.iloc[981:1483]
    
    #Split into features and label
    train_x = train_set[["mcg", "gvh", "alm", "mit", "erl", "pox", "vac", "nuc"]]
    train_y = train_set[["class"]]
    test_x = test_set[["mcg", "gvh", "alm", "mit", "erl", "pox", "vac", "nuc"]]
    test_y = test_set[["class"]]
    
    return ((train_x, train_y), (test_x, test_y))


def build_model():
    model = keras.Sequential([
    keras.layers.Dense(3, activation='sigmoid', input_dim=8), #input layer - specify input nodes with "input_dim" parameter
    keras.layers.Dense(3, activation='sigmoid'), #hidden layer
    keras.layers.Dense(10, activation='sigmoid')]) #output layer - not actually sure about this one
    
    model.compile(loss='categorical_crossentropy',
              optimizer='adam',
              metrics=['accuracy'])
    
    return model


def classify():
    data = load_and_remove_outliers()
    (train_x, train_y), (test_x, test_y) = train_test_set(data)
    prob2_model = build_model()
    prob2_model.fit(train_x, train_y) #train model
    socre = prob2_model.evaluate(test_x, test_y) #test model
    
    
classify()