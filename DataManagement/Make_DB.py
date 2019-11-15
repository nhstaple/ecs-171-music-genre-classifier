import numpy as numpy
import pandas as pd 
from sqlalchemy import create_engine
import sqlite3
conn = sqlite3.connect('features.db')
#new_conn = 
engine = create_engine("sqlite://", echo=False)

features_db = pd.read_csv('fma_metadata/features.csv')

column_names = []
for(columnName, columnData) in features_db.iteritems():
	s = columnData.values[0]
	d = columnData.values[1]
	
	type_feature = ''.join([i for i in s if not i.isdigit()])
	new_column_name = columnName  + type_feature+"." + d
	columnName = new_column_name
	column_names.append(columnName)

features_db.columns = column_names

features_db = features_db.rename(columns ={'featurestatistics.number': 'track_id'})
features_db = features_db.iloc[3:]
features_db.to_csv('updated_features.csv')

#features_db.to_sql('features', con = engine)
#print(engine.execute("SELECT * FROM features WHERE track_id == 2").fetchall())

