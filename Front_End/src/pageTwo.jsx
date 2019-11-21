import React from 'react';
import ReactDOM from 'react-dom';
class PageTwo extends React.Component{
    
    constructor(props) {
        super(props);
    }

    gotolandingPage = () =>{
        console.log("ATTEMPTING TO LEAVE");
        
        this.props.pageState();
    }

    render() {
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
                    <div id="predicted_genre">
                        <div id="predicted_genre_name">
                            <p id="placeGenreHere">
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
                    <div id="model_stats">
                        <div id="model_score">
                            <p id="modelScore">
                            </p>
                        </div>
                    </div>
                </div>
           </main>
        );
    }

}

export default PageTwo;