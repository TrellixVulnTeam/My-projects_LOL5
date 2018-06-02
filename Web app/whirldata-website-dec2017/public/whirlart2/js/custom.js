//Global variables
var name;
var email;
var $uploadContentCrop;
var $uploadStyleCrop;
var base64content;
var base64style;
var	content_flag = false;
var style_flag = false;

var viewportwidth  = 300;
var viewportheight = 200;

if($('body').width() < 740){
	viewportwidth  = 250;
	viewportheight = 190;
}

if($('body').width() < 940){
	viewportwidth  = 250;
	viewportheight = 190;
}



// check local storage for user details
getlocalstorage();
function getlocalstorage(){
	if(localStorage.getItem("email") && localStorage.getItem("uname")){
		$('#uname').val(localStorage.getItem("uname"));
		$('#uemail').val(localStorage.getItem("email"));
	}
}

//  Upload content image and cropp function
$uploadContentCrop = $('#content-image').croppie({
	viewport : { width : viewportwidth,  height : viewportheight },
	boundary : { width : viewportwidth,	 height : viewportheight },
	showZoomer: false,
	enableOrientation: true
});
$uploadContentCrop.croppie('bind', {
	url : 'img/400x300.png'
});

$('#content-upload').on('change', function() {
	readContentFile(this);
});

function readContentFile(input) {
	if (input.files && input.files[0]) {
	
		var reader = new FileReader();
		reader.onload = function(e) {
			var tt = e.target.result.split(';');

			if(tt[0] == 'data:image/jpeg' ){
				content_flag = true;
				$('#nocont_img_info').fadeOut();
				$('#contentnxt').fadeIn();

				$uploadContentCrop.croppie('bind', {
					url : e.target.result
				});
			}else{
				$('#myerror').modal('show');
			}
		}
		reader.readAsDataURL(input.files[0]);
	}
}

//  Upload style image and cropp function

$uploadStyleCrop = $('#style-image').croppie({
		viewport : { width : viewportwidth,	height : viewportheight},
		boundary : { width : viewportwidth, height : viewportheight },
		showZoomer: false,
		enableOrientation: true
	});
$uploadStyleCrop.croppie('bind', {
	url : 'img/400x300.png'
});

$('#style-upload').on('change', function() {
	readStyleFile(this);
});


function readStyleFile(input) {
	if (input.files && input.files[0]) {
		var reader = new FileReader();
		reader.onload = function(e) {
		
		var tt = e.target.result.split(';');
		
			if(tt[0] == 'data:image/jpeg' ){
			style_flag = true;
			$('#nosty_img_info').fadeOut();
			$('#stytnxt').fadeIn();
			
			$uploadStyleCrop.croppie('bind', {
				url : e.target.result
			});
		 }
		 else{
			$('#myerror').modal('show');
		 }
		}
		reader.readAsDataURL(input.files[0]);
	}
}

// choose content image from gallary
function gallarycontentimg(src){
	content_flag = true;
	$('#nocont_img_info').fadeOut();
	$('#contentnxt').fadeIn();

	$uploadContentCrop.croppie('bind', {
		url :src
	});
}
// choose style image from gallary
function gallarystyleimg(src){
	style_flag = true;
	$('#nosty_img_info').fadeOut();
	$('#stytnxt').fadeIn();

	$uploadStyleCrop.croppie('bind', {
			url : src
	});
}

function befrajax(){
	
    if(content_flag && style_flag){
        $('#userinput').hide();
		$('#uploading').show();
		name = $('#uname').val();
		email = $('#uemail').val();
		settolocalstorage();
		finalupload();
    } 
    if(!content_flag) {
    	$('#nocont_img_info').show()
		scrolltodiv("contentdiv");
		return
      }
   if(!style_flag) {
   	 $('#nosty_img_info').show()
	 scrolltodiv("stylediv");
	 }
	
}

function settolocalstorage(){
	localStorage.setItem("email", email);
	localStorage.setItem("uname", name);
}


function finalupload(){
	if(localStorage.getItem("uname") && localStorage.getItem("email")){
		contentImageFunction();
	}
}

/*CROP CONTENT IMAGE*/
function contentImageFunction() {
	$uploadContentCrop.croppie('result', {
		type : 'canvas',
		size :{width :400 ,height:300},
		format : 'jpeg'
	}).then(function(contentImageBase64) {
		base64content =contentImageBase64;
		styleImageFunction();
   		});
}

/*CROP STYLE IMAGE*/
function styleImageFunction() {
	$uploadStyleCrop.croppie('result', {
		type : 'canvas',
		size :{width :400 ,height:300},
		format : 'jpeg'
	}).then(function(styleImageBase64) {
	    base64style =styleImageBase64;
	     ajaxCall( name, email, base64content, base64style);
  		});
}

/* Final AJAX CALL*/
function ajaxCall( uname, emailbox, contentImage, styleImage) {
	var data = new Object();
	data.username = uname;
	data.email   = email;
	data.contentImage = contentImage;
	data.styleImage = styleImage;

	var data2 = JSON.stringify(data);
	console.log(uname);
	console.log("++++++++++++++++++++++++++++++++");
	console.log(emailbox);
	console.log("++++++++++++++++++++++++++++++++");
	console.log(contentImage);
	console.log("++++++++++++++++++++++++++++++++");
	console.log(styleImage);
	$.ajax({
		url : "https://ilv3li44fd.execute-api.us-east-1.amazonaws.com/v1?action=clientRequest",
		type : "POST",
		dataType: "json",
		contentType: "application/json",
		data: data2,
		headers : {
			'Access-Control-Allow-Origin' : '*'
		},
		cache : false,
		processData : false,
		success : function(data) {
			//console.log(data);
			if(data.status == 200){
			 six(data.estimation_time,data.key,data.id);
			}
			else{
			errror();
			}
		},
		error: function(data) {       
		     	errror();
		}
	});
}

function six(min,key,id){
	$('#uploading').hide();
	$('#finished').show();
	var reslink='https://www.whirldatascience.com/whirlart2/output.html?key='+key+'&id='+id;
	$('#finishedmsg').append('<h4 class="heading">OK '+name+', Gotcha! Your WhirlArt will be generated in '+min+' mins. Check your mailbox or click <a href='+reslink+'>here</a></h4>' );
	
}

function scrolltodiv(divid){
    $('html, body').animate({
        scrollTop: $('#'+divid).offset().top
    }, 1500);
}


function reload(){
       window.location = window.location.href.split("?")[0];
}