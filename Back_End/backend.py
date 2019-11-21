from flask import Flask, jsonify, request #import objects from the Flask model
import sys, os
import pandas as pd
sys.path.append(os.path.abspath(os.path.join('..', 'Data_Management'))) #path to Data_Management folder
sys.path.append(os.path.abspath(os.path.join('..', 'ML_Algs'))) #path to ML_Algs folder
import pandasDB
import ANN_class
app = Flask(__name__) #define app using Flask

# reference to https://www.youtube.com/watch?v=qH--M56OsUg
# songArray is the example, which is like a data base
songArray = ["one", "two","three"]

# Homepage, which is for testing. It uses url: http://localhost:8080
@app.route('/', methods=['GET'])
def test():
	return jsonify({'songGenre' : 'It works!'})


# use url: http://localhost:8080/song/songName, 
# which the songName is the song title and can be changed
@app.route('/song/<string:name>', methods=['GET'])
def findOneSong(name):
	# songList = [song for song in songArray if song == name]

	# for song in songArray:
	# 	if song == name:
	# 		return jsonify({'songGenre' : 'Dance'})


	# get data from database
	randomFlag = False

	data = pandasDB.DataBase().query(name, randomFlag)
	sample = data['track_data'][0]

	# Data:
	# -track id
	# -song_title
	# -artist_name
	# -data
	# -top_genre
	# -set
	# -X

	#send data to ML
	neuralNet = ANN_class.ANN(trained_model='best')

	indepent_features = ['mfcc', 'spectral_contrast']

	total_score = {
		'iterations': 0,
		'sum': 0
	}
	total_score['iterations'] = total_score['iterations'] + 1
	
	sample['prediction'] = {}
	sample['X'] = sample['X'][['mfcc', 'spectral_contrast']]
	sample = neuralNet.predict(sample)

	total_score['sum'] = sample['prediction']['score'] + total_score['sum']

	predictedGenre = sample['prediction']['result']
	actualGenre = data['track_data'][0]['top_genre'][0]

	# send ML results to front end

	return jsonify({

		'songName' : name,
		'artist' : data['track_data'][0]['artist_name'][0],
		'songGenre' : predictedGenre,
		'predictedScore' : str(sample['prediction']['genres'][predictedGenre]),
		'actualGenre' : actualGenre,
		'actualScore' : str(sample['prediction']['genres'][actualGenre]),
		'modelScore' : 'Score: ' + str(total_score['sum'])
	})

@app.route('/song', methods=['POST'])
def findOneSong2():
	for song in songArray:
		if song == request.json['name']:
			return jsonify({'songGenre' : 'Dance'})

	return jsonify({'songGenre' : 'I do not find it.'})



if __name__ == '__main__':
	app.run(debug=True, port=8080) #run app on port 8080 in debug mode