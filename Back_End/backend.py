#backend.py
#Authors: Spencer Grossarth, Jiahui Dai, Luc Nglankong
from flask import Flask, jsonify, request, render_template #import objects from the Flask model
import sys, os
import pandas as pd
sys.path.append(os.path.abspath(os.path.join('..', 'Data_Management'))) #path to Data_Management folder
sys.path.append(os.path.abspath(os.path.join('..', 'ML_Algs'))) #path to ML_Algs folder
import pandasDB
import ANN_class
#define app using Flask, and specifiy what static pages to load
app = Flask(__name__, static_folder="../Front_End/build/", template_folder="../Front_End/build/")

# Homepage of website
@app.route("/")
def index():
    return render_template("index.html")

# FUNCTION: findOneSong
# DESCRIPTION: Backend pipeline that retrieves input from the front end,
# retrieves data from the database, predicts a song genre from the neural network
# given the output from the database, and sends the results to the front end.
# PARAMETER 1: @name (string datatypes) is the song title that the user 
# enters in the front end. @name can be anything inside a string.
# PARAMETER 2: @randomFlag (string datatypes) is the feature flag that 
# ignores the user input and picks a random song from the database. 
# @randomFlag should be 'True' or 'False' only.
@app.route('/song/<string:name>/<string:randomFlag>/', methods=['GET'])
def findOneSong(name, randomFlag):

	# initialize error message
	error = False

	# get data from database
	if(randomFlag == 'True'): # if "Feeling Lucky" or "Random Song" was pressed
		data = database.query(name, True)
		sample = data['track_data']
		songName = data['track_data']['song_title'][0]
		actualGenre = data['track_data']['genre_top'][0]
		artist = data['track_data']['artist_name'][0]
	else: # if "Search" button was pressed
		data = database.query(name, False)
		# if there is no this song title, query return a empty list call 'track_data'
		if(not data['track_data']):
			error = True
		else:
			sample = data['track_data'][0]
			songName = data['track_data'][0]['song_title'][0]
			actualGenre = data['track_data'][0]['genre_top'][0]
			artist = data['track_data'][0]['artist_name'][0]

	# when error == False, query found the input song title. otherwise, skip below because data is empty
	if(error == False):
		sample['prediction'] = {}
		sample = neuralNet.predict(sample)

		predictedGenre = sample['prediction']['result']

	# send ML results to front end
	if(error == False):

		# construct youtube url
		url = 'https://www.youtube.com' + '/results?'
		artistURl = artist
		query = 'search_query=' + songName + '+' + artist
		redirect_link = url + query
		redirect_link = redirect_link.replace(' ', '+')

		return jsonify({
			'songName' : songName,
			'artist' : artist,
			'songGenre' : predictedGenre,
			'predictedScore' : str(sample['prediction']['genres'][predictedGenre]*100),
			'actualGenre' : actualGenre,
			'actualScore' : str(sample['prediction']['genres'][actualGenre]*100),
			'songScore' : str(sample['prediction']['score']),
			'modelScore' : str(neuralNet.get_mean_score()),
			'error' : error,
			'redirect_link' : redirect_link,
			'predictionVector': str(sample['prediction']['genres'])
		})
	else:
		return jsonify({
			'error' : error
		})

if __name__ == '__main__':
	# create the database upon startup
	database = pandasDB.DataBase()

	# create the neural network upon startup
	neuralNet = ANN_class.ANN(trained_model='matt')

	app.run(debug=True, port=8080, host='0.0.0.0') #run app on port 8080 in debug mode
