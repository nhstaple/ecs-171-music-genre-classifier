#Make_DB.py
#Author(s): Jatin Mohanty, Jose Torres-Vargas

#file was used when attempting to implement sqlite database. As sqlite wasn't used
#this file wasn't used.
#script formats csv file in order to later make a DB file.
import numpy as numpy
import pandas as pd 
from sqlalchemy import create_engine
import sqlite3
conn = sqlite3.connect('features.db')
#new_conn = 
engine = create_engine("sqlite://", echo=False)

features_db = pd.read_csv('../Data/features.csv', index_col = 0, header = [0,1,2])
tracks_db = pd.read_csv('../Data/tracks.csv', index_col = 0, header = [0,1])
#features_db = pd.read_pickle('features.pkl')
features_db.columns = [''.join(col).strip() for col in features_db.columns.values]
tracks_db.columns = [''.join(col).strip() for col in tracks_db.columns.values]
final_db = pd.merge(features_db, tracks_db[['trackgenre_top']], on = 'track_id', how = 'left')
#final_db.rename(index={0: "track_id"})

final_db.to_csv('make_db.csv')




