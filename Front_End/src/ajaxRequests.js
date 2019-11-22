import React, { useEffect, useState } from "react";

//create and export ajax base function:
export function createAJAXRequest(method, url) {
    let xhr = new XMLHttpRequest();
    console.log("METHOD: " + method + " URL: " + url);
    xhr.open(method, url, true);  // call its open method
    return xhr;
}
/* this function will grab the url from the window: */
function getUrlVars() {
let vars = {};
let parts = window.location.href.replace(/[?&]+([^=&]+)=([^&]*)/gi,
function(m,key,value) {
  vars[key] = value;
});
return vars;
}
//create actual ajax request to send song title, and receive a response from the swe team:
//ajax grabs the info from the url

function makeAJAXRequest(song = getUrlVars()(["songTitle"]), random='True'){
    //for backend, find url we need (url1 is temporary):
    let url1 = "/song/";
    let url2 = url1 + song + "/" + random + "/";
    console.log(url2); //JD: for testing
    
    //sending song title to server and wait to get genre back
    let xhr = createAJAXRequest('GET', url2);

    //checking for errors
    if (!xhr) {
	     alert('CORS not supported');
	     return;
    }
    //here is the callback function that we get the response in
    xhr.onload = function() {
        //grab the response from swe team
        let responseStr = xhr.responseText;  // get the JSON string
        console.log(responseStr); //to test

        let object = JSON.parse(responseStr);  // turn it into an object

        if(object.error === true){
            alert("song is not in the database");
            return;
        }
        console.log(object);

        //place the response on the screen
        document.getElementById('songName').textContent = object.songName;
        document.getElementById('artist').textContent = object.artist;
        document.getElementById('placeGenreHere').textContent = object.songGenre;
        document.getElementById('predictedScore').textContent = object.predictedScore + "% probability";
        document.getElementById('actualGenre').textContent = "Actual: " + object.actualGenre;
        document.getElementById('songScore').textContent = "Song Rank: " + object.songScore;
        document.getElementById('actualScore').textContent = object.actualScore + "% probability";
        document.getElementById('modelScore').textContent = "Model Rank: " + object.modelScore;
        
        //console.log(object); //to test
    }
    xhr.send();

}
//at this point, user has clicked the search button, so we will need to send the request:
export function sbm(id, random){
    //this function makes request and sends it:
    //Backend: uncomment to test
    makeAJAXRequest(id, random);
    //below works, testing placing a response onto screen:
    // let temporaryResponse = "Sent Request " + id
    // document.getElementById('placeGenreHere').textContent = temporaryResponse
}
