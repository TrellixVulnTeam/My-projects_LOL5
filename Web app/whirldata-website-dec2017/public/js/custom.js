$(function() {
	$("#headerContent").load("blocks/header.html");
	$("#services-mini").load("blocks/services-mini.html");
	$("#footerContent").load("blocks/footer.html");
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
	console.log(aid);
	$('html,body').animate({
		scrollTop : aid.offset().top
	}, 'slow');
}

function showMenu() {
	$(".mask").fadeIn("slow");
	$('#rightMenu').animate({
		'right' : "0" // moves right
	});
}
function hideMenu() {
	$(".mask").fadeOut("slow");
	$('#rightMenu').animate({
		'right' : "-1000" // moves right
	});
}

$(document).scroll(function() {
	var y = $(this).scrollTop();
	if (y > 300) {
		// $('.Header-BG').fadeIn();
	} else {
		// $('.Header-BG').fadeOut();
	}
});
