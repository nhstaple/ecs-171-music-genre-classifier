#binInterface.py
#Author(s): Jose Torres-Vargas
import pandas as pd
import numpy as np
from sklearn.model_selection import KFold
from sklearn.feature_selection import SelectKBest
from sklearn.feature_selection import f_classif

class featRead:

	def __init__(self, pkls=['features.pkl', 'tracks.pkl', 'echonest.pkl', 'genres.pkl']):	
		self.tableDF = {}
		for key in pkls:
			if(key == 'features.pkl'):
				print('Reading features.pkl')
				features = pd.read_pickle('../Data/reducedFeat.pkl')
				self.tableDF['features'] = features

			elif(key == 'tracks.pkl'):
				print('Reading tracks.pkl')
				tracks = pd.read_pickle('../Data/tracks.pkl')
				self.tableDF['tracks'] = tracks.copy()
				self.tableDF['album'] = tracks['album'].copy()
				self.tableDF['track'] = tracks['track'].copy()
				self.tableDF['artist'] = tracks['artist'].copy()
				self.tableDF['set'] = tracks['set'].copy()

			elif(key == 'genres.pkl'):
				print('Reading genres.pkl')
				genres = pd.read_pickle('../Data/genres.pkl')
				self.tableDF['genres'] = genres
			else:
				print(key + ' is not a vaild file name')
				break



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


	#returns a dictionary. Each entry, genre, contains a list of dictionaries which contain
	#samples of that genre which can then be fed into our model to make predicitons.
	#@subset: for which subset do you want the sorted bins for
	def getBins(self, subset):
        	#small subset contains only 8 genres
		if (subset == 'small'):
			med = self.getSubset(self.tableDF['tracks'], 'small')
			med = med['track']
			med_genres = list(med['genre_top'].unique())
		#medium and cleanLarge had 16 root genres
		else:
			med = self.getSubset(self.tableDF['tracks'], 'medium')
			med = med['track']
			#List containing our 16 bins
			med_genres = list(med['genre_top'].unique())

		#Sort entire clean dataset into bins
		genre_tops = self.getSubset(self.tableDF['tracks'], subset)
		genre_tops = genre_tops['track']
		genre_tops = genre_tops[['genre_top']]

		tracks = self.tableDF['tracks']
		features = self.tableDF['features']
		genreBins = {}
		for bins in med_genres:
			res = genre_tops.loc[genre_tops['genre_top'] == bins]
			results = res.to_dict()
			results = results['genre_top']

			ans = []

			for key in results:
				song = tracks.loc[key]
				top_g = bins

				d = {}
				d['track_id'] = key
				d['genre_top'] = bins
				d['X'] = pd.DataFrame(features.loc[[key],:]).values
				ans.append(d)


			genreBins[bins] = ans

		return genreBins

		
