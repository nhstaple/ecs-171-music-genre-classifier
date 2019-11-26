# Back End

## Frameworks: Flask
+ **NAME:** findOneSong(name, randomFlag)
+ **DESCRIPTION:** The function will take the song tiel as @name and the random pick sonf feature as @randomFlag from the url, which front-end triggers. Both @name and @randomFlag are string datatype. @name can be anything inside a string, but @randomFlag should be 'True' or 'False' only. The function will return a json message, which contaions one object 'error' only when there is no this song title in database or result with objects, 'songName','artist', 'songGenre', 'predictedScore', 'actualGenre, 'songScore', 'modelScore', 'error', when the song is in the database.
+ **EXAMPLES:** For example, 'http://localhost:8080/song/enter song/True', @name is 'enter song' and @randomFlag is 'True'
