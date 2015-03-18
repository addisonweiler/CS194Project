# CS194 Project - Lowdown
Addison Weiler, April Yu, Sean Scott

Packages Used
-------------

User Testing
------------

File Structure
--------------
    CS194Project/Lowdown_Backend/Lowdown/static/
The directory where CSS files, images, and JS files (Excluding quiz_score) are contained. Images used in our quiz, such as the logos and the “Share” button, are all stored here.

    CS194Project/Lowdown_Backend/Lowdown/static/quiz.js
The main file where all javascript for the quiz page is housed. A few different elements are controlled from this file, including the progress bar, instant feedback for question selections, fading out of questions, and error handling / timeout handling. As a user progresses through the quiz, the progress bar is updated, and questions fade in and out. A running score is calculated as well, and is shown when the user reaches the end of the quiz.

    CS194Project/Lowdown_Backend/Lowdown/static/home.js
The file for controlling the overlay when a quiz is being generated. Loads a new page when any friend is clicked on, and starts the generation of a quiz on the fly. 

---------------------------------------------------------------------

    CS194Project/Lowdown_Backend/Lowdown/Facebook_App/
The main directory for the project files. All paths from here on out are relative to this directory. Other folders were simply used for Django / AWS configuration. The only exception to this is the “static” folder where js and css scripts (+ images) are stored.


    ./generate_quiz.py
The main file for generating a quiz and rendering the quiz page. Here, the types and quantities of each question are specified and rendered as HTML when a request is made to /Facebook_App/quiz. In addition, this file is where the call is made to Facebook’s Graph API through utils.py to pull data down on the subject of the quiz.

    ./utils.py
The main file for making requests to Facebook’s Graph API. Multithreading was used to pull down data, and one thread was used per field needed from the user (Locations, statuses, etc.) 

    ./views.py
The main file used by Django as our view controller. Through views.py, 5 urls were specified: home, about, quiz, blank_quiz, and quiz_score. Home is our homepage, and checked to make sure users were logged in. About renders our “About us” page. When Quiz, as mentioned in generate_quiz.py, is called, generate_quiz.py is called to generate a quiz. Blank_quiz is used for UI purposes: the user will be redirected to a loading page while the quiz is being loaded. Finally, quiz_score will display the user’s score after a quiz has been taken, and will give them the option to post on their friend’s Facebook Timeline. 

---------------------------------------------------------------------

    ./questions/
The directory for all the question types and their generating logic. All questions build off of questions.py, and import either MultipleChoiceQuestion or PhotoMultipleChoiceQuestion from it. In addition, supporting files for question generation are located in this directory.

    ./questions/color_shirt_question.py
    ./questions/point_cluster.py
These files together are responsible for creating the color_shirt question. Photos from Facebook are first pulled and analyzed using Pillow, a fork of the Python Image Library (PIL). Samples from each photo are taken, both of the subject’s shirt color and their skin tone, in the shape of a “plus” pattern for variety. Once these samples are collected, they are clustered into 5 clusters each using functions from point_cluster.py. Once this step is done, the cluster from the shirt_colors array that resembles the most likely skin color of the subject (Gleaned from the skin_colors array) is removed. The most worn color is then returned as the correct answer.

    ./questions/most_used_word.py
    ./questions/stopwords.py
A list of common words in English that should not be considered as “most used” words for users.

    ./questions/fake_data.py
This file contains “fake” data used in a variety of questions to either provide correct or incorrect answers to the questions. We had considered generating this data dynamically, for example by pulling in data from other friends in the user’s network. This would be an important extension, but even if such an extension is implemented, fake data is still very necessary for the common case of the user that only has one friend on the app.

---------------------------------------------------------------------

**Template Structure**
	Each question is defined by a question class in ./questions/, and is rendered by a template in ./templates/. There are only 3 question templates that the questions use: a default, a default with a picture, and a custom one for the shirt-color question. This structure allows adding any question type and ensuring that it can be rendered correctly.

    ./templates/
The directory where views (and templates) are stored. Included is a folder of question templates: the default template, a photo template, and a template for the color_shirt question.

    ./templates/quiz_score.html
This file contains HTML for quiz_score along with javascript for the Facebook “Share with Friend” functionality. We needed to include the javascript in the HTML template (rather than in a separate .js file) because variables from the controller were needed for insertion into the javascript.
