//Global Variables
var currentQuestion = -1;
var numQuestions = -1;
var form;
var FADE_TIME = 1500; //Controls fade from question to question
var TIMEOUT_TIME = 30000;

/* Initializes variables */
function init(){
  currentQuestion = 1
  numQuestions = document.getElementsByName("question").length
  form = document.getElementById("form")
}

/* Goes to next question, fades out current one */
function nextQuestion(){
  currentQuestion++;
  if (currentQuestion > numQuestions){
    var currentQuestionId = "question_" + (currentQuestion - 1);
    $("#" + currentQuestionId).fadeOut(FADE_TIME, function(){
      form.submit()
    }); 
  }
  var currentQuestionId = "question_" + (currentQuestion - 1);
  var nextQuestionId = "question_" + currentQuestion;

  $("#" + currentQuestionId).fadeOut(FADE_TIME);
  $("#" + nextQuestionId).delay( FADE_TIME ).fadeIn(FADE_TIME);
}

/* 
* Main function 
*/
(function(){
 "use strict";
var timeout = setTimeout(function(){alert("Oops, it looks like something timed out. Please try reloading the quiz!")}, TIMEOUT_TIME);
 $(document).ready(function(){
  try {
   $.get(window.location.href + "/content", function(data){
     document.write(data);
     init();
     clearTimeout(timeout);

     //Instant feedback on right or wrong
     var answers = document.getElementById("answers").value;
     var answerArr = answers.substring(1, answers.length-1).split(',');

     var $radiobuttons = $('input[type=radio]'); //For all radio buttons
     $radiobuttons.click(function(){ //If selected
      var index = currentQuestion - 1;
      var correctAnswer = Number(answerArr[index]);
      var correctElem = document.getElementsByName("question_" + index)[correctAnswer];

      if (Number(correctAnswer) == Number(this.value)){ //Correct?
        $(correctElem).parent().css("background-color", "green").delay(FADE_TIME*5);
        nextQuestion();
      }
      else{
        //Highlight correct answer and make bad answer red
        $(this).parent().css("background-color", "red");
        $(correctElem).parent().css("background-color", "green");
        nextQuestion();
      }
    });
   })
.fail(function(jqXHR, textStatus, errorThrown) {
  if (jqXHR.status == 500){
    alert( "Loading Error, please try reloading the page!" );
  }
});
} catch(e) {
  alert("Your quiz failed to load.  Please try again.");
  document.clear();
}

});
}());