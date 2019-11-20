import pandas as pd 


class DataBase:

	#Constructor creates df's that are needed.
	#Assumes that pkl files are in thee same directory
	def __init__(self, pkls=['tracks.pkl', 'features.pkl']):
		self.tables = {}

		for pkl in pkls:
			if(pkl == 'tracks.pkl'):
				key = 'tracks'
			else:
				key = 'features'

			try:
				self.tables[key] = pd.read_pickle(pkl)
			except:
				print('File ' + pkl + ' was not found!')

	def query(self, songTitle):
		tracks = self.tables['tracks']
		track = tracks['track']
		features = self.tables['features']

		#string matches all done in lower case
		titles = track[['title']]
		titles = titles['title'].str.lower()
		titles = titles.to_frame()

		#get querey hits as a dictionary
		res = titles.loc[titles['title'] == songTitle]
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
			ans.append(d)
			featList.append(key)

		feat = features.loc[featList, :]
		ret = {}
		ret['track_data'] = ans
		ret['features'] = feat

		return ret




