
import pandas as pd
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

	
	def listFrames(self):
		for key in self.tableDF:
			print(key)

	def getFrame(self, frame):
		return self.tableDF[frame]

	def getFeatures(self, feature=['chroma_cens'], stat=['mean', 'std']):
		df = self.tableDF['features'].copy()
		for i in feature:
			feat = df[i]


