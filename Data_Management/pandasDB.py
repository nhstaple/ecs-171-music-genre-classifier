import pandas as pd 



class DataBase:

	#Constructor creates df's that are needed.
	#Assumes that pkl files are in thee same directory
	def __init__(self, pkls=['/Data/tracks.pkl', '/Data/features.pkl']):
		self.tables = {}
		for pkl in pkls:
			if(pkl == '/Data/tracks.pkl'):
				key = 'tracks'
			else:
				key = 'features'

			try:
				self.tables[key] = pd.read_pickle('../'+pkl)
			except:
				print('File ' + '../'+pkl + ' was not found!')


	def getSubset(self, frame, sub='small'):
			tracks = self.tables['tracks']
			setDF = tracks['set']

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
				genres = tracks['track']
				genres = genres['genre_top']
				#full set genre_top not complete
				genres = genres.dropna()

				newDF = frame[frame.index.isin(genres.index)].copy()
				return newDF

			else:
				print('Not a vaild set type')

	def getRandomSong(self, subset='medium'):
		tracks = self.tables['tracks']
		tracks = self.getSubset(tracks, subset)
		track = tracks['track']
		features = self.tables['features']

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
			d['X'] = feat

		ret = {}
		ret['track_data'] = d
		#ret['features'] = feat
		
		return ret


	def query(self, songTitle, randomFlag):

		if(randomFlag == True):
			return self.getRandomSong()

		tracks = self.tables['tracks']
		track = tracks['track']
		features = self.tables['features']

		#string matches all done in lower case
		titles = track[['title']]
		titles = titles['title'].str.lower()
		titles = titles.to_frame()
		titles = self.getSubset(titles, 'cleanLarge')

		#get querey hits as a dictionary
		res = titles.loc[titles['title'] == songTitle.lower()]
		results = res.to_dict()
		results = results['title']

		#need a list since there might be mulitple songs with same name
		ans = []
		featList = []

		#building dictionary of metadata
		for key in results:
			song = tracks.loc[key]
			songTitle = song[[('track', 'title')]].values
			artistName = song[[('artist', 'name')]].values
			date = song[[('track', 'date_created')]].values
			top_g = song[[('track', 'genre_top')]].values
			subset = song[[('set', 'subset')]].values

			d = {}
			d['track_id'] = key
			d['song_title'] = songTitle
			d['artist_name'] = artistName
			d['date'] = date
			d['top_genre'] = top_g
			d['set'] = subset
			d['X'] = features.loc[[key],:]
			ans.append(d)
			#featList.append(key)

		#feat = features.loc[featList, :]
		ret = {}
		ret['track_data'] = ans
		#ret['features'] = feat

		return ret


