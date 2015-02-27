(function(){
  	"use strict";

  	$(document).ready(function(){
	    $.get(window.location.href + "/content", function(data){
	      	document.write(data);
	    });
  	});
}());