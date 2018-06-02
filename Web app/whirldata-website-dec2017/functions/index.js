const
functions = require('firebase-functions');

const
admin = require('firebase-admin');
admin.initializeApp(functions.config().firebase);

exports.whirlbotLog = functions.https.onRequest((req, res) => {
	const text = req.query.text;
	const botName = req.query.botName;
	return admin.database().ref('/whirlbot/'+botName+'/log').push({msg: text}).then((snapshot) => {
		res.status(200).send("done");
	});
});

exports.whirlbotSuccessLog = functions.https.onRequest((req, res) => {
	const text = req.query.text;
	const botName = req.query.botName;
	return admin.database().ref('/whirlbot/'+botName+'/successLog').push({msg: text}).then((snapshot) => {
		res.status(200).send("done");
	});
});

exports.whirlbotFailLog = functions.https.onRequest((req, res) => {
	const text = req.query.text;
	const botName = req.query.botName;
	return admin.database().ref('/whirlbot/'+botName+'/failLog').push({msg: text}).then((snapshot) => {
		res.status(200).send("done");
	});
});

exports.backupLog = functions.https.onRequest((req, res) => {
	const botName = req.query.botName;
	
	var logRef = admin.database().ref('/whirlbot/');
	logRef.child(botName).once('value').then(function(snap) {
	  var data = snap.val();
	  return admin.database().ref('/whirlbot/'+botName+'-bk').push(data).then((snapshot) => {
		  var botLogRef = admin.database().ref('/whirlbot/'+botName);
		  botLogRef.remove(function (error) {
			    if (!error) 
			    	res.status(200).send("done");
			    else
			    	res.status(200).send("Failed "+error);
			});
			
		});
	});
});