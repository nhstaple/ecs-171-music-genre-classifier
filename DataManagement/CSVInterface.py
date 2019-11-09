
import pandas as pd
from sklearn.model_selection import KFold


class featRead:

	def __init__(self, csvs=['features.csv', 'tracks.csv', 'echonest.csv', 'genres.csv']):	
		self.tableDF = {}
		for key in csvs:
			if(key == 'features.csv'):
				features = pd.read_csv('features.csv', index_col=0, header=[0,1,2])
				self.tableDF['features'] = features

			elif(key == 'tracks.csv'):
				tracks = pd.read_csv('tracks.csv', index_col=0, header=[0, 1])
				self.tableDF['album'] = tracks['album'].copy()
				self.tableDF['track'] = tracks['track'].copy()
				self.tableDF['artist'] = tracks['artist'].copy()
				self.tableDF['set'] = tracks['set'].copy()

			elif(key == 'echonest.csv'):
				echonest = pd.read_csv('echonest.csv', index_col=0, header=[0, 1, 2])
				echo_audio_feat = echonest.iloc[:, echonest.columns.get_level_values(1) == 'audio_features'].copy()
				echo_meta_data = echonest.iloc[:, echonest.columns.get_level_values(1) == 'metadata'].copy()
				echo_social_feat = echonest.iloc[:, echonest.columns.get_level_values(1) == 'social_features'].copy()
				self.tableDF['echo_audio_feat'] = echo_audio_feat
				self.tableDF['echo_meta_data'] = echo_meta_data
				self.tableDF['echo_social_feat'] = echo_social_feat


			elif(key == 'genres.csv'):
				genres = pd.read_csv('genres.csv', index_col=0)
				self.tableDF['genres'] = genres
			else:
				print(key + ' is not a vaild csv file name')
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



