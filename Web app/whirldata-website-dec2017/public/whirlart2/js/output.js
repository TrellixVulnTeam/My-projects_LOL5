var s3url = "https://s3.amazonaws.com/";

/* check param RESULT*/
var getUrlParameter = function getUrlParameter(sParam) {
    var sPageURL = decodeURIComponent(window.location.search.substring(1)),
        sURLVariables = sPageURL.split('&'),
        sParameterName,
        i;

    for (i = 0; i < sURLVariables.length; i++) {
        sParameterName = sURLVariables[i].split('=');

        if (sParameterName[0] === sParam) {
            return sParameterName[1] === undefined ? true : sParameterName[1];
        }
    }
};

var key = getUrlParameter('key');
if (key == 'whirlart-images'){

var bucketname =  getUrlParameter('key');
var foldername =  getUrlParameter('id');
var contenturl = s3url+bucketname+'/'+foldername+'/contentImage.jpg';
var styleurl   = s3url+bucketname+'/'+foldername+'/styleImage.jpg';
var resultimg  = s3url+bucketname+'/'+foldername+'/processedImage.jpg';

		$('#fcontent').attr('src',contenturl);
		$('#fstyle').attr('src',styleurl);
		$('#fresult').attr('src',resultimg);
		$('#downloadres').attr('href',resultimg);

	    $("meta[name='fbimage']").attr("content", resultimg);
	    $("meta[name='twitter\\:image']").attr('content', resultimg);
}
function reload(){
       window.location = "https://whirldatascience.com/whirlart2";
}


window.fbAsyncInit = function() {
    FB.init({
        appId            : '172807293348238',
        status           : true,
        cookie           : true,
        version          : 'v2.10'                
    });
    
    $( '#fbshareclick' ).click(function(e){
        e.preventDefault();
        var resurl      = window.location.href;
        var image = $('#fresult').attr('src');
        var uname = localStorage.getItem("uname");
        FB.ui({
        method: 'share_open_graph',
        action_type: 'og.shares',
        display: 'popup',
        action_properties: JSON.stringify({
        object: {
        'og:url': resurl,
        'og:title': 'WhirlArt',
        'og:description': 'I created a awesome art using WhirlArt ',
        'og:image': image
    }
    })
     },
      function(response){});
})
};

(function(d, s, id){
    var js, fjs = d.getElementsByTagName(s)[0];
    if (d.getElementById(id)) {return;}
    js = d.createElement(s); js.id = id;
    js.src = "//connect.facebook.net/en_US/sdk.js";
    fjs.parentNode.insertBefore(js, fjs);
}(document, 'script', 'facebook-jssdk'));

$('#fresult').on('error', function(){
  $('#resultstart').hide();
  $('#fresult').hide();
    $('#loadingres').show();

});

