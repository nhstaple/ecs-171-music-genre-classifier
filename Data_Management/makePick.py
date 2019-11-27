#makePick.py
#Author(s): Jose Torres-Vargas

#Script should be run in Data folder. Converts necessary csv files
#to pickle files which allows for quicker read times of the files.
import pandas as pd 


print('trying to read tracks.csv')
try:
	tracks = pd.read_csv('../Data/tracks.csv', index_col=0, header=[0, 1])
	print('saving as tracks.pkl')
	tracks.to_pickle('../Data/tracks.pkl')
except:
	print('tracks conversion failed')



print('trying to read features.csv')
try:	
	features = pd.read_csv('../Data/features.csv', index_col=0, header=[0,1,2])
	print('saving as features.pkl')
	features.to_pickle('../Data/features.pkl')
except:
	print('features conversion failed')



print('trying to read echonest.csv')
try:
	echonest = pd.read_csv('../Data/echonest.csv', index_col=0, header=[0,1,2])
	print('saving as echonest.pkl')
	echonest.to_pickle('../Data/echonest.pkl')
except:
	print('echonest conversion failed!')


print('trying to read genres.csv')
try:
	genres = pd.read_csv('../Data/genres.csv', index_col=0)
	print('saving as genres.pkl')
	genres.to_pickle('../Data/genres.pkl')
except:
	print('genres conversion failed!')
