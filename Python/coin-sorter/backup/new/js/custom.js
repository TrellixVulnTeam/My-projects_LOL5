url = $("#urlinput").val("http://192.168.1.100:8080")

image_load = null

function start() {
	console.log("start")
	$("#start").hide();
	$("#loding").show();
	url = $("#urlinput").val()
	 $.ajax({
	 	url: "calibration_edge.py?url="+url, 
	 	success: function(result){
        	console.log(result)
        	if(result.status ==200){
				utility(result.count)
        	}
    	},error:function(result){
    		console.log("error")
    		console.log(result)
    		$("#loding").hide();
    		$("#start").show();
    		alert("check your internet and camera is conncted, restart the camera app !!")
    	}
	});
}

function main(){
	 $.ajax({
	 	url: "main.py?url="+url, 
	 	success: function(result){
	    	if(result.status ==200){
	    		console.log(result)
	    	}
		},error:function(result){
			console.log("error")
			console.log(result)
		}
	 });
main_cnrlr()
}

function stop(){
	console.log("stop");
    $("#coins").hide();
	$("#loding").show();
 $.ajax({
	 	url: "index.py?method=stop", 
	 	success: function(result){
        	console.log(result);
        	stop_cnrlr();
    	},error:function(result){
    		console.log("error")
    		console.log(result)
    	}
	});
}

function utility(count){
	if(count == 4){
		$("#continueutil").show();
		$("#edgeinfo").hide();
	}
	else{
		$("#continueutil").hide();
		$("#edgeinfo").show();
	}
	d = new Date();
	$("#loding").hide();
	$("#utility_img").attr("src" ,"./util_img.png?"+d.getTime())
	$("#utility").show();
}

function main_cnrlr(){
	$("#start").hide();
	$("#stop").show();
	$("#utility").hide();
	$("#coins").show();
}

function stop_cnrlr(){
	$("#loding").hide();
	$("#stop").hide();
	$("#start").show();
}
