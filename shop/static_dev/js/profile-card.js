$('.profile-img').hover(
	function(){
		$("#profile-card").css("visibility", "visible").css("opacity", "1");
	},
)

$('#profile-card').mouseout(
	function(){
		$("#profile-card").css("opacity", "0").delay(300).queue(function () {$("#profile-card").css("visibility", "hidden"); $(this).dequeue();});
	},
)