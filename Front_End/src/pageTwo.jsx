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
                                {this.props.parentStates.songTitle}
                            </div>
                            <div id="artist">
                                {this.props.parentStates.artist}
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
                            {this.props.parentStates.predictedScore} Confidence
                        </div>
                    </div>
                    <div id="actual_genre">
                        <div id="actual_genre_name">
                            Actual: {this.props.parentStates.actualGenre}
                        </div>
                        <div id="actual_genre_probability">
                            {this.props.parentStates.actualScore} Confidence
                        </div>
                    </div>
                    <div id="model_stats">
                        <img src={require('./sampleImage.png')}/>
                        <div id="model_score">
                            {this.props.parentStates.modelScore}
                        </div>
                    </div>
                </div>
           </main>
        );
    }

}

export default PageTwo;