import { Component } from '@angular/core';
import { IonicPage, NavController, NavParams } from 'ionic-angular';
import { Http } from '@angular/http';
import 'rxjs/add/operator/map';
import { Storage } from '@ionic/storage';
import { FileTransfer, FileUploadOptions, FileTransferObject } from '@ionic-native/file-transfer';
import { File } from '@ionic-native/file';


@IonicPage()
@Component({
  selector: 'page-myshirts',
  templateUrl: 'myshirts.html',
})
export class MyshirtsPage {
  posts: any ;
  drawerOptions: any;
  galleryType = 'regular';

  constructor(public navCtrl: NavController, public navParams: NavParams,public http: Http) {
this.drawerOptions = {
      handleHeight: 50,
      thresholdFromBottom: 200,
      thresholdFromTop: 200,
      bounceBack: true
    };
  
	let usertoken ='97135b9bf0ee3f8e04771ff91526c88d';
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
