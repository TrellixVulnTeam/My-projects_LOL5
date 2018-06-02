url = $("#urlinput").val("http://192.168.1.101:8080")

image_load = null

function start() {
	console.log("start")
	$("#start").hide();
	$("#loding").show();
	url = $("#urlinput").val()
	 $.ajax({
	 	url: "index.py?method=start&url="+url, 
	 	success: function(result){
        	console.log(result)
        	if(result.status ==200){
				utility(result.url ,result.count)
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
	 	url: "index.py?method=main&url="+url, 
	 	success: function(result){
        	console.log(result)
        	if(result.status ==200){
				// main_cnrlr()
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

function utility(url,count){
	if(count == 4){
		$("#continueutil").show();
		$("#edgeinfo").hide();
	}
	else{
		$("#continueutil").hide();
		$("#edgeinfo").show();
	}
	$("#loding").hide();
	$("#utility_img").attr("src" ,"./"+url)
	$("#utility").show();
}

function main_cnrlr(){
	$("#stop").show();
	$("#utility").hide();
	$("#coins").show();
	imageReload()
}


function imageReload(){
	console.log("relod")

	image_load = setInterval(function(){ 
		d = new Date();
		width= $( window ).width()
		if(width < 760 ){
			$("#coinsimg").attr("src", "./url_img_mob.png?"+d.getTime()); 			
		}
		else{
		$("#coinsimg").attr("src", "./url_img.png?"+d.getTime()); 
	    }
	}, 2000);
}

function stop_cnrlr(){
	$("#loding").hide();
	clearInterval(image_load);
	$("#stop").hide();
	$("#start").show();
}
