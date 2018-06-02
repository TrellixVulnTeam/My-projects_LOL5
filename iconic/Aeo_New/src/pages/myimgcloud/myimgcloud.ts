import { Component } from '@angular/core';
import { IonicPage, NavController, NavParams } from 'ionic-angular';
import { Http } from '@angular/http';
import 'rxjs/add/operator/map';
import { Storage } from '@ionic/storage';
import { FileTransfer, FileUploadOptions, FileTransferObject } from '@ionic-native/file-transfer';
import { File } from '@ionic-native/file';


@IonicPage()
@Component({
  selector: 'page-myimgcloud',
  templateUrl: 'myimgcloud.html',
  providers: [FileTransfer, FileTransferObject, File]

})
export class MyimgcloudPage {
  posts: any ;
  galleryType = 'regular';
  constructor(public navCtrl: NavController, public navParams: NavParams,public http: Http) {
	let usertoken ='148fbba2fd80ea9258ca0eb77d16f569';
	let url  ='http://172.104.45.18/aeoalbum/api/index.php/files/read/'+usertoken;
	console.log("111"+url);
	this.fileget(url,usertoken);

}

fileget(url,usertoken){
this.http.get( url ).map( res => res.json() ).subscribe( data => {
let jsondata = data;
let keys = [];
for ( let key in jsondata ) {
keys.push( {
key: key,
value: "http://172.104.45.18/aeoalbum/api/uploads/"+usertoken+"/" + jsondata[key]
} );
}
this.posts = keys;
});
}

}
