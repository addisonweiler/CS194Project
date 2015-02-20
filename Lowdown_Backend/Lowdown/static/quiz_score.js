window.fbAsyncInit = function() {
	FB.init({
		appId      : '{{app_id}}',
		xfbml      : true,
		version    : 'v2.1'
	});
};

(function(d, s, id){
	var js, fjs = d.getElementsByTagName(s)[0];
	if (d.getElementById(id)) {return;}
	js = d.createElement(s); js.id = id;
	js.src = "//connect.facebook.net/en_US/sdk.js";
	fjs.parentNode.insertBefore(js, fjs);
}(document, 'script', 'facebook-jssdk'));

(function(){
	"use strict";
	$(document).ready(function(){
		$(".share_btn").click(function(){
			FB.ui({
				method: 'feed',
				name: "Lowdown Friend Quiz",
				link: '{{full_url}}',
				caption: 'Lowdown: The auto-generated Facebook Quiz!',
				to: '{{friend_id}}',
				description: '{{share_message}}',
				picture: 'http://revelationnow.net/wp-content/gallery/beyonce_demon_dance_face/01_angry_beyonce.jpg',
			}, function(response){});
		})
	});
}());
