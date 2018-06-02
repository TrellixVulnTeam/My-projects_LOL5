import { Component } from '@angular/core';
import { IonicPage, NavController, NavParams,AlertController } from 'ionic-angular';
import {HomePage} from '../home/home';
//import * as $ from 'jquery'
import { Http } from '@angular/http';
import { Storage } from '@ionic/storage';

 @IonicPage()
	@Component({
  	selector: 'page-login',
  	templateUrl: 'login.html',
	})
 export class LoginPage {
  		data:any = {};
  		token:any;
  		constructor(public navCtrl: NavController, public navParams: NavParams,public http: Http,private alertCtrl: AlertController,private storage: Storage) {
	 this.data.username = '';
 	 this.data.pass = ''; 
 	 this.data.response = '';
 	 this.http = http;
 	 }
  
      //login

mylogin(){
	this.data.username ="mano@gmail.com";
	this.data.pass = "mano42023";
}

      submit() {
      		if(this.data.username || this.data.pass){
  			var link = 'http://172.104.45.18/aeoalbum/api/index.php/users/login';
 			var myData = JSON.stringify({userName: this.data.username,password:this.data.pass});
 			this.http.post(link, myData)
 			.subscribe(data => {
 			console.log(data['_body'] );
 			if(data['_body']){
 			this.data.response = JSON.parse(data['_body']); 
 			this.token = this.data.response.userId;
   				this.setToken(this.token);
				this.navCtrl.push(HomePage);
 			} else{
 				this.presentAlert();
	  		}
	    	}, error => {
 			});
 	  		}else{
 	  		this.presentAlert();
 	  		}
 	  }
 	 // alert 
 		presentAlert() {
  			let alert = this.alertCtrl.create({
    	 	subTitle: 'Check Your UserName or Password',
  		 	buttons: ['Dismiss']
  			});
  	  	alert.present();
		}

 		//local storage
 		setToken(token1) {
			this.storage.set( 'userToken', token1 );
			this.getToken();
		}
 		getToken() {
			this.storage.get( 'userToken' ).then(( val ) => {
			console.log(val);
			});
		}




	}
