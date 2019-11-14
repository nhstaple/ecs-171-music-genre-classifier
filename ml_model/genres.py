# genres.py


NUM_GENRES = 16

# Genres
classes = []
for i in range(0, NUM_GENRES):
	classes.append(
		"Genre {0}".format(int(i + 1))
	)