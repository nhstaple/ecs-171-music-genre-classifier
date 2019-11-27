#SQL_query.py
#Author(s):Jatin Mohanty

#First attempt at implementing a data base using sql. Implementation
#was too slow so we opted to using a data frame instead.

import sqlite3
import numpy as numpy
import pandas as pd 


def get_features(track_id, features, stats):
	connection = sqlite3.connect('features_with_genre.db')
	cursor = connection.cursor()
	feature_list = []
	for feature in features:
		for stat in stats:
			feature_list.append(feature+stat)
	
	query = "PRAGMA table_info(my_table)"
	cursor.execute(query)
	results = cursor.fetchall()
	mylist = []
	for feature in feature_list:
		mylength = len(feature)
		for i in range(0,519):
			full_string = results[i][1]
			string_match = full_string[:mylength]
			if(feature == string_match):
				mylist.append(full_string)
			

	
	feature_select = ", ".join(mylist)
	query2 = "SELECT " + feature_select+"  FROM my_table WHERE track_id = " + str(track_id) +";"
	cursor.execute(query2)
	results = cursor.fetchall()
	
	cursor.close()
	connection.close()
	return results
    # return results[0][0]
mylist = ["chroma_cens", "chroma_cens"]
stats = ["kurtosis", "max"]

print(get_features(2, mylist, stats))




