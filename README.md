# CS194 Project - Lowdown
Addison Weiler, April Yu, Sean Scott


Instructions
------------
As the app is still in development mode (since it has not been fully checked for security), new users must be registered by us as app testers. Currently only Alex on the teaching staff is. Of Alex's friends on the app, I know XiaoSong has too restrictive security settings to allow quiz generation; the quiz on Sean should work however.

After being added as a tester, a user needs to confirm his/her role as a tester, and then log in to the app without a current active Facebook session (e.g. in incognito). Then the home screen will appear.

The main url is http://lowdownquiz.me

Packages Used
-------------
0. Pillow
Pillow, a fork of the Python Image Library (PIL), was used for image processing. Pillow was used to process images pulled down from Facebook, and specifically was used to getting individual pixels and their RGB values for use in color_shirt_question.py. It was also used for debugging, as it provided sufficient drawing functionality. 

0. Django
We used the web framework Django for our project. Django, combined with Amazon AWS servers, provided the framework we needed for Lowdown, and allowed us to use Python for our backend processing. 

0. Python Social Auth
We used the Python Social Auth package to authenticate Facebook users and pull data from their profiles.  This package provided an easy framework to use to accomplish this essential component of our final product.

User Testing
------------
0. Design
We used the storyboarding technique taught in CS147 to get user feedback on different design options we imagined.  These ideas were sketched out onto index cards, which allowed for easy viewing by the test users and rapid change and iteration by us.

0. Workflow
Similarly, we took the final design (based on our own aesthetic opinions and user feedback) and implemented it in our prototype.  After implementing this alpha version, we had users step through the workflow again on the computer.  This allowed them to see the transitions from one page to another, along with the fade time between pages.  From here, we gathered more feedback and used it to iterate on the design until we arrived at the final product.



File Structure
--------------
Note all links here are in the root directory of `CS194Project/Lowdown_Backend/Lowdown`

    ./static/
The directory where CSS files, images, and JS files (Excluding quiz_score) are contained. Images used in our quiz, such as the logos and the “Share” button, are all stored here.

    ./static/quiz.js
The main file where all javascript for the quiz page is housed. A few different elements are controlled from this file, including the progress bar, instant feedback for question selections, fading out of questions, and error handling / timeout handling. As a user progresses through the quiz, the progress bar is updated, and questions fade in and out. A running score is calculated as well, and is shown when the user reaches the end of the quiz.

    ./static/home.js
The file for controlling the overlay when a quiz is being generated. Loads a new page when any friend is clicked on, and starts the generation of a quiz on the fly. 

---------------------------------------------------------------------

    ./Facebook_App/
The main directory for the project files.

    ./Facebook_App/generate_quiz.py
The main file for generating a quiz and rendering the quiz page. Here, the types and quantities of each question are specified and rendered as HTML when a request is made to /Facebook_App/quiz/####. In addition, this file is where the call is made to Facebook’s Graph API through utils.py to pull data down on the subject of the quiz.

The structure of questions is highly modular and fault-tolerant. All a developer needs to do to add a question is:
0. Write a class that subclasses `MultipleChoiceQuestion` or one of its subclasses.
0. Define a method called `gen` that takes in two parameters: the `self_data` and `friend_data`, and returns an instance of the class. The `MultipleChoiceQuestion` constructor takes two arguments: a list of correct answers and a list of incorrect answers. More on that in the description of `./Facebook_App/questions/questions.py`.
0. Override the `QUESTION_TEXT` class constant to define the question text, replacing instances of the friend’s name with `%s`.
0. In `generate_quiz.py`, import the question class and add it to the `QUESTION_AMOUNTS` dict, setting the number of repetitions for that question as well.

That’s all! The generation logic catches any exception thrown as a result of the `gen` method and simply logs it as a warning. If the question class knows that it does not have the data to generate the question, it can raise a `QuestionNotFeasibleException` that logs a debug statement instead. In this way, inconsistencies in the Facebook API data returned can be gracefully handled.

    ./Facebook_App/utils.py
The main file for making requests to Facebook’s Graph API. Multithreading was used to pull down data, and one thread was used per field needed from the user (Locations, statuses, etc.) 

    ./Facebook_App/views.py
The main file used by Django as our view controller. Through views.py, 5 urls were specified: home, about, quiz, blank_quiz, and quiz_score. Home is our homepage, and checked to make sure users were logged in. About renders our “About us” page. When Quiz, as mentioned in generate_quiz.py, is called, generate_quiz.py is called to generate a quiz. Blank_quiz is used for UI purposes: the user will be redirected to a loading page while the quiz is being loaded. Finally, quiz_score will display the user’s score after a quiz has been taken, and will give them the option to post on their friend’s Facebook Timeline. 

---------------------------------------------------------------------

    ./Facebook_App/questions/
The directory for all the question types and their generating logic.

    ./Facebook_App/questions/questions.py
All questions currently supported subclass `MultipleChoiceQuestion` by some hierarchy. This class has some very convenient features, including:
* Checking that the wrong answers don’t include a right answer. Since so many questions have lists of fake/static data, they can sometimes include something that is actually the right answer. Instead of forcing all subclasses to check that they are not passing in right answers in `wrong_answers`, this class automatically removes them.
* Discarding questions that don’t have enough wrong answers, possibly as a result of the above process.
* Deduplicating right and wrong answers.
* Picking a random right answer from a list of possible right answers. Many question types have a list of possible right answers.
* Setting a template (`default.html`) and a default number of wrong answers (3).

As mentioned in the comment above for `/Facebook_App/generate_quiz.py`, any exceptions raised in this process are simply logged, and the question discarded.

    ./Facebook_App/questions/color_shirt_question.py
    ./Facebook_App/questions/point_cluster.py
These files together are responsible for creating the color_shirt question. Photos from Facebook are first pulled and analyzed using Pillow, a fork of the Python Image Library (PIL). Samples from each photo are taken, both of the subject’s shirt color and their skin tone, in the shape of a “plus” pattern for variety. Once these samples are collected, they are clustered into 5 clusters each using functions from point_cluster.py. Once this step is done, the cluster from the shirt_colors array that resembles the most likely skin color of the subject (Gleaned from the skin_colors array) is removed. The most worn color is then returned as the correct answer.

    ./Facebook_App/questions/most_used_word.py
    ./Facebook_App/questions/stopwords.py
A list of common words in English that should not be considered as “most used” words for users.

    ./Facebook_App/questions/fake_data.py
This file contains “fake” data used in a variety of questions to either provide correct or incorrect answers to the questions. We had considered generating this data dynamically, for example by pulling in data from other friends in the user’s network. This would be an important extension, but even if such an extension is implemented, fake data is still very necessary for the common case of the user that only has one friend on the app.

---------------------------------------------------------------------

**Template Structure**
	Each question is defined by a question class in ./questions/, and is rendered by a template in ./templates/. There are only 3 question templates that the questions use: a default, a default with a picture, and a custom one for the shirt-color question. This structure allows adding any question type and ensuring that it can be rendered correctly.

    ./Facebook_App/templates/
The directory where views (and templates) are stored. Included is a folder of question templates: the default template, a photo template, and a template for the color_shirt question.

    ./Facebook_App/templates/quiz_score.html
This file contains HTML for quiz_score along with javascript for the Facebook “Share with Friend” functionality. We needed to include the javascript in the HTML template (rather than in a separate .js file) because variables from the controller were needed for insertion into the javascript.
