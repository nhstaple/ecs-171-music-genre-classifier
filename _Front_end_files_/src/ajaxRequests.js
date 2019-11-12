//create and export ajax base function:
export function createAJAXRequest(method, url) {
    let xhr = new XMLHttpRequest();
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
function makeAJAXRequest(song = getUrlVars()(["songTitle"])){
    //I'm not sure what to query for the url, have to figure this out
    //for now just using this url:
    let url1 = "/findgenre?song=";
    let url2 = url1 + song;
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
       //console.log(responseStr); //to test
	     let object = JSON.parse(responseStr);  // turn it into an object
       //place the response on the screen
       //for now just place on Landing Page, this is a html paragraph dom element
       document.getElementById('LandingPage').textContent = object.songGenre;
	     //console.log(object); //to test
    }
    xhr.send();
}
//at this point, user has clicked the search button, so we will need to send the request:
export function sbm(){
    //for now songinput is hardcoded, will need to change!!
    let id = document.getElementById("songInput").value;
    makeAJAXRequest(id);
}
