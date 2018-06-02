var query = window.location.search.substring(1);
var qs = parse_query_string(query);
device = qs.device;
org = qs.org;

var config = {
	apiKey : "AIzaSyC0tTndtkaYWnJghVIwvSPJ7Mo8CypG0HI",
	authDomain : "wd-feedback.firebaseapp.com",
	databaseURL : "https://wd-feedback.firebaseio.com",
	projectId : "wd-feedback",
	storageBucket : "wd-feedback.appspot.com",
	messagingSenderId : "625605571670"
};

function parse_query_string(query) {
	console.log(query);
	var vars = query.split("&");
	var query_string = {};
	for (var i = 0; i < vars.length; i++) {
		var pair = vars[i].split("=");
		// If first entry with this name
		if (typeof query_string[pair[0]] === "undefined") {
			query_string[pair[0]] = decodeURIComponent(pair[1]);
			// If second entry with this name
		} else if (typeof query_string[pair[0]] === "string") {
			var arr = [ query_string[pair[0]], decodeURIComponent(pair[1]) ];
			query_string[pair[0]] = arr;
			// If third or later entry with this name
		} else {
			query_string[pair[0]].push(decodeURIComponent(pair[1]));
		}
	}
	return query_string;
}

function closeWindow() {
	console.log("Closing");
	window.open('', '_parent', '');
	window.close();

}

function refresh() {
	location.reload();
}
