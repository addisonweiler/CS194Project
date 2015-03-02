(function(){
  	"use strict";

  	$(document).ready(function(){
	    $.get(window.location.href + "/content", function(data){
	      	document.write(data);
	    });
	    window.setTimeout(function(){alert("Your quiz could not load.  Please try again");}, 10000)
  	});
}());