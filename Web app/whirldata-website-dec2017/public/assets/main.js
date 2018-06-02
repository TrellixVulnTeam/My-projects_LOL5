$(function() {
	$("#headerContent").load("blocks/header.html");
	$("#services-mini").load("blocks/services-mini.html");
	$(".footer").load("blocks/footer.html");
});

function loadJS(file) {
	var jsElm = document.createElement("script");
	jsElm.type = "application/javascript";
	jsElm.src = file;
	document.body.appendChild(jsElm);
}

function init() {
	document.head.innerHTML = document.head.innerHTML
			+ "<meta http-equiv='Content-Type' content='text/html; charset=UTF-8' />";
	document.head.innerHTML = document.head.innerHTML
			+ "<meta charset='UTF-8'>";
	document.head.innerHTML = document.head.innerHTML
			+ "<link rel='icon' href='assets/images/favicon.png' type='image/png'>";
	document.head.innerHTML = document.head.innerHTML
			+ "<link rel='stylesheet prefetch' href='assets/bootstrap.css'>";
	// DOCUMENT.HEAD.INNERHTML = DOCUMENT.HEAD.INNERHTML
	// + "<LINK REL='STYLESHEET' HREF='ASSETS/NORMALIZE.MIN.CSS'>";
	document.head.innerHTML = document.head.innerHTML
			+ "<link rel='stylesheet prefetch' href='assets/jquery.fullPage.css'> "
			+ "<link rel='stylesheet prefetch' href='css/wd.css'>";
	document.head.innerHTML = document.head.innerHTML
			+ "<meta name='viewport' content='width=device-width, initial-scale=1'>";
	if (document.body.className == "fullPage") {
		loadJS("https://alvarotrigo.com/fullPage/jquery.fullPage.min.js");
		loadJS("js/index.js");
	}

}
init();

accClass = "accordion-content";

function showAccordion(accId) {
	console.log("DDD");
	$("." + accClass).hide();
	$("#" + accId).show();

	$(".acc-indicator").html("+");
	$("#" + accId + "-indicator").html("-");

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