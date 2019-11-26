# ECS171 music genre classifier
This is a Music Genre Classifier built as a website for ECS 171 - Introduction to Machine Learning.
Users can enter in a song title and the result will be a predicted genre. We have split the project into 4 teams.The Data Management team that analyzed and formatted the data. The Machine Learning team used the data from the Data Management team to make the best model for classifying songs. The Front End team designed the website and its interactions to server. The Back End team answered requests from the front end team by giving a prediction for a given song in addition to putting our website on AWS. 

## Installation for Local Machine:
#### NOTE: This list should contain all of the required libraries, but there may be some additional dependencies that you need in order to run this.  If your terminal indicates that you are missing another dependency during this setup, please download the missing dependencies it indicates in order to complete the setup.
+ **Required Libraries**
+ &nbsp;&nbsp;&nbsp;&nbsp;Keras ('pip3 install keras')
+ &nbsp;&nbsp;&nbsp;&nbsp;Tensorflow ('pip3 install tensorflow')
+ &nbsp;&nbsp;&nbsp;&nbsp;Pandas ('pip3 install pandas')
+ &nbsp;&nbsp;&nbsp;&nbsp;Flask ('pip3 install flask')
+ **Insert Instructions**
+ &nbsp;&nbsp;&nbsp;&nbsp;**Step 1:** Download https://os.unil.cloud.switch.ch/fma/fma_metadata.zip
+ &nbsp;&nbsp;&nbsp;&nbsp;**Step 2:** Move all downloaded files to the Data directory
+ &nbsp;&nbsp;&nbsp;&nbsp;**Step 3:** Navigate to the Data_Management folder and run 'python3 Make_DB.py' and 'python3 makePick.py' in terminal
+ &nbsp;&nbsp;&nbsp;&nbsp;**Step 4:** Navigate to the backend folder and run 'python3 backend.py' (IMPORTANT: make sure you run it while you are in the Back_End folder or else it won't work)
+ &nbsp;&nbsp;&nbsp;&nbsp;**Step 5:** Open a new terminal tab and navigate to the Front_End folder and run 'npm install' and then 'npm start'

### Languages
+ **Front end programming languages:** JavaScript (ES6), HTML, CSS
+ **Back end programming languages:** Python (version >= 3)













