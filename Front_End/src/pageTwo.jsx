import React from 'react';
import ReactDOM from 'react-dom';
class PageTwo extends React.Component{
    
    constructor(props) {
        super(props);
    }

    //wrapper that calls gotolandingPage in index.jsx
    gotolandingPage = () =>{        
        this.props.pageState();
    }

    //wrapper that calls gotoFeelingLucky in index.jsx
    //while new information is loading set all output to empty
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