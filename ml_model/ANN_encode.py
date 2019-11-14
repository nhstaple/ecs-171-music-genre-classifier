# encode.py
# author - nick s.
## from hw2
## A onehotencoder

import numpy as np
from genres import classes

# TODO replace with the actual feature name that is the genre
dep = 'genre'

# decodes an encoding 
def decode(enc):
	for i in range (0, 10):
		if enc[i]:
			return classes[i]
	print("FATAL ERROR: a sample's class cannot be dencoded: {}".format(enc))
	exit()
	

# encodes the entire dataframe's dependent variable
# into a vector of zeros with one 1 indicating it's class
# membership
def encode(data, string=False):
	Y = []
	if string:
		encoding = np.zeros(10)
		for i in range(0, len(classes)):
			if data[dep] == classes[i]:
				encoding[i] = 1
				Y.append(encoding) ; break
			elif data[dep] not in classes:
				print("FATAL ERROR: a sample's class cannot be encoded: {}".format(sample[dep]))
				exit()
		return Y
	for _, sample in data.iterrows():
		encoding = np.zeros(10)
		for i in range(0, len(classes)):
			if sample[dep] == classes[i]:
				encoding[i] = 1
				Y.append(encoding) ; break
			elif sample[dep] not in classes:
				print("FATAL ERROR: a sample's class cannot be encoded: {}".format(sample[dep]))
				exit()
	return Y
