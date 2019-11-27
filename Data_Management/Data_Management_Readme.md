# Additional CSV's
In order to run the website no additional files must be downloaded as they are already in the
Data folder of the repository. However some of the data_management files use additional CSV's and
the full feature set, instead of the reduced one, to display the data. In order to have all the
necessary files you must Download: https://os.unil.cloud.switch.ch/fma/fma_metadata.zip
place the csv's(tracks.csv, features.csv, echonest.csv, and genres.csv) in the data folder.
Then run the makePick.py script in the data folder in order to generate necessary 
pickle files. Once this is done you will have the necessary files to run the notebooks and 
any other scripts that may be found in the Data_Management folder.

# CSVInterface.py

CSVInterface was created early in order to provide a simple interface to interact with the data which is stored in CSV(comma-separated values) files. Later on, files were converted to pickle files instead of CSV's as the time it took to read in data from a pickle file is substantially faster.

`featRead()`: Constructor for the featRead class. Constructor reads in all necessary .pkl(pickle) files. Data frames are then stored in a dictionary that is created when the object is instantiated.
* Example usage: `reader = featRead()`

`listFrames()`: Prints out a list of all the data frames that are stored in the objects `tableDF`(Dictionary).
* Example usage: `reader.listFrames()`

`getFrame()`: Returns specific dataframe in found in *tablesDF*. 
* Example usage: `frame = reader.getFrame('features')`

`getFeatures()`: Returns a subset of statistics('features') from a specific feature category. Statistics are passes in a list. Returns features as a data frame.
* Example usage: `chroma_means = reader.getFeatures('chroma_cens', stat=['mean'])`

`getSubset()`: Returns a subset of the data frame.
* Example usage: `newFrame = reader.getSubset(frame, 'medium')`

`makeKfold()`: Returns a collection of data frames. Takes in data frame and number of folds as parameters.
* Example usage: `frames = reader.makeKfold(dataFrame, 2)`

`mergeFrames()`: Wrapper function around pandas merge function that allows you to merge two data frames on their track_id's(index).
* Example usage: `newFrame = mergeFrames(frame1, frame2)`


# PandasDB.py
Implements the "DataBase" class that is used when querying for songs and their information such as name, track ID, audio features, etc.

## Class Methods

`DataBase()`: The constructor that initializes the "DB". Reads in pickle files, that contain the data, that are found in the "Data/" directory.(Assumes files are placed there)
* Usage example: `db = DataBase()`

`getSubset()`: Returns a data frame that is a specific subset of the data frame that was passed into the function. Subsets are *small*, *medium*, *large*, and *cleanLarge*. For more information on subsets look at DataOverview.md found in Data_Management. *cleanLarge is the same as the large set, but samples with no labels were removed.* 
* Usage example: `newFrame = db.getSubset(frame, 'small')`

`getRandomSong()`: Returns a random song(sample) from a specified subset. If no subset is specified then *medium* subset is assumed by default.
* Usage example: `song = db.getRandomSong('small')`

`query()`: Function receives a song to search in the database from the front end. The function takes in the song title that is being queried and a flag specifying whether to look for the specified song or return a random song. Returns a dictionary or list of dictionaries in the case where several songs of the same name. Each dictionary contains information such as the *track_id*, *artist_name*, *top_genre*, *audio features*, *etc.*
* Usage example: `db.query('songName', False)` This will query the DB for song of title 'songName'
* Usage example: `db.query('songName', True)` Ignores songName and calls getRandomSong().

# binInterface:
A simpler version of CSVInterface. The only difference is that CSVInterface
uses the whole csv files. Bin interface simply reads in the reduced feature
pickle files. Returns features ready to be fed staright into the model.

### Methods

getBins('subset'): Returns a dictionary with 16 bins(root genres) for both the medium
and cleanLarge subset. Small subset only contains 8 bins. Songs in each subest are 
sorted into there respective bins(genre).
* Usage example: `binInterface.getBins('small')` returns a dictionary with 8 bins.