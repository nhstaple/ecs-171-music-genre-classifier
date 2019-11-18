import pandas as pd 

print('Reading tracks.csv')
tracks = pd.read_csv('tracks.csv', index_col=0, header=[0, 1])
print('saving as tracks.pkl')
tracks.to_pickle('tracks.pkl')

print('Reading features.csv')
features = pd.read_csv('features.csv', index_col=0, header=[0,1,2])
print('saving as features.pkl')
features.to_pickle('features.pkl')