import React, { useEffect, useState } from "react";

//create and export ajax base function:
export function createAJAXRequest(method, url) {
    let xhr = new XMLHttpRequest();
    console.log("METHOD: " + method + " URL: " + url);
    xhr.open(method, url, true);  // call its open method
    return xhr;
}

// this function will grab the url from the window:
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
    //construct request URL
    let url1 = "/song/";

    //if no song is given, put RANDOM in URl
    if(song == ""){
        song = "RANDOM";
    }

    //final URL
    let url2 = url1 + song + "/" + random + "/";
    
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

        let object = JSON.parse(responseStr);  // turn it into an object

        //check if response object returned an error
        if(object.error === true){
            //trigger an alert
            alert("song is not in the database");

            //remove loading screen
            document.getElementById('placeGenreHere').textContent = '';
            return;
        }

        //place the response on the screen
        document.getElementById('songName').textContent = object.songName;
        document.getElementById('artist').textContent = object.artist;
        document.getElementById('placeGenreHere').textContent = object.songGenre;
        document.getElementById('predictedScore').textContent = object.predictedScore + "% probability";
        document.getElementById('actualGenre').textContent = "Actual: " + object.actualGenre;
        document.getElementById('songScore').textContent = "Song Rank: " + object.songScore;
        document.getElementById('actualScore').textContent = object.actualScore + "% probability";
        document.getElementById('modelScore').textContent = "Model Rank: " + object.modelScore;
        document.getElementById('redirect_link').href = object.redirect_link;
        document.getElementById('redirect_link').textContent = "YouTube Search";
    }
    xhr.send();
}

//at this point, user has clicked the search button, so we will need to send the request:
export function sbm(id, random){
    //begin AJAX request
    makeAJAXRequest(id, random);
}
