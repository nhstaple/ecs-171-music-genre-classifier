
import pandas as pd
from sklearn.model_selection import KFold

# import sys
# sys.path.append('../')

class featRead:

	def __init__(self, pkls=['features.pkl', 'tracks.pkl', 'echonest.pkl', 'genres.pkl']):	
		self.tableDF = {}
		for key in pkls:
			if(key == 'features.pkl'):
				print('Reading features.pkl')
				features = pd.read_pickle('../features.pkl')
				self.tableDF['features'] = features

			elif(key == 'tracks.pkl'):
				print('Reading tracks.pkl')
				tracks = pd.read_pickle('../tracks.pkl')
				self.tableDF['tracks'] = tracks.copy()
				self.tableDF['album'] = tracks['album'].copy()
				self.tableDF['track'] = tracks['track'].copy()
				self.tableDF['artist'] = tracks['artist'].copy()
				self.tableDF['set'] = tracks['set'].copy()

			elif(key == 'echonest.pkl'):
				print('Reading echonest.pkl')
				echonest = pd.read_pickle('../echonest.pkl')
				echo_audio_feat = echonest.iloc[:, echonest.columns.get_level_values(1) == 'audio_features'].copy()
				echo_meta_data = echonest.iloc[:, echonest.columns.get_level_values(1) == 'metadata'].copy()
				echo_social_feat = echonest.iloc[:, echonest.columns.get_level_values(1) == 'social_features'].copy()
				self.tableDF['echo_audio_feat'] = echo_audio_feat
				self.tableDF['echo_meta_data'] = echo_meta_data
				self.tableDF['echo_social_feat'] = echo_social_feat


			elif(key == 'genres.pkl'):
				print('Reading genres.pkl')
				genres = pd.read_pickle('../genres.pkl')
				self.tableDF['genres'] = genres
			else:
				print(key + ' is not a vaild file name')
				break;

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
	#@frame: data frame
	#@k: integer, number of splits
	#return: returns a collection of data frames
	def makeKfold(self, frame, k):
		kf = KFold(n_splits=k, shuffle=True)
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
			d['top_genre'] = top_g
			d['set'] = subset

			feat = features.loc[[key],:]

		ret = {}
		ret['track_data'] = d
		ret['features'] = feat
		
		return ret