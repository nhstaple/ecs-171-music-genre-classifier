import pandas as pd 


print('trying to read tracks.csv')
try:
	tracks = pd.read_csv('tracks.csv', index_col=0, header=[0, 1])
	print('saving as tracks.pkl')
	tracks.to_pickle('tracks.pkl')
except:
	print('tracks conversion failed')



print('trying to read features.csv')
try:	
	features = pd.read_csv('features.csv', index_col=0, header=[0,1,2])
	print('saving as features.pkl')
	features.to_pickle('features.pkl')
except:
	print('features conversion failed')



print('trying to read echonest.csv')
try:
	echonest = pd.read_csv('echonest.csv', index_col=0, header=[0,1,2])
	print('saving as echonest.pkl')
	echonest.to_pickle('echonest.pkl')
except:
	print('echonest conversion failed!')


print('trying to read genres.csv')
try:
	genres = pd.read_csv('genres.csv', index_col=0)
	print('saving as genres.pkl')
	genres.to_pickle('genres.pkl')
except:
	print('genres conversion failed!')