import * as ajaxRequests from './ajaxRequests.js'
import React from 'react';
import ReactDOM from 'react-dom';
import PageTwo from './pageTwo.js';

//creaate main page for our application
class MainPage extends React.Component{
  //create constructor for class that holds the page states
  constructor(props){
    super(props);

    this.state = {
      // States are hardcoded for now
      landingPage: true,
      secondPageState: false,
      songTitle: 'What You Know',
      artist: 'By: Two Door Cinema Club',
      predictedGenre: 'Electronic',
      predictedScore: '90%',
      actualGenre: 'Alternative',
      actualScore: '80%',
      modelScore: '*Model Score*'
    }
  }
  //create goto page state functions
  //in here setState will rerender the dom
  gotolandingPage = () =>{
    this.setState({
      landingPage: true,
      secondPageState: false,
    })
  }
  gotoPageTwoState = () =>{
    this.setState({
      landingPage: false,
      secondPageState: true,
    })
    //call ajaxrequest, must wait for page to render.
    const song = this.state.songTitle
    setTimeout(function() {ajaxRequests.sbm(song); }, 1000);
  }
  handleTextChange = (event) =>{
    this.setState({
      songTitle: event.target.value
    })
  }
  render() {
    if(this.state.landingPage === true){
      return (
        <main>
          <div className="pageContainer">
            <div className="boxContent">
              <div className="title">
                <div id="LandingPage">
                  Moosic Classifier
                </div>
                <div id="description">
                  music genre classifier
                </div>
              </div>
              <div id="textInput">
                <input
                  id="songInput"
                  style={{height: 40, fontSize:40}}
                  placholder="enter in song title"
                  onChange={this.handleTextChange}
                  value={this.state.songTitle}
                />
                <div className="buttons">
                  <button id="buttonStyle" onClick={this.gotoPageTwoState}> Search </button>
                  <button id="buttonStyle" onClick={this.gotoPageTwoState}> Feeling Lucky </button>
                </div>
              </div>
            </div>
          </div>
        </main>
      );
    } else if(this.state.secondPageState === true) {
      return (
        <PageTwo pageState={this.gotolandingPage} parentStates={this.state} />   
      );
    }
  }
}
ReactDOM.render(
    <MainPage />,
    document.getElementById('root')
);
