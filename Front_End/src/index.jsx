//index.jsx
//Authors: Luc Nglankong, Cameron Fitzpatrick

import * as ajaxRequests from './ajaxRequests.js'
import React from 'react';
import ReactDOM from 'react-dom';
import PageTwo from './pageTwo.js';

//creaate main page for our application
class MainPage extends React.Component{
  //create constructor for class that holds the page states
  constructor(props){
    super(props);

    //State variables for MainPage component
    this.state = {
      landingPage: true,
      secondPageState: false,
      songTitle: '',
      artist: '',
      predictedGenre: '',
      predictedScore: '',
      actualGenre: '',
      actualScore: '',
      modelScore: ''
    }
  }
  
  // FUNCTION: gotolandingPage
  // DESCRIPTION: This function indicates that the user should be on the
  // first page by setting the state boolean variables landingPage to
  // true and secondPageState to false.Once these state variables change,
  // the render function will execute and choose what component to show
  // based on these variables.
  gotolandingPage = () =>{
    this.setState({
      landingPage: true,
      secondPageState: false,
    })
  }

  // FUNCTION: gotoPageTwoState
  // DESCRIPTION: This function indicates that the user should be on the
  // second page by setting the state boolean variables landingPage to 
  // false and secondPageState to true.Once these state variables 
  // change, the render function will execute and choose what component 
  // to show based on these variables.This function also retrieves the 
  // given song title from the state variable songTitle(which is set by 
  // the user in the input field) and creates an AJAX request containing 
  // the songTitle and a boolean representing that the Search Button was pressed.
  gotoPageTwoState = () =>{
    this.setState({
      landingPage: false,
      secondPageState: true,
    })
    //call ajaxrequest, must wait for page to render.
    const song = this.state.songTitle
    setTimeout(function() {ajaxRequests.sbm(song, 'False'); }, 1000);
  }

  // FUNCTION: gotoFeelingLucky
  // DESCRIPTION: This function is identical to gotoPageTwoState with 
  // the exception that the AJAX request contains a boolean 
  // representing that the Feeling Lucky button was pressed.
  gotoFeelingLucky = () => {
    this.setState({
      landingPage: false,
      secondPageState: true,
    })
    
    //call ajaxrequest, must wait for page to render.
    const song = this.state.songTitle
    setTimeout(function () {ajaxRequests.sbm(song, 'True');}, 1000);
  }

  // FUNCTION: handleTextChange
  // DESCRIPTION: This function retrieves the song title entered
  // in the input field by the user and saves it in the state 
  // variable songTitle.
  // INPUT:
  // (event) - the event object triggered by the input field.
  // The user input will be extracted from this parameter.
  handleTextChange = (event) =>{
    this.setState({
      songTitle: event.target.value
    })
  }

  // FUNCTION: render
  // DESCRIPTION: The render function is split into two components: 
  // one for the first page(this.state.landingPage === true) and one for the results
  // page(this.state.secondPageState === true).The first page features the input field, 
  // Search button and Feeling Lucky button.The results page calls the < PageTwo /> 
  // component in PageTwo.jsx.The gotolandingPage(), gotoFeelingLucky(), and state
  // variables of index.jsx are passed to the PageTwo component.Note that Index.js
  // is just the React representation of the JSX code from Index.jsx.

  render() {
    //first page
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
                  placeholder="Enter Song Title"
                  style={{height: 40, fontSize:40}}
                  onChange={this.handleTextChange}
                />
                <div className="buttons">
                  <button id="buttonStyle" onClick={this.gotoPageTwoState}> Search </button>
                  <button id="buttonStyle" onClick={this.gotoFeelingLucky}> Feeling Lucky </button>
                </div>
              </div>
            </div>
          </div>
        </main>
      );
      //second page
    } else if(this.state.secondPageState === true) {
      return (
        <PageTwo pageState={this.gotolandingPage} parentStates={this.state} feelingLucky={this.gotoFeelingLucky}/>   
      );
    }
  }
}
ReactDOM.render(
    <MainPage />,
    document.getElementById('root')
);
