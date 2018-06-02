$(function() {
	$("#headerContent").load("blocks/header.html");
	$("#services-mini").load("blocks/services-mini.html");
});
accClass = "accordion-content";
function showAccordion(accId) {
	console.log("DDD");
	$("." + accClass).hide();
	$("#" + accId).show();

	$(".acc-indicator").html("+");
	$("#" + accId + "-indicator").html("-");

}

function scrollToAnchor(aid) {
	$('html,body').animate({
		scrollTop : aid.offset().top
	}, 'slow');
}
var i = 1;
$(document).keydown(function(event) {
console.log("DD");
	if (event.keyCode == 38) {
		i++;
		scrollToAnchor($("#section" + i + ""));
	} else if (event.keyCode == 40) {
		i--;
		event.preventDefault();
		scrollToAnchor($("#section" + i + ""));
	}
});