# ANN_result.py

class Result:
	interface = {
		'title': '',
		'artist': '',
		'prediction': {
			'Genre A': 1,
			'Genre B': 0.5,
			'Genre D': 0.25,
			'Genre E': 0.00
		}
		# added additional items like recommended songs
		# 'recommended songs': [ ID, ID, ... ]
		# 'similar artists': [ ID, ID, ... ]
	}

	def __init__(
		self,
		title='Layla',
		artist='Eric Clapton',
		prediction={
			'Genre 5': 0.64,
			'Genre 3': 0.34,
			'Genre 6': 0.12,
			'Genre 4': 0.05
		}):

		self.res = self.interface.copy()
		self.res['title'] = title
		self.res['artist'] = artist
		self.res['prediction'] = prediction


test = False
if test:
	result = Result()
	print(result.res)