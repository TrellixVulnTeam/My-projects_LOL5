import { Component} from '@angular/core';
import { NavController ,AlertController} from 'ionic-angular';
import { BarcodeScanner } from '@ionic-native/barcode-scanner';
import {DesignPage} from '../design/design';
import { Storage } from '@ionic/storage';

@Component({
 selector: 'page-home',
  providers: [BarcodeScanner],
 templateUrl: 'home.html'
})

export class HomePage {
	designPage = DesignPage;
     	public barcode:string;
		constructor(public navCtrl: NavController , private barcodeScanner: BarcodeScanner,private storage: Storage,private alertCtrl: AlertController ) {
   }
   

 scan(){
	this.barcodeScanner.scan().then((barcodeData) => {
		this.barcode= barcodeData.text;  
		this.godesign();
	}, (err) => {
		this.barcode=err;
	});
 }

godesign(){
if(this.barcode){
	this.setToken(this.barcode);
	this.navCtrl.push(DesignPage);
	}else{
	}
}

 setToken(prodid) {
			this.storage.set( 'prodid', prodid );
			this.getToken();
		}
getToken() {
			this.storage.get( 'prodid' ).then(( id ) => {
			console.log(id);
			});
		}


// alert 
 		presentAlert() {
  			let alert = this.alertCtrl.create({
    	 	subTitle: 'Scan or Enter Barcode',
  		 	buttons: ['Dismiss']
  			});
  	  	alert.present();
		}


		

}