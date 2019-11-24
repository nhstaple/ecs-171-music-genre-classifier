###Test the small dataset using an SVM


import sys
sys.path.append('../Data_Management/')
import CSVInterface
import pandas as pd
import numpy as np
from sklearn.svm import SVC
from sklearn.metrics import classification_report, confusion_matrix

#Maps genre to ints
GENRE_MAP = {
	'Experimental' : 0,
	'Electronic' : 1,
	'Rock' : 2,
	'Instrumental' : 3,
	'Pop' : 4,
	'Folk' : 5,
	'Hip-Hop' : 6,
	'International' : 7,
	'Jazz' : 8,
	'Classical' : 9,
	'Country' : 10,
	'Spoken' : 11,
	'Blues' : 12,
	'Soul-RnB' : 13,
	'Old-Time / Historic' : 14,
	'Easy Listening' : 15
}


def main():
	reader = CSVInterface.featRead()
	D = {}
	D['X'] =  {
	'small'	: reader.getSubset(
				reader.getFrame('features'),
				sub='small'),
	'cleanLarge' : reader.getSubset(
				reader.getFrame('features'),
				sub='cleanLarge')}

	D['Y'] = {
	'small'	: reader.getSubset(
		reader.getFrame('track')['genre_top'],
		sub='small'),
	'cleanLarge': reader.getSubset(
		reader.getFrame('track')['genre_top'],
		sub='cleanLarge'),}

	X = D['X']['small']['mfcc'][['mean', 'std']]

	#Convert genres to the numbers - needs to be a list
	Y = pd.DataFrame(D['Y']['small'], columns=['genre_top']).to_numpy()
	Y_labels = []
	for genre in Y:
		Y_labels.append(GENRE_MAP[genre[0]])

	#Split into test and train sets. Note that SVM is hella slow so more samples takes forever
	X_train = X.iloc[0:1000]
	X_test = X.iloc[7000:8001]
	Y_train = Y_labels[0:1000]
	Y_test =  Y_labels[7000:8001]
	
	#Train
	svclassifier = SVC(kernel='linear', decision_function_shape='ovo')
	svclassifier.fit(X_train, Y_train)

	Y_pred = svclassifier.predict(X_test)

	#Print evaluations
	print(confusion_matrix(Y_test,Y_pred))
	print(classification_report(Y_test,Y_pred))

if __name__ == '__main__':
	main()