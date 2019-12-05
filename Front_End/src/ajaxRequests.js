//ajaxRequests.js
//Authors: Luc Nglankong, Cameron Fitzpatrick, Jiahui Dai

import React, { useEffect, useState } from "react";

// FUNCTION: createAJAXRequest
// DESCRIPTION: This function creates a request given the method(GET or POST) 
// and url.This function is primarily used to make a GET request.
// INPUT:
// (method) - The request method, which is either GET or POST
// (url) - The request URL in the format <domain>/song/<songTitle>/<randomFlag>/
// OUTPUT:
// (xhr) - Request object
export function createAJAXRequest(method, url) {
    let xhr = new XMLHttpRequest();
    console.log("METHOD: " + method + " URL: " + url);
    xhr.open(method, url, true);  // call its open method
    return xhr;
}

// FUNCTION: getUrlVars
// DESCRIPTION: This is a helper function that will take the url 
// from the window and return parameters found within it.
// This is how the song title is retrieved.
// OUTPUT:
// (vars) - every parameter in the URL in a dictionary
function getUrlVars() {
    let vars = {};
    let parts = window.location.href.replace(/[?&]+([^=&]+)=([^&]*)/gi,
    function(m,key,value) {
        vars[key] = value;
    });
    return vars;
}

// FUNCTION: makeAJAXRequest
// DESCRIPTION: This function takes the processed song title from getUrlVars() 
// and whether or not the "Feeling Lucky" button was pressed to create an AJAX 
// request.The request url is built using < domain > /song/ < songTitle > /<random> 
// if the Search button was pushed or <domain>/song / RANDOM / <songTitle> if the 
// Feeling Lucky button was pushed and creates the GET request by calling 
// createAJAXRequest(). The function then checks for errors and sends the request 
// before receiving the callback function. In the callback function, the response 
// object is obtained which holds the JSON response from the backend and then modifies 
// the DOM on the front end to show the output.
// INPUT:
// (song) - The song name from the input.
// (random) - a boolean flag that represents if a random search should
// be performed on the database.  Is True when "Feeling Lucky" or
// "Random Song" buttons are pressed and is false when "Search"
// button is pressed.
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

        //quick fix to reset highlighting
        document.getElementById("genre_rank_1").style.backgroundColor = "";
        document.getElementById("probability_rank_1").style.backgroundColor = "";
        document.getElementById("genre_rank_2").style.backgroundColor = "";
        document.getElementById("probability_rank_2").style.backgroundColor = "";
        document.getElementById("genre_rank_3").style.backgroundColor = "";
        document.getElementById("probability_rank_3").style.backgroundColor = "";
        document.getElementById("genre_rank_4").style.backgroundColor = "";
        document.getElementById("probability_rank_4").style.backgroundColor = "";
        document.getElementById("genre_rank_5").style.backgroundColor = "";
        document.getElementById("probability_rank_5").style.backgroundColor = "";
        document.getElementById("genre_rank_6").style.backgroundColor = "";
        document.getElementById("probability_rank_6").style.backgroundColor = "";
        document.getElementById("genre_rank_7").style.backgroundColor = "";
        document.getElementById("probability_rank_7").style.backgroundColor = "";
        document.getElementById("genre_rank_8").style.backgroundColor = "";
        document.getElementById("probability_rank_8").style.backgroundColor = "";

        //place the response on the screen
        document.getElementById('songName').textContent = object.songName;
        document.getElementById('artist').textContent = object.artist;
        document.getElementById('genre_rank_1').textContent = "1. " + object.genre_rank_1 + ":";
        document.getElementById('genre_rank_2').textContent = "2. " + object.genre_rank_2 + ":";
        document.getElementById('genre_rank_3').textContent = "3. " + object.genre_rank_3 + ":";
        document.getElementById('genre_rank_4').textContent = "4. " + object.genre_rank_4 + ":";
        document.getElementById('genre_rank_5').textContent = "5. " + object.genre_rank_5 + ":";
        document.getElementById('genre_rank_6').textContent = "6. " + object.genre_rank_6 + ":";
        document.getElementById('genre_rank_7').textContent = "7. " + object.genre_rank_7 + ":";
        document.getElementById('genre_rank_8').textContent = "8. " + object.genre_rank_8 + ":";
        document.getElementById('probability_rank_1').textContent = object.probability_rank_1 + "% probability";
        document.getElementById('probability_rank_2').textContent = object.probability_rank_2 + "% probability";
        document.getElementById('probability_rank_3').textContent = object.probability_rank_3 + "% probability";
        document.getElementById('probability_rank_4').textContent = object.probability_rank_4 + "% probability";
        document.getElementById('probability_rank_5').textContent = object.probability_rank_5 + "% probability";
        document.getElementById('probability_rank_6').textContent = object.probability_rank_6 + "% probability";
        document.getElementById('probability_rank_7').textContent = object.probability_rank_7 + "% probability";
        document.getElementById('probability_rank_8').textContent = object.probability_rank_8 + "% probability";
        document.getElementById('actualGenre').textContent = "Actual: " + object.actualGenre;
        document.getElementById('songScore').textContent = "Song Rank: " + object.songScore;
        document.getElementById('actualScore').textContent = object.actualScore + "% probability";
        document.getElementById('modelScore').textContent = "Model Rank: " + object.modelScore;
        document.getElementById('redirect_link').href = object.redirect_link;
        document.getElementById('redirect_link').textContent = "YouTube Search";
        document.getElementById("genre_rank_" + object.songScore).style.backgroundColor = "yellow";
        document.getElementById("probability_rank_" + object.songScore).style.backgroundColor = "yellow";
    }
    xhr.send();
}

// FUNCTION: sbm
// DESCRIPTION: This is the exported function in ajaxRequest.js that 
// gets called when index.jsx attempts to send an AJAX request.
// It will start the process of creating the AJAX request by calling 
// makeAJAXRequest().
// INPUT:
// (id) - song title from user
// (random) - a boolean flag that represents if a random search should
// be performed on the database.  Is True when "Feeling Lucky" or
// "Random Song" buttons are pressed and is false when "Search"
// button is pressed.
export function sbm(id, random){
    //begin AJAX request
    makeAJAXRequest(id, random);
}
