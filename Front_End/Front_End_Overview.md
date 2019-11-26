# Back End

## Frameworks: Flask
+ **NAME:** findOneSong(name, randomFlag)
+ **DESCRIPTION:** The function will take the song tiel as @name and the random pick sonf feature as @randomFlag from the url, which front-end triggers. Both @name and @randomFlag are string datatype. @name can be anything inside a string, but @randomFlag should be 'True' or 'False' only. The function will return a json message, which contaions one object 'error' only when there is no this song title in database or result with objects, 'songName','artist', 'songGenre', 'predictedScore', 'actualGenre, 'songScore', 'modelScore', 'error', when the song is in the database.
+ **EXAMPLES:** For example, 'http://localhost:8080/song/enter song/True', @name is 'enter song' and @randomFlag is 'True'


BELOW is what cameron added, not sure if this is useful, but I put it here just in case. 
### Front End
+ **Frameworks:** React
+ **Modules:** node.js, webpack, npm
## Index.jsx
+ **NAME:** render()
+ **DESCRIPTION:** This is the file responsible for the first page of the UI.  The render() function returns JSX code that will create the final HTML outline for the first page.  The render function is split into two components: one for the first page (this.state.landingPage === true) and one for the results page (this.state.secondPageState === true).  The first page features the input field, Search button and Feeling Lucky button.  The results page calls the <PageTwo/> component in PageTwo.jsx.  The gotolandingPage(), gotoFeelingLucky(), and state variables of index.jsx are passed to the PageTwo component.  Note that Index.js is just the React representation of the JSX code from Index.jsx. <br /> <br />
+ **NAME:** gotolandingPage = () => {}
+ **DESCRIPTION:** This function indicates that the user should be on the first page by setting the state boolean variables landingPage to true and secondPageState to false.  Once these state variables change, the render function will execute and choose what component to show based on these variables.
+ **NAME:** gotoPageTwoState = () => {}
+ **DESCRIPTION:** <br /> <br />
+ **NAME:** gotoFeelingLucky = () => {}
+ **DESCRIPTION:** <br /> <br />
+ **NAME:** handleTextChange = () => {}
+ **DESCRIPTION:** <br /> <br />


