#CSVInterface.py
#Author(s): Jose Torres-Vargas, Jatin Mohanty, Chance Stewart

import pandas as pd
import numpy as np
from sklearn.model_selection import KFold
from sklearn.feature_selection import SelectKBest
from sklearn.feature_selection import f_classif

#Interface that allows interaction with the data.
#Class featRead implements an objects that holds a dictionary with all of
#the data frames that might be needed.
#@pkls: list of file names(pkl) files that are to be read in.
class featRead:

	def __init__(self, pkls=['features.pkl', 'tracks.pkl', 'echonest.pkl', 'genres.pkl']):	
		self.tableDF = {}
		for key in pkls:
			if(key == 'features.pkl'):
				print('Reading features.pkl')
				features = pd.read_pickle('../Data/features.pkl')
				self.tableDF['features'] = features

			elif(key == 'tracks.pkl'):
				print('Reading tracks.pkl')
				tracks = pd.read_pickle('../Data/tracks.pkl')
				self.tableDF['tracks'] = tracks.copy()
				self.tableDF['album'] = tracks['album'].copy()
				self.tableDF['track'] = tracks['track'].copy()
				self.tableDF['artist'] = tracks['artist'].copy()
				self.tableDF['set'] = tracks['set'].copy()

			elif(key == 'echonest.pkl'):
				print('Reading echonest.pkl')
				echonest = pd.read_pickle('../Data/echonest.pkl')
				echo_audio_feat = echonest.iloc[:, echonest.columns.get_level_values(1) == 'audio_features'].copy()
				echo_meta_data = echonest.iloc[:, echonest.columns.get_level_values(1) == 'metadata'].copy()
				echo_social_feat = echonest.iloc[:, echonest.columns.get_level_values(1) == 'social_features'].copy()
				self.tableDF['echo_audio_feat'] = echo_audio_feat
				self.tableDF['echo_meta_data'] = echo_meta_data
				self.tableDF['echo_social_feat'] = echo_social_feat


			elif(key == 'genres.pkl'):
				print('Reading genres.pkl')
				genres = pd.read_pickle('../Data/genres.pkl')
				self.tableDF['genres'] = genres
			else:
				print(key + ' is not a vaild file name')
				break

	#lists all of the data frames names contained by the featRead object
	def listFrames(self):
		for key in self.tableDF:
			print(key)

	#return a certain data fram 
	#@frame: string name of frame
	def getFrame(self, frame):
		return self.tableDF[frame]

	#return a subset of statistics from a specific feature
	#@feature: feature categories can be found in the DataOverview.md
	#@stat: list of stats you want from the feature category
	def getFeatures(self, feature='chroma_cens', stat=['mean', 'std']):
		df = self.tableDF['features'].copy()
		df = df[feature]
		return df[stat]

	#return the data subset 'small', 'medium', 'large'
	#@frame: frame that subset will be obtained from
	#@sub: string that specifies which subset
	#default is small subset
	def getSubset(self, frame, sub='small'):
		setDF = self.tableDF['set']

		if(sub == 'small'):
			subset = setDF
			subset = subset.loc[subset['subset'] == sub]
			newDF = frame[frame.index.isin(subset.index)].copy()
			return newDF

		elif(sub == 'medium'):
			subset = setDF
			subset = subset.loc[(subset['subset'] == sub) | (subset['subset'] == 'small')]
			newDF = frame[frame.index.isin(subset.index)].copy()
			return newDF

		elif(sub == 'large'):
			subset = setDF
			subset = subset.loc[(subset['subset'] == sub) | (subset['subset'] == 'medium') | (subset['subset'] == 'small')]
			newDF = frame[frame.index.isin(subset.index)].copy()
			return newDF
		elif(sub == 'cleanLarge'):
			genres = self.tableDF['track']
			genres = genres['genre_top']
			#full set genre_top not complete
			genres = genres.dropna()

			newDF = frame[frame.index.isin(genres.index)].copy()
			return newDF

		else:
			print('Not a vaild set type')

	#KFold function
	#input
	#@frame: data frame
	#@k: integer, number of splits
	#output
	#df_collection: returns a collection of data frames in pairs of training/testing splits
	def makeKfold(self, frame, k):
		kf = KFold(n_splits=k, shuffle=False)
		df_collection = {}
		i = 0
		for train_index, test_index in kf.split(frame):
			df_collection[i,"training"] = frame.iloc[train_index]
			df_collection[i,"testing"] = frame.iloc[test_index]
			i += 1
		return df_collection

	#can be used after getFeatures() method to merge dataframes of different
	#feature category.
	#@f1: frame on the left
	#@f2: frame on the right
	#return: returns combined dataframe
	def mergeFrames(self, f1, f2):
		combined = pd.merge(f1, f2, on='track_id', how='outer')
		return combined

	#returns a random sample from the small subset by default.
	#subset: subset from which random sample will be obtained
	def getRandomSong(self, subset='small'):
		tracks = self.tableDF['tracks']
		tracks = self.getSubset(tracks, subset)
		track = tracks['track']
		features = self.tableDF['features']

		titles = track[['title']]
		song = titles.sample()
		song = song.to_dict()
		song = song['title']

		for key in song:
			s = tracks.loc[key]
			songTitle = s[[('track', 'title')]].values
			artistName = s[[('artist', 'name')]].values
			date = s[[('track', 'date_created')]].values
			top_g = s[[('track', 'genre_top')]].values
			subset = s[[('set', 'subset')]].values

			d = {}
			d['track_id'] = key
			d['song_title'] = songTitle
			d['artist_name'] = artistName
			d['date'] = date
			d['genre_top'] = top_g
			d['set'] = subset

			print(top_g)

			feat = features.loc[[key],:]

		ret = {}
		ret['track_data'] = d
		ret['features'] = feat
		
		return ret

	#selectN - univariate feature selection
	#finds the column indices for a specificed number of top scoring features
	#calculated using univariate selection with the f_classif scoring function
	#input
	#@n: number of features to calculate
	#output
	#@indices: column indeces for the selected features
	def selectN(self, n = 50):
		#set up dataframes
		featureData = self.getSubset(self.getFrame('features'), sub='cleanLarge')
		genreData = self.getSubset(self.getFrame('track')['genre_top'], sub='cleanLarge')
		Xdf = pd.DataFrame(featureData)
		Ydf = pd.DataFrame(genreData)

		#create class for selectKbest with f_classif and n results
		bestfeatures = SelectKBest(score_func=f_classif, k=n)
		#select features and put into dataframe
		fit = bestfeatures.fit(Xdf, np.ravel(Ydf))
		dfscores = pd.DataFrame(fit.scores_)

		#get column indices
		indices = dfscores.nlargest(n, 0).index
		return indices

	#selectmRMR - minimum Redundancy Maximum Relevancy Feature Selection
	#finds the column indices for up to 200 of the top scoring features calculated
	#using mRMR Feature Selection (calculated with an executable file, see 
	#FeatureSelect.ipbn for details)
	#input
	#@n: number of features to be returned 
	#output
	#@indices: column indeces of the selected features
	def selectmRMR(self, n = 50):
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
		if(n > 200):
			print("mRMR is not computed for the number of features you asked for. Using max: 200")
			n = 200
		return indices[0:n]



		
