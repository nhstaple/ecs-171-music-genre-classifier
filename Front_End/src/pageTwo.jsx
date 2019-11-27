//pageTwo.jsx
//Authors: Luc Nglankong

import React from 'react';
import ReactDOM from 'react-dom';
class PageTwo extends React.Component{
    
    constructor(props) {
        super(props);
    }

    // FUNCTION: gotolandingPage
    // DESCRIPTION: This function wraps the gotolandingPage 
    // function of index.jsx.It will get called when the Go 
    // Back button is pushed.
    gotolandingPage = () =>{        
        this.props.pageState();
    }

    // FUNCTION: gotoFeelingLucky
    // DESCRIPTION: This function wraps the gotoFeelingLucky function 
    // of index.jsx.It will get called when the Random Song button is 
    // pushed.It will also set all of the text on this page to empty 
    // while the new random data is being retrieved.
    gotoFeelingLucky = () => {
        //clear page while loading new song
        document.getElementById('songName').textContent = '';
        document.getElementById('artist').textContent = '';
        document.getElementById('placeGenreHere').textContent = 'LOADING...';
        document.getElementById('predictedScore').textContent = '';
        document.getElementById('actualGenre').textContent = '';
        document.getElementById('songScore').textContent = '';
        document.getElementById('actualScore').textContent = '';
        document.getElementById('modelScore').textContent = '';
        document.getElementById('redirect_link').textContent = '';
        this.props.feelingLucky();
    }

    // FUNCTION: render
    // DESCRIPTION: This function returns JSX code that will build 
    // the HTML for the results page.This page features the song 
    // title, artist, predicted genre, predicted genre probability, 
    // actual genre, actual genre probability, song rank and model 
    // rank.There is also a back button that goes back to the first 
    // page, random button that will reroll results for a random song, 
    // and a YouTube search link that will search for the given song and 
    // artist.When there is initially no data, the predicted genre text 
    // is replaced with 'Loading...' until a response is received from 
    // the backend.

    render() {
        //page two contents
        return(
            <main>
                <div id="page_two_contents">
                    <h1>
                        <div id="title_and_artist">
                            <div id="songTitle">
                                <p id="songName">
                                </p>
                            </div>
                            <div id="artist">
                                <p id="artist">
                                </p>
                            </div>
                        </div>
                    </h1>
                    <button id="back_button" onClick={this.gotolandingPage}>Go Back</button>
                    <button id="random_button" onClick={this.gotoFeelingLucky}> Random Song </button>
                    <div id="predicted_genre">
                        <div id="predicted_genre_name">
                            <p id="placeGenreHere">
                                LOADING...
                            </p>
                        </div>
                        <div id="predicted_genre_probability">
                            <p id="predictedScore">
                            </p>
                        </div>
                    </div>
                    <div id="actual_genre">
                        <div id="actual_genre_name">
                            <p id="actualGenre">
                            </p>
                        </div>
                        <div id="actual_genre_probability">
                            <p id="actualScore">
                            </p>
                        </div>
                    </div>
                    <div id = "song_stats">
                        <div id = "song_score">
                            <p id = "songScore">
                            </p>
                        </div>
                    </div>
                    <div id="model_stats">
                        <div id="model_score">
                            <p id="modelScore">
                            </p>
                        </div>
                    </div>
                    <a id="redirect_link" style={{display: "table-cell"}} href="" target="_blank"/>
                </div>
           </main>
        );
    }

}

export default PageTwo;