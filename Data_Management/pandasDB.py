#pandasDB.py
#Author(s): Jose Torres-Vargas

import pandas as pd 


#The "DataBase" that is used by the back-end when querying songs
#and obtaining features.
class DataBase:

	#Constructor creates df's that are needed.
	#Assumes that pkl files are in thee same directory
	#reducedFeat.pkl is a cleaned up version of features.pkl
	#unlabeled samples(rows) were dropped.
	#unused features(columns) were dropped
	def __init__(self, pkls=['/Data/tracks.pkl', '/Data/reducedFeat.pkl']):
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

    	#Returns a subset of specified frame
        #@frame: frame which we want subset from
        #@sub: string specifyin subset
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
                                #CleanLarge simply drops those samples that don't have a label i.e. genre_top
				newDF = frame[frame.index.isin(genres.index)].copy()
				return newDF

			else:
				print('Not a vaild set type')

        #Returns a dictionary containing inforamtion of a random song.
        #@subset: from which subset do you want to select a ranom song.
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
			d['genre_top'] = top_g
			d['set'] = subset
			feat = features.loc[[key],:]
			d['X'] = pd.DataFrame(feat)

		ret = {}
		ret['track_data'] = d
		
		return ret

        #Retruns list of dictionaries with song information of songs that were found in "DB".
        #@songTitle: name of song to search for
        #@randomFlag: Boolean. If true then title is ignored and random song is selected instead
	def query(self, songTitle='', randomFlag=True):

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
			d['genre_top'] = top_g
			d['set'] = subset
			d['X'] = pd.DataFrame(features.loc[[key],:])
			#print('dataframe\n{}'.format(d['X']))
			ans.append(d)
			#featList.append(key)

		#feat = features.loc[featList, :]
		ret = {}
		ret['track_data'] = ans
		#ret['features'] = feat

		return ret



