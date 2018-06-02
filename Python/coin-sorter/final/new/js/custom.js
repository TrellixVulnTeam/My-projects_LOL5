//Reads the url value from front end (By default : 192.168.1.100:8080)
url = $("#urlinput").val("http://192.168.1.100:8080")

//Connects to camera using cam_ip and calls calibration_edge.py file
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

//on clicing start button will call main.py,on success to main_cnrlr() and arm_cnrlr() function
function start(){
	$("#start").hide();
	// $("#utility").hide();
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


//On clicking stop button will call stop.py program
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


//Function to show the image with edges detected
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

//Function to show the video feed of Uarm working
function main_cnrlr(){
	cam_ip = $("#urlinput").val();
	$("#stop").show();
	// $("#utility").hide();
	$("#coins").show();
	d = new Date();
	$("#coinsimg").attr("src" ,cam_ip)
}

//Function to call armmove.py to control uram movement
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

//On finishing calibration page refreshes to initial page
function finish_calibrate(){
	$("#utility").hide();
	$("#start").show();
}