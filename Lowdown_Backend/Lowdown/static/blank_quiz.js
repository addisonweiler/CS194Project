var currentQuestion = -1
var numQuestions = -1
var prevButton;
var nextButton;
var submit;
var FADE_TIME = 1000;

function init(){
  numQuestions = document.getElementsByName("question").length
  currentQuestion = 1
  prevButton = document.getElementById("previousButton")
  nextButton = document.getElementById("nextButton")
  // submit = document.getElementById("submitbutton")
  form = document.getElementById("form")
}

function loadPopupBoxCorrect() {    // To Load the Popupbox
  $('#popup_box_correct').fadeIn(FADE_TIME);
  $('#popup_box_correct').fadeOut(FADE_TIME, ScoreAndNextQuestion());
}

function loadPopupBoxIncorrect() {    // To Load the Popupbox
  $('#popup_box_incorrect').fadeIn(FADE_TIME);
  $('#popup_box_incorrect').fadeOut(FADE_TIME, ScoreAndNextQuestion());
} 

function ScoreAndNextQuestion(){
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


(function(){
 "use strict";

 $(document).ready(function(){
  try {
   $.get(window.location.href + "/content", function(data){
     document.write(data);
     init();

     //Instant feedback
     var answers = document.getElementById("answers").value;
     var answerArr = answers.substring(1, answers.length-1).split(',');
     var scoreDiv = document.getElementById("score");
     var score = 0

     var $radiobuttons = $('input[type=radio]');
     $radiobuttons.click(function(){
      var index = currentQuestion - 1;
      if (Number(answerArr[index]) == Number(this.value)){
        score++;
        scoreDiv.innerHTML = "SCORE: " + score;
        loadPopupBoxCorrect();
      }
      else{
        loadPopupBoxIncorrect();
      }
    });
   });
 } catch(e) {
   alert("Your quiz failed to load.  Please try again.");
 }
});
}());