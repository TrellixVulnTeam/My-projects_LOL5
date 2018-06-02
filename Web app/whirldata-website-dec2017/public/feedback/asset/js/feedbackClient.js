

function loadQuestions(questionNumber) {
	$(".answers").hide();
	var query = firebase.database().ref(org + "/questions/q" + questionNumber);
	query.on("value", function(snapshot) {
		title = snapshot.child("title").val();
		$("#question").html(title);
	});
	console.log("org1/questions/q" + questionNumber + "/options");
	var optionsQuesry = firebase.database().ref(
			"org1/questions/q" + questionNumber + "/options");

	optionsQuesry.on("value", function(options) {
		console.log(options.val())
		$("#options").html("");
		for (i = 1; i <= 4; i++) {
			if (options.child("o" + i).val() != null)
				showOptions(i, options.child("o" + i).val());
		}

	});
}

function showOptions(optionNumber, value) {
	$("#options").append(
			"<h2 class='well col-sm-6 btn-" + optionNumber + "'>"
					+ optionNumber + ". " + value + "</h2>");
}

$("#userName").html("");
var query = window.location.search.substring(1);
var qs = parse_query_string(query);
deviceId = qs.device;
var currentUsername = null;
var deviceStatus = "1";
// Initialize Firebase
console.log
application = firebase.initializeApp(config);

var introQuery = firebase.database().ref(org);
introQuery.on("value",
		function(snapshot) {
			storeName = snapshot.child("orgName").val();
			logo = snapshot.child("logo").val();
			devicePathPrefix = snapshot.child("devicePathPrefix").val();
			promoImage = snapshot.child("promoImage").val();
			$("#storeName").html(storeName);
			$("#logo").attr('src', logo);
			$('#qrcode').html("");
			$('#qrcode').qrcode(
					devicePathPrefix + "?org=" + org + "&device=" + deviceId);
			$("#promoImage").attr('src', promoImage);

		});

var defaultDatabase = firebase.database();
var query = firebase.database().ref(org + "/devices/" + deviceId);
query.once("value").then(function(snapshot) {
	currentUsername = snapshot.child("currentUsername").val();
	isEnabled = snapshot.child("isEnabled").val();
	console.log(currentUsername);
});

i = 0;
query.on("value", function(snapshot) {
	currentUsername = snapshot.child("currentUsername").val();
	isEnabled = snapshot.child("isEnabled").val();
	currentQuestion = snapshot.child("currentQuestion").val();
	if (isEnabled && currentUsername != null) {
		$("#userName").html("Hi " + currentUsername + "!");
		loadQuestions(currentQuestion);
		$("#responses").show();
		$(".qrcode").hide();
	} else {
		$("#userName").html("");
		$("#responses").hide();
		$("#answers").hide();
		$(".qrcode").show();
	}
});