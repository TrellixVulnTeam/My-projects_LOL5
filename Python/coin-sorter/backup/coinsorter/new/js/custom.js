url = $("#urlinput").val("http://192.168.1.100:8080")


function calibrate() {
	console.log("calibrateing");
	$("#start").hide();
	$("#loding").show();
	cam_ip = $("#urlinput").val()
	 $.ajax({
	 	url: "calibration_edge.py?url="+cam_ip, 
	 	success: function(result){
        	console.log(result)
        	if(result.status ==200){
        		// alert(result.count);
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

function start(){
	$("#start").hide();
	$("#utility").hide();
	$("#loding").show();
	cam_ip = $("#urlinput").val();

	 $.ajax({
	 	contentType: "application/json",
	 	url: "main.py?url="+cam_ip, 
	 	success: function(result){
	    	if(result.status ==200){
	    		// alert(result.status);
	    		$("#loding").hide();
	    		main_cnrlr()
	    		arm_cnrlr()
	    	}
		},error:function(result){
			// alert("error");
			// alert(result.status);
		}
	 });
}


function stop(){
	
	$("#stop").hide();
	$("#coins").hide();
	$("#loding").show();

	 $.ajax({
	 	contentType: "application/json",
	 	url: "stop.py", 
	 	success: function(result){
	    	if(result.status ==200){
	    		$("#loding").hide();
	    		$("#start").show();	
	    		$("#coinsimg").attr("src" ,"");

	    	}
		},error:function(result){
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
	cam_ip = $("#urlinput").val();
	$("#stop").show();
	$("#utility").hide();
	$("#coins").show();
	d = new Date();
	$("#coinsimg").attr("src" ,cam_ip)
}


function arm_cnrlr(){
	// alert("arm  start");
	 $.ajax({
	 	contentType: "application/json",
	 	url: "armmove.py", 
	 	success: function(result){
	    	if(result.status ==200){
	    		$("#coinsimg").attr("src" ,"");
	    		$("#coins").hide();
				$("#start").show();
				$("#stop").hide();
	    	}
		},error:function(result){

		}
	 });
}

