# Back End

## FILE NAME: backend.py
#### FUNCTION NAME: findOneSong(name, randomFlag)
+ **DESCRIPTION:** The function will take the song title as @name and the random song parameter as @randomFlag from the url, which is sent by the front-end. If the "Search" buttons were pressed on the front-end, then @randomFlag will be 'True' and if the "Feeling Lucky" or "Random Song" button was pressed, then @randomFlag will be 'False'.  In the pipeline, a search query will be sent to the database containing @name and @randomFlag.  Then, information about the song is collected from the database.  If there are multiple songs with the same name, all data for all of the songs will be collected.  The data is then passed to the predict function of the neural network and a prediction is retrieved.  Finally, the function will return a json message, which contaions one object 'error' only when there is no this song title in database or result with objects, 'songName','artist', 'songGenre', 'predictedScore', 'actualGenre, 'songScore', 'modelScore', 'error', when the song is in the database.
+ **PARAMETER 1:** @name (string datatypes) is the song title that the user enters in the front end. @name can be anything inside a string.
+ **PARAMETER 2:** @randomFlag (string datatypes) is the feature flag that ignores the user input and picks a random song from the database. @randomFlag should be 'True' or 'False' only.
+ **Frameworks:** Flask
+ **EXAMPLES:** For example, 'http://0.0.0.0:8080/song/enter song/True', @name is 'enter song' and @randomFlag is 'True'

## FILE NAME: song_result_interface.py
+ **DESCRIPTION:** The file shows the format of data from pandasDB.py (Data Management team’s code) to backend.py (Back end team’s code).
