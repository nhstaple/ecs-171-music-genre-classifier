from flask import Flask, jsonify, request #import objects from the Flask model
app = Flask(__name__) #define app using Flask

languages = [{'name' : 'JavaScript'}, {'name' : 'Python'}, {'name' : 'Ruby'}]

songArray = ["one", "two","three"]

@app.route('/', methods=['GET'])
def test():
	return jsonify({'message' : 'It works!'})

@app.route('/lang', methods=['GET'])
def returnAll():
	return jsonify({'languages' : languages})

@app.route('/lang/<string:name>', methods=['GET'])
def returnOne(name):
	langs = [language for language in languages if language['name'] == name]
	return jsonify({'language' : langs[0]})

@app.route('/lang', methods=['POST'])
def addOne():
	language = {'name' : request.json['name']}

	languages.append(language)
	return jsonify({'languages' : languages})

@app.route('/lang/<string:name>', methods=['PUT'])
def editOne(name):
	langs = [language for language in languages if language['name'] == name]
	langs[0]['name'] = request.json['name']
	return jsonify({'language' : langs[0]})

@app.route('/lang/<string:name>', methods=['DELETE'])
def removeOne(name):
	lang = [language for language in languages if language['name'] == name]
	languages.remove(lang[0])
	return jsonify({'languages' : languages})


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