# Front End
## Frameworks: React
## Modules: node.js, webpack, npm
### Index.jsx
#### NAME: render()
+ **DESCRIPTION:** This is the file responsible for the first page of the UI.  The render() function returns JSX code that will create the final HTML outline for the first page.  The render function is split into two components: one for the first page (this.state.landingPage === true) and one for the results page (this.state.secondPageState === true).  The first page features the input field, Search button and Feeling Lucky button.  The results page calls the &lt;PageTwo/&gt; component in PageTwo.jsx.  The gotolandingPage(), gotoFeelingLucky(), and state variables of index.jsx are passed to the PageTwo component.  Note that Index.js is just the React representation of the JSX code from Index.jsx. <br /> <br />
#### NAME: gotolandingPage = () => {}
+ **DESCRIPTION:** This function indicates that the user should be on the first page by setting the state boolean variables landingPage to true and secondPageState to false.  Once these state variables change, the render function will execute and choose what component to show based on these variables.
#### NAME: gotoPageTwoState = () => {}
+ **DESCRIPTION:** This function indicates that the user should be on the second page by setting the state boolean variables landingPage to false and secondPageState to true.  Once these state variables change, the render function will execute and choose what component to show based on these variables.  This function also retrieves the given song title from the state variable songTitle (which is set by the user in the input field) and creates an AJAX request containing the songTitle and a boolean representing that the Search Button was pressed.<br /> <br />
#### NAME: gotoFeelingLucky = () => {}
+ **DESCRIPTION:** This function is identical to gotoPageTwoState with the exception that the AJAX request contains a boolean representing that the Feeling Lucky button was pressed.<br /> <br />
#### NAME: handleTextChange = () => {}
+ **DESCRIPTION:** This function retrieves the song title entered in the input field by the user and saves it in the state variable songTitle.<br /><br />
+ **Parameters:**
event - the event object triggered by the input field. The user input will be extracted from this parameter.<br /> <br />
### pageTwo.jsx
#### NAME: render()
+ **DESCRIPTION:** This function returns JSX code that will build the HTML for the results page.  This page features the song title, artist, predicted genre, predicted genre probability, actual genre, actual genre probability, song rank and model rank.  There is also a back button that goes back to the first page, random button that will reroll results for a random song, and a YouTube search link that will search for the given song and artist.  When there is initially no data, the predicted genre text is replaced with 'Loading...' until a response is received from the backend.<br /><br /> 
#### NAME: gotolandingPage = () => {}
+ **DESCRIPTION:** This function wraps the gotolandingPage function of index.jsx.  It will get called when the Go Back button is pushed.<br /> <br /> 
#### NAME: gotoFeelingLucky = () => {}
+ **DESCRIPTION:** This function wraps the gotoFeelingLucky function of index.jsx.  It will get called when the Random Song button is pushed.  It will also set all of the text on this page to empty while the new random data is being retrieved.<br /> <br /> 
### ajaxRequest.js
#### NAME: sbm(id, random)
+ **DESCRIPTION:** This is the exported function in ajaxRequest.js that gets called when index.jsx attempts to send an AJAX request.  It will start the process of creating the AJAX request by calling makeAJAXRequest().<br /><br />
+ **Parameters:**<br /> 
***id*** - song title from user<br /> 
***random*** - a boolean flag that represents if a random search should be performed on the database.  Is True when "Feeling Lucky" or "Random Song" buttons are pressed and is false when "Search" button is pressed.
#### NAME: makeAJAXRequest(song, random)
+ **DESCRIPTION:** This function takes the processed song title from getUrlVars() and whether or not the "Feeling Lucky" button was pressed to create an AJAX request.  The request url is built using &lt;domain&gt;/song/&lt;songTitle&gt;/&lt;random&gt; if the Search button was pushed or &lt;domain&gt;/song/RANDOM/&lt;songTitle&gt; if the Feeling Lucky button was pushed and creates the GET request by calling createAJAXRequest().  The function then checks for errors and sends the request before receiving the callback function.  In the callback function, the response object is obtained which holds the JSON response from the backend and then modifies the DOM on the front end to show the output.<br /><br />
+ **Parameters:**<br />
***song*** - The song name from the input.<br />
***random*** - a boolean flag that represents if a random search should be performed on the database.  Is True when "Feeling Lucky" or "Random Song" buttons are pressed and is false when "Search" button is pressed.<br /><br />
#### NAME: getUrlVars()
+ **DESCRIPTION:** This is a helper function that will take the url from the window and return parameters found within it.  This is how the song title is retrieved.<br /><br />
+ **Output:**<br />
***vars*** - every parameter in the URL stored in a dictionary.<br />
#### NAME: createAJAXRequest(method, url)
+ **DESCRIPTION:** This function creates a request given the method (GET or POST) and url.  This function is primarily used to make a GET request. <br /><br />
+ **Parameters:**
***method*** - The request method, which is either GET or POST.<br />
***url*** - The request URL built in makeAJAXRequest()
+ **Output:**
***xhr*** - Request object.<br />
