var currentQuestion = 0;
var currentQuestionTitle="";
powerBiApi = "https://api.powerbi.com/beta/449b3784-97bd-445c-9e13-ae4779649caa/datasets/f4059488-1228-48ab-a3e0-da6bb0ad3e2e/rows?key=lPRTjQ0la%2BvHFNbcMHzVe9YFjfA6T1DwR0W3HjE4H2xiEqQ2tpC88E9rBB1ywR%2FvQvjQxBbMyOqop8Y8IFjFXQ%3D%3D";

if (localStorage.getItem("pairId") == null) {
	var dt = new Date();
	var time = Date.now();
	localStorage.setItem("pairId", time);
}

function logout() {
	localStorage.removeItem("pairId");
	firebase.database().ref(org+"/devices/"+device).set({
		isEnabled : false
	});
	console.log("Completed");
	application.delete();
}

application = firebase.initializeApp(config);
var database = firebase.database();
userCheck();

console.log("uuu=?> " + localStorage.getItem("currentUsername"));
function userCheck() {
	if (localStorage.getItem("currentUsername")) {
		var checkEnable = firebase.database().ref(org+"/devices/" + device);
		checkEnable.once(('value'), function(data) {
			isEnabled = data.child("isEnabled").val();
			pairId = data.child("pairId").val();
			console.log("PairID=> " + pairId);
			console.log("Is enabled=> " + isEnabled)
			if (pairId != null && pairId != localStorage.getItem("pairId")) {
				application.delete();
				console.log("Stopped");
				$("#wait").show()
			} else
				init();
		});

	} else {
		var currentUsername = prompt("Enter current user name", "Muthu");
		localStorage.setItem("currentUsername", currentUsername);
		userCheck();
	}
}

var query = firebase.database().ref(org+"/devices/" + device);
query.on("value", function(snapshot) {
	console.log($("#userName").html());
	currentUsername = snapshot.child("currentUsername").val();
	isEnabled = snapshot.child("isEnabled").val();
	currentQuestion = snapshot.child("currentQuestion").val();
	if (currentUsername == null)
		currentUsername = localStorage.getItem("currentUsername");
	pairId = snapshot.child("pairId").val();
	if (pairId == localStorage.getItem("pairId")) {
		$("#userName").show();
		$("#userName").html("Hi " + currentUsername);
		loadOptions(currentQuestion);
	} else {
		$("#userName").html("");
		// $("#responses").hide();
	}
});

function loadOptions(questionNumber) {
	$("#responses").html("");
	console.log(org+"/questions/q" + questionNumber + "/options");

	var questionsQuery = firebase.database().ref(
			"org1/questions/q" + questionNumber );
	questionsQuery.on("value", function(question) {
		if (question.val() == null) {
			console.log("NO QUESTION FOUND");
			logout();
			$("#thankYou").show();
			return;
		}else{
			console.log("QUESTION FOUND");
			localStorage.setItem("questionTitle",question.child("title").val());
			console.log("QUESTION SET");
			options=question.child("options");
			for (i = 1; i <= 4; i++) {
				if (options.child("o" + i).val() != null){
					showOptions(i, options.child("o" + i).val());
					localStorage.setItem("option"+i, options.child("o" + i).val());
				}
			}

			$("#responses").show();
		}
	});


}

function showOptions(optionNumber, value) {
	console.log(optionNumber + ". " + value);
	$("#responses").append(
			"<button  class='answer-btn col-sm-6 col-xs-6 btn btn-primary btn-"
					+ optionNumber + "' onclick=next();sendToPowerBi('"+optionNumber+"')>" + optionNumber
					+ "</button>");
	// $("#option" + optionNumber).show();
}




function next() {

	init();
}

function init() {

	console.log('device: ' + device + ", org: " + org);

	firebase.database().ref("org1/devices/device1").set({
		isEnabled : true,
		pairId : localStorage.getItem("pairId"),
		currentQuestion : currentQuestion + 1,
		currentUsername : localStorage.getItem("currentUsername")
	});

	console.log("Completed");
}


function sendToPowerBi(optionNumber) {
	console.log("Q=> "+localStorage.getItem("questionTitle")+", A=> "+optionNumber);

	var req = [ {
		"user" : localStorage.getItem("currentUsername"),
		"question" : localStorage.getItem("questionTitle"),
		"answer" : localStorage.getItem("option"+optionNumber),
		"deviceId":"1",
		"orgId":"1",
		"questionNumber":currentQuestion-1

	} ];

	$.ajax({
		type : "POST",
		url : powerBiApi,
		data : JSON.stringify(req),
		contentType : "application/json; charset=utf-8",
		dataType : "json",
		success : function(data) {
			alert(data);
		},
		failure : function(errMsg) {
			alert(errMsg);
		}
	});
}
