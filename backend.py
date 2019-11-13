from flask import Flask, jsonify, request #import objects from the Flask model
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
	for song in songArray:
		if song == name:
			return jsonify({'songGenre' : 'I find it!'})

	return jsonify({'songGenre' : 'I do not find it.'})

@app.route('/song', methods=['POST'])
def findOneSong2():
	for song in songArray:
		if song == request.json['name']:
			return jsonify({'songGenre' : 'I find it!'})

	return jsonify({'songGenre' : 'I do not find it.'})



if __name__ == '__main__':
	app.run(debug=True, port=8080) #run app on port 8080 in debug mode