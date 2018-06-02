import { Component,ChangeDetectorRef, Injectable} from '@angular/core';
import { NavController,Platform } from 'ionic-angular';
import { SpeechRecognition } from '@ionic-native/speech-recognition';
import { Media, MediaObject } from '@ionic-native/media';
import { File } from '@ionic-native/file';
@Injectable()


@Component({
selector: 'page-home',
templateUrl: 'home.html'
})
export class HomePage {

matches: String[];
isRecording = false;

audfile :MediaObject;
audiocount:number =1;

constructor(public navCtrl: NavController,private speechRecognition: SpeechRecognition,private cd: ChangeDetectorRef,private plt: Platform,private media: Media,private file: File) {}


// Speech to text  start

isIos() {
    return this.plt.is('ios');
  }
 
stopListening() {
    this.speechRecognition.stopListening().then(() => {
           this.isRecording = false;
    });
  }
 
languagesuprt(){
this.speechRecognition.getSupportedLanguages()
  .then(
    (languages: Array<string>) => console.log(languages),
    (error) => console.log(error) )
}

 getPermission() {
    this.speechRecognition.hasPermission()
      .then((hasPermission: boolean) => {
        if (!hasPermission) {
          this.speechRecognition.requestPermission();
        }
      });
  }


// Speech to text end


//Voice record start
startrecording(){

  this.audiocount =this.audiocount+1;
  this.audfile = this.media.create(this.file.externalRootDirectory+'recording.mp3');
  this.audfile.startRecord(); 

 let options = {
	language: 'en-US',
	showPopup : false
	}

	this.speechRecognition.startListening(options).subscribe(matches => {
			this.matches = matches;
			this.cd.detectChanges();
	 })

   if(this.matches){
     this.audfile.stopRecord();
    }
}





}

