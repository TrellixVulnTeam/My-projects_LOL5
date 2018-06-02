import { Component } from '@angular/core';
import { IonicPage, NavController, NavParams,AlertController } from 'ionic-angular';
import 'fabric';
import * as $ from 'jquery'
import { Http } from '@angular/http';
import 'rxjs/add/operator/map';
import { FileTransfer, FileUploadOptions, FileTransferObject } from '@ionic-native/file-transfer';
import { File } from '@ionic-native/file';
import { Storage } from '@ionic/storage';
import { Base64ToGallery } from '@ionic-native/base64-to-gallery';
import * as AWS from 'aws-sdk';

declare var cordova: any;
declare let fabric: any;

@IonicPage()
@Component({
selector: 'page-design',
templateUrl: 'design.html',
providers: [FileTransfer, FileTransferObject, File]

})
export class DesignPage {
storageDirectory: string = '';
txtinp:string;
public canvas;
public activcanvas;
public backcanvas;
posts: any;
imgsrc :any;
bkimg: any;
productid:any;
private imgElement;
usertoken:string;
pname:string;

constructor(public navCtrl: NavController, public navParams: NavParams, public http: Http,private transfer: FileTransfer,
private TransferObject: FileTransferObject, private file: File,private storage: Storage,private base64ToGallery: Base64ToGallery,
public alertCtrl: AlertController) {

this.storage.get( 'userToken' ).then(( usrtoken ) => {
let url  ='http://172.104.45.18/aeoalbum/api/index.php/files/read/'+usrtoken;
console.log("111"+url);
this.fileget(url,usrtoken);
this.productget();
} );
}


fileget(url,usrtoken){
this.http.get( url ).map( res => res.json() ).subscribe( data => {
let jsondata = data;
let keys = [];
for ( let key in jsondata ) {
keys.push( {
key: key,
value: "http://172.104.45.18/aeoalbum/api/uploads/" +usrtoken+ "/" + jsondata[key]
} );
}
this.posts = keys;
});
}

productget(){
this.storage.get( 'prodid' ).then(( id ) => {
console.log(id);
this.productid= id;
this.productload(id);
});
}


productload(id){
let jsonurl = "./assets/document.json"
this.http.get( jsonurl ).map( res => res.json() ).subscribe( data => {
let jsondata = data;
console.log(jsondata);
var obj = jsondata;
$.each(obj, function(key,value) {
$.each(value,function(key,value) {
console.log(value['productId']);
if(value['productId'] === id ){

let mainimg = value['main-img'];
this.pname = value['name'];
let ass = "./assets/imgs/"; 
 $( '#designarea' ).css( 'background-image', 'url( '+ass+''+mainimg+')' );
}
});
});
});
}


//canvas inittext
ionViewDidLoad() {
this.canvas = new fabric.Canvas( 'c' );
let w = window.screen.width;
let h = window.screen.height;	
this.canvas.setHeight(h/1.5);
this.canvas.setWidth(w/1.4);
this.activcanvas = this.canvas;
this.canv();
this.backcanvasinit();

$(".canvas-container").hide();
$("#backc").parent().hide();
$("#c").parent().show();

}

//back canvas inittext
backcanvasinit() {
this.backcanvas = new fabric.Canvas( 'backc' );
let w = window.screen.width;
let h = window.screen.height;	
this.backcanvas.setHeight(h/1.5);
this.backcanvas.setWidth(w/1.4);
this.canv();
}

canv(){
let w =$( window ).width();
let h= $( window ).height();
$(".canvas-container" ).css({ 
 'position': 'absolute',
'left': '0', 
'top': '0',
'right': '0',  
'bottom': '0', 
'margin': 'auto'
});
}


//show gallary
public inserttext: boolean = false;
public inittext() {
this.inserttext = !this.inserttext;
}

public buttonClicked: boolean = false;
public insetImg() {
this.buttonClicked = !this.buttonClicked;
}


//insert img
insertimg( img_id ) {
this.showdeletebox();
this.imgElement = document.getElementById( img_id );
let imgInstance = new fabric.Image( this.imgElement, {

} );
this.activcanvas.add( imgInstance );
this.activcanvas.setActiveObject( imgInstance );
//this.activcanvas.centerObject( imgInstance );
}


showdeletebox(){
console.log("deletebox");
$('.up-nav').css('display', 'none');
if(this.activcanvas.getActiveObject())
$('#deletebox').css('display', 'block');
}

//insert text
public insertext() {
this.showdeletebox();
let text = new fabric.Textbox("New text",
{ left: 20 , top: 160 ,width: 200, textAlign: 'center' ,fontSize: 24,
}
);
this.activcanvas.add(text);
this.activcanvas.allowTouchScrolling = true;
this.activcanvas.setActiveObject( text );
}

public dltactiveobject(){

console.log(this.activcanvas.getActiveObject());
if(this.activcanvas.getActiveObject()){
    this.activcanvas.remove(this.activcanvas.getActiveObject());
     }
}


saveimg(){

this.imgsrc = this.activcanvas.toDataURL("image/png");  
        AWS.config.accessKeyId = 'AKIAIZNVG4PEUM7LUMIQ';
        AWS.config.secretAccessKey = 'G5ohTw+fLc44q8hClZHj7TFLq+ugP6Z83VKNXvF7';

     var s3Bucket = new AWS.S3( { params: {Bucket: 'myBucket'} } );

 let buf = new Buffer(this.imgsrc.replace(/^data:image\/\w+;base64,/, ""),'base64')
  var data = {
    Key: "1121.png", 
    Body: buf,
    Bucket: 'wd-prahs',
    ContentEncoding: 'base64',
    ContentType: 'image/jpeg'
  };
  s3Bucket.putObject(data, function(err, data){
      if (err) { 
          console.log(JSON.stringify(err));
      } else {
         console.log('succesfully uploaded the image!');
      }
  });






/*

this.base64ToGallery.base64ToGallery(this.imgsrc, { prefix: '_img' }).then(
  res => console.log('Saved image to gallery ', res),
  err => console.log('Error saving image to gallery ', err)
);
*/
}

public showsides(){
$('.up-nav').css('display', 'none');
$('#sidebox').css('display', 'block');
$( '#sides' ).css('visibility', 'hidden');
}

public hidesides(){

$( '#sides' ).css('visibility', 'visible');
$('#sidebox').css('display', 'none');

}
public hidetext(){
$( '#sides' ).css('visibility', 'visible');
$('#deletebox').css('display', 'none');	
}

public sides(side){

let pid= this.productid
let frontimg= "./assets/imgs/"+pid+".jpg";
let backimg= "./assets/imgs/"+pid+"-back.jpg";
if('Front' == side )
{
$(".canvas-container").hide();
$("#c").parent().show();
this.activcanvas = this.canvas;
$( '#designarea' ).css( 'background-image', 'url('+frontimg+')' );
}else{
$(".canvas-container").hide();
$("#backc").parent().show();
this.activcanvas = this.backcanvas;
$( '#designarea' ).css( 'background-image', 'url('+backimg+')' );
}

}

public overlayon(){
    document.getElementById("overlay").style.display = "block";
}

public overlayoff(){
	    document.getElementById("overlay").style.display = "none";
}


}
