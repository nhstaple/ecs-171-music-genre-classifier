###Test the small dataset using an SVM


import sys
sys.path.append('../Data_Management/')
import CSVInterface
import pandas as pd
import numpy as np
from sklearn.svm import SVC, LinearSVC
from sklearn.metrics import classification_report, confusion_matrix

#Maps genre to ints for classification
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

#indices of feature dataframe that MRMR analysis selected
indices = [435, 295, 412, 314, 312, 275, 437, 331,
384, 317, 515, 449, 323, 377, 354, 462, 450, 321,
509, 387, 272, 315, 294, 517, 461, 292, 430, 277,
508, 379, 174, 428, 411, 386, 325, 375, 319, 426,
208, 510, 281, 352, 297, 436, 311, 385, 451, 440,
330, 399, 431, 380, 507, 394, 229, 303, 318, 467,
388, 373, 415, 301, 285, 406, 355, 381, 444, 429,
250, 279, 206, 376, 358, 327, 173, 414, 398, 338,
460, 299, 383, 416, 198, 468, 506, 438, 287, 196,
433, 445, 389, 335, 305, 278, 212, 382, 172, 395,
404, 427, 344, 310, 211, 231, 390, 329, 274, 204,
372, 458, 397, 214, 505, 166, 336, 293, 169, 378,
320, 209, 514, 343, 328, 356, 391, 471, 159, 205,
441, 234, 307, 497, 464, 290, 207, 276, 403, 459,
176, 283, 333, 238, 288, 175, 194, 452, 324, 442,
232, 434, 465, 298, 210, 254, 228, 472, 309, 362,
213, 496, 171, 405, 448, 286, 340, 401, 193, 291,
280, 302, 233, 454, 243, 308, 423, 253, 164, 170,
215, 443, 511, 199, 289, 313, 339, 230, 200, 488,
498, 282, 304, 392, 479, 334, 195, 402, 75, 410,
177, 192]


def main():
	reader = CSVInterface.featRead() #Init interface to the CSV data
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

	#Choose which set of features to use
	#X = D['X']['small']['spectral_contrast'][['mean', 'std']] #only spectral contrast features
	X = D['X']['small']['mfcc'][['mean', 'std']] #only mfcc features
	
	#dat1 = D['X']['small']['mfcc'][['mean', 'std']] #for mfcc and spectral
	#dat2 = D['X']['small']['spectral_contrast'][['mean', 'std']] #for mfcc and spectral
	#X = pd.concat([dat1, dat2], axis=1) #append mfcc and spectral
	#X = D['X']['small'].iloc[:, indices] #For top 200 mrmr features
	X = X.sample(frac=1, random_state=21).reset_index(drop=True) #Randomize


	#Convert genres to the numbers - needs to be a list
	Y = pd.DataFrame(D['Y']['small'], columns=['genre_top'])
	Y = Y.sample(frac=1, random_state=21).reset_index(drop=True) #Randomize, seed must be same as X
	Y = Y.to_numpy()

	#Transform labels to numbers
	Y_labels = []
	for genre in Y:
		Y_labels.append(GENRE_MAP[genre[0]])

	#Split into test and train sets. Note that SVM is slow for ovo so more samples takes forever
	X_train = X.iloc[0:1500]
	X_test = X.iloc[1500:8001]
	Y_train = Y_labels[0:1500]
	Y_test =  Y_labels[1500:8001]
	
	print("Before train")
	#Train
	svclassifier = SVC(kernel='linear', decision_function_shape='ovo') #change to ovr if wanted
	svclassifier.fit(X_train, Y_train)

	print("Before prediction")
	Y_pred = svclassifier.predict(X_test)

	#Print evaluations
	print(confusion_matrix(Y_test,Y_pred))
	print(classification_report(Y_test,Y_pred))

if __name__ == '__main__':
	main()