(function(){
  	"use strict";

  	$(document).ready(function(){
  		try {
  			$.get(window.location.href + "/content", function(data){
      			document.write(data);
	    	});
  		} catch(e) {
  			alert("Your quiz failed to load.  Please try again.");
  		}
  	});
}());