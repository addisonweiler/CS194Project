/*
When a friend is clicked, pops up the loader and 
sends a signal to load the quiz.
*/
(function() {
	"use strict";
	$(document).ready(function(){
		$(".quiz_btn").click(function(){
			$.get($(this).attr("data-href"), function(data) {
				document.write(data);
			});
			$("#loader").removeClass("hidden");
		});
	});
}());
