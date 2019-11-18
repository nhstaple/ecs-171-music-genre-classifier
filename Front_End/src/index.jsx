import * as ajaxRequests from './ajaxRequests.js'
import React from 'react';
import ReactDOM from 'react-dom';

//creaate main page for our application
class MainPage extends React.Component{
  //create constructor for class that holds the page states
  constructor(props){
    super(props);
    this.state = {
      landingPage: true,
      secondPageState: false,
      thirdPageSate: false,
      songTitle: ' '
    }
  }
  //create goto page state functions
  //in here setState will rerender the dom
  gotolandingPage = () =>{
    this.setState({
      landingPage: true,
      secondPageState: false,
      thirdPageState: false
    })
  }
  gotoPageTwoState = () =>{
    this.setState({
      landingPage: false,
      secondPageState: true,
      thirdPageState: false
    })
    //call ajaxrequest, must wait for page to render.
    const song = this.state.songTitle
    setTimeout(function() { ajaxRequests.sbm(song); }, 1000);
  }
  gotoPageThreeState = () =>{
    this.setState({
      landingPage: false,
      secondPageState: false,
      thirdPageState: true
    })
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
            <p id="LandingPage">
              Please enter in a song title to find its genre
            </p>
            <div id="textInput">
              <p id="songInputP">
                song title
              </p>
              <input
                style={{height: 40, fontSize:40}}
                placholder="enter in song title"
                onChange={this.handleTextChange}
                value={this.state.songTitle}
              />
              <button id="buttonStyle" onClick={this.gotoPageTwoState}> Search </button>
            </div>
          </div>
        </main>
      );
    } else if(this.state.secondPageState === true) {
      return (
        <main>
          <div className="pageContainer">
            <p id="placeGenreHere">
            </p>
            <button id="SecondPageButton" onClick={this.gotoPageThreeState}>goto 3rd page</button>
          </div>
        </main>
      );
    } else if(this.state.thirdPageState === true) {
      return (
        <main>
          <div className="pageContainer">
            <p id="ThirdPage">
              page 3
            </p>
            <button id="ThirdPageButton" onClick={this.gotolandingPage}>goto 1st page</button>
          </div>
        </main>
      );
    }
  }
}
ReactDOM.render(
    <MainPage />,
    document.getElementById('root')
);
