# Metadata
The "fma_metadata.zip" is contains the following csv's
* tracks.csv
* genres.csv
* features.csv
* echonest.csv


## Tracks

This file contains per-track, per-album, and per-artist metadata. Additionaly
each track id has two columns that correspond to what subset it belongs to and
whether the track was split for training, validation, or testing.

### Subsets

1. Full: Complete Dataset. 161 Genres. Unbalanced 1 - 38K tracks per genres.

2. Large: Full dataset with audio limited to 30 sec. clips extracted from
middle of track.

3. Medium: Root genre recognition should be treated as a multi-label problem
in general this set is constructed for the simpler problem of single label prediction.
Tracks here only have one top genre and sampled clips according to completeness
of meta-data, popularity, in hopes of selecting tracks of higher quality.
25k 30sec clips. Genre unbalanced with 21-7,103 clips per top genre.

4. Small: Top 1,000 clips from the 8 most popular genres of med. set. 
8,000 30sec clips. Balanced with 1,000 clips per genre, 1 root genre per clip

### Splits
80/10/10% split is proposed for training. This is satisfied for all subsets.
Track is assigned to same split across all of the subsets.

### Per-track table preview

![Per-Track Table](https://github.com/nhstaple/ecs-171-music-genre-classifier/blob/master/Data_Management/per-track.PNG)

Per-Track Columns:
* bit_rate
* comments
* composer
* date_created
* date_recorded
* duration
* favorites
* genre_top
* genres
* genres_all
* information
* interest
* language_code
* license
* listens
* lyricist
* number
* publisher
* tags
* title

### Per-Album table
![Per-Album](https://github.com/nhstaple/ecs-171-music-genre-classifier/blob/master/Data_Management/per-album.PNG "Per-Album Table")

### Per-Artist table preview
![Per-Artist](https://github.com/nhstaple/ecs-171-music-genre-classifier/blob/master/Data_Management/per-artist.PNG "Per-Artist Table") 

* ative_year_begin
* active_year_end
* associated_labels
* bio
* comments
* date_created
* favorites
* id
* latitude
* location
* longitude
* members
* name
* related_projects
* tags
* website
* wikiPage


### Per-Set table preview
![Per-Set](https://github.com/nhstaple/ecs-171-music-genre-classifier/blob/master/Data_Management/per-set.PNG "Per-Set Table")

* Split
* Subset

## Genres

Contains a genre heirarchy. 161 genres of which 16 are roots. Each track has a
*genres* feature which contains the genre_ids that are associated with that
track. The *genres_top* feature contains the tracks Root Genre. Finally, the
*genres_all* column contains all the genres that are traversed through the tree
when going from the *genres* to *genre_top*.

### Root Genres
![Top Genres](https://github.com/nhstaple/ecs-171-music-genre-classifier/blob/master/Data_Management/top_genres.PNG)


## Features

The features table consits of the following features
* Chroma
	* chroma_cens: computes the variant "Chroma Energy Noramlized" after
	obtaining vectors from chroma_cqt. Features are robust to dynamics,
	timbre and articulation. Used commonly in audio matching and retrival
	applications.
	* chroma_cqt:  Constant-Q transorm. Uses a logarithmically spaced
	frequency axis.
	* chroma_stft: Compute a chromogram from a waveform or power spectogram


Chroma feature relates to the twelve different pitch classes. They capture
harmonic and melodic characterisitics of music. Spectrum is projected onto 
12 bins each representing 12 distinct chroma  of the musical octave.

### Visualization of Chroma Gram
![Chroma Gram](https://github.com/nhstaple/ecs-171-music-genre-classifier/blob/master/Data_Management/chroma_gram.PNG "Chroma Gram")

* Tonnetz 
	* tonnetz: tonal centroid features. 

* MFCC 
	* mfcc: Mel-Frequency coeffecients 

Mel-Frequency is a representation of the short-term power spectrum of a sound.
MFCC's are the coeffecients that collectively make up an MFC. Commonly used as
features in speech recognition. Finding use in other applications such as
genre classification and audio similarity.

* Spec. Centroid
	* spectral_centroid: Indicates where the "center of mass" of spectrum
	is located. "Brightness" of a sound. At which frequency the energy of
	a spectrum is centered on.

* Spec. Bandwidth 
	* spectral_bandwidth: Wavelength interval in which a spectral quantity
	is not less than half of max value.

* Spec Contrast
	* spectral_contrast: Considers the spectral peak, the spectral valley,
	and their difference in each frequency subband.

* Spec Rollof 
	* spectral_rolloff: frequency below which a specified percentage of the
	total spectral energy lies.

[More Info](https://musicinformationretrieval.com/spectral_features.html)

* RMS energy 
	* rmse: Computes the root-mean-square(RMS) energy for each frame from
	audio samples.

* Zero-Crossing Rate
	* zcr: Number of times the signal crosses horizontal axis.

[More Info](https://musicinformationretrieval.com/zcr.html)

Each feature has a certain amount of windows, where each window is 2048
samples. Statistics such as the mean, med, min, etc. are then applied to each
window for each feature. This way the feature table consists of 518 features.


## Echonest

Features in the Echonest table are derived by a music analyzing program
built by a company called Echonest, which derives information about the
song and uses algorithms to rate them on various metrics defined by
Echonest. Could not find documentation explaining how features were calculated
as they are proprietary. Therefore we did not use them in this project.
