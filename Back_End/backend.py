from flask import Flask, jsonify, request, render_template #import objects from the Flask model
import sys, os
import pandas as pd
sys.path.append(os.path.abspath(os.path.join('..', 'Data_Management'))) #path to Data_Management folder
sys.path.append(os.path.abspath(os.path.join('..', 'ML_Algs'))) #path to ML_Algs folder
import pandasDB
import ANN_class
app = Flask(__name__, static_folder="../Front_End/build/", template_folder="../Front_End/build/") #define app using Flask

# Homepage, which is for testing. It uses url: http://localhost:8080
# @app.route('/', methods=['GET'])
# def test():
# 	return jsonify({'songGenre' : 'It works!'})

@app.route("/")
def index():
    return render_template("index.html")


# sample url: http://localhost:8080/song/enter song/True, 
# which the songName is the song title and can be changed
@app.route('/song/<string:name>/<string:randomFlag>/', methods=['GET'])
def findOneSong(name, randomFlag):

	# initialize error message
	error = False

	# get data from database
	if(randomFlag == 'True'):
		data = database.query(name, True)
		sample = data['track_data']
		songName = data['track_data']['song_title'][0]
		actualGenre = data['track_data']['top_genre'][0]
		artist = data['track_data']['artist_name'][0]
	else:
		data = database.query(name, False)
		# if there is no this song title, query return a empty list call 'track_data'
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

	# when error == False, query found the input song title. otherwise, skip below because data is empty
	if(error == False):
		#need to implement .selectN() to get N most influential featues for new models
		independent_features = neuralNet.get_features()
		# neuralNet = ANN_class.ANN(trained_model='best')
		sample['prediction'] = {}
		sample['X'] = sample['X'][independent_features]
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
			'redirect_link' : redirect_link
		})
	else:
		return jsonify({
			'error' : error
		})



if __name__ == '__main__':
	database = pandasDB.DataBase()
	neuralNet = ANN_class.ANN(trained_model='matt')
	app.run(debug=True, port=8080, host='0.0.0.0') #run app on port 8080 in debug mode
