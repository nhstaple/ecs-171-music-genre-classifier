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
@app.route('/song/<string:name>/<string:randomFlag>/', methods=['GET'])
def findOneSong(name, randomFlag):
	# songList = [song for song in songArray if song == name]

	# for song in songArray:
	# 	if song == name:
	# 		return jsonify({'songGenre' : 'Dance'})

	error = False
	# get data from database
	if(randomFlag == 'True'):
		data = pandasDB.DataBase().query(name, True)
		sample = data['track_data']
		songName = data['track_data']['song_title'][0]
		actualGenre = data['track_data']['top_genre'][0]
		artist = data['track_data']['artist_name'][0]
	else:
		data = pandasDB.DataBase().query(name, False)
		print(data)
		if(not data['track_data']):
			error = True
		else:
			sample = data['track_data'][0]
			songName = data['track_data'][0]['song_title'][0]
			actualGenre = data['track_data'][0]['top_genre'][0]
			artist = data['track_data'][0]['artist_name'][0]
	
	# Data:
	# -track id
	# -song_title
	# -artist_name
	# -data
	# -top_genre
	# -set
	# -X
	if(error == False):
		#need to implement .selectN() to get N most influential featues for new models
		independent_features = ['mfcc', 'spectral_contrast']

		# neuralNet = ANN_class.ANN(trained_model='best')
		sample['prediction'] = {}
		sample['X'] = sample['X'][independent_features]
		sample = neuralNet.predict(sample)

		predictedGenre = sample['prediction']['result']

	# send ML results to front end

	if(error == True):
		return jsonify({
			'error' : error
		})
	else:
		return jsonify({
			'songName' : songName,
			'artist' : artist,
			'songGenre' : predictedGenre,
			'predictedScore' : str(sample['prediction']['genres'][predictedGenre]*100),
			'actualGenre' : actualGenre,
			'actualScore' : str(sample['prediction']['genres'][actualGenre]*100),
			'modelScore' : str(neuralNet.get_mean_score()),
			'error' : error
		})

@app.route('/song', methods=['POST'])
def findOneSong2():
	for song in songArray:
		if song == request.json['name']:
			return jsonify({'songGenre' : 'Dance'})

	return jsonify({'songGenre' : 'I do not find it.'})



if __name__ == '__main__':
	neuralNet = ANN_class.ANN(trained_model='best')
	app.run(debug=True, port=8080) #run app on port 8080 in debug mode