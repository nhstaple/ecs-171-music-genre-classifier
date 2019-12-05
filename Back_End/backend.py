#backend.py
#Authors: Spencer Grossarth, Jiahui Dai, Luc Nglankong
from flask import Flask, jsonify, request, render_template #import objects from the Flask model
import sys, os
import pandas as pd
sys.path.append(os.path.abspath(os.path.join('..', 'Data_Management'))) #path to Data_Management folder
sys.path.append(os.path.abspath(os.path.join('..', 'ML_Algs'))) #path to ML_Algs folder
import pandasDB
import ANN_class
import song_result_interface
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

	result_list = []

	# get data from database
	if(randomFlag == 'True'): # if "Feeling Lucky" or "Random Song" was pressed
		data = database.query(name, True)
		current_result = song_result_interface.result
		current_result['song_id'] = 0
		current_result['title'] = data['track_data']['song_title'][0]
		current_result['metadata']['artist'] = data['track_data']['artist_name'][0]
		current_result['genre_top'] = data['track_data']['genre_top'][0]
		current_result['subset'] = data['track_data']['set'][0]
		current_result['X'] = data['track_data']['X']
		result_list.append(current_result)
	else: # if "Search" button was pressed
		data = database.query(name, False)
		# if there is no this song title, query return a empty list call 'track_data'
		if(not data['track_data']):
			error = True
		else:
			# store all song name results from database
			for index in range(0, len(data['track_data'])):
				current_result = song_result_interface.result
				current_result['song_id'] = index
				current_result['title'] = data['track_data'][index]['song_title'][0]
				current_result['metadata']['artist'] = data['track_data'][index]['artist_name'][0]
				current_result['subset'] = data['track_data'][index]['set'][0]
				current_result['X'] = data['track_data'][index]['X']
				current_result['genre_top'] = data['track_data'][index]['genre_top'][0]
				result_list.append(current_result)

	# when error == False, query found the input song title. otherwise, skip below because data is empty
	if(error == False):
		result_list[0] = neuralNet.predict(result_list[0])

	# send ML results to front end
	if(error == False):

		actualGenre = result_list[0]['genre_top']
		predictedGenres = list(result_list[0]['prediction']['genres'].keys())
		predictedProbabilities = list(result_list[0]['prediction']['genres'].values())

		# construct youtube url
		url = 'https://www.youtube.com' + '/results?'
		artistURl = result_list[0]['metadata']['artist']
		query = 'search_query=' + result_list[0]['title'] + '+' + result_list[0]['metadata']['artist']
		redirect_link = url + query
		redirect_link = redirect_link.replace(' ', '+')

		return jsonify({
			'songName' : result_list[0]['title'],
			'artist' : result_list[0]['metadata']['artist'],
			'genre_rank_1' : predictedGenres[0],
			'genre_rank_2' : predictedGenres[1],
			'genre_rank_3' : predictedGenres[2],
			'genre_rank_4' : predictedGenres[3],
			'genre_rank_5' : predictedGenres[4],
			'genre_rank_6' : predictedGenres[5],
			'genre_rank_7' : predictedGenres[6],
			'genre_rank_8' : predictedGenres[7],
			'probability_rank_1' : str(round(predictedProbabilities[0]*100,4)),
			'probability_rank_2' : str(round(predictedProbabilities[1]*100,4)),
			'probability_rank_3' : str(round(predictedProbabilities[2]*100,4)),
			'probability_rank_4' : str(round(predictedProbabilities[3]*100,4)),
			'probability_rank_5' : str(round(predictedProbabilities[4]*100,4)),
			'probability_rank_6' : str(round(predictedProbabilities[5]*100,4)),
			'probability_rank_7' : str(round(predictedProbabilities[6]*100,4)),
			'probability_rank_8' : str(round(predictedProbabilities[7]*100,4)),
			'actualGenre' : actualGenre,
			'actualScore' : str(round(result_list[0]['prediction']['genres'][actualGenre]*100,4)),
			'songScore' : str(result_list[0]['prediction']['score']),
			'modelScore' : str(round(neuralNet.get_mean_score(),4)),
			'error' : error,
			'redirect_link' : redirect_link,
			'predictionVector': str(result_list[0]['prediction']['genres'])
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
