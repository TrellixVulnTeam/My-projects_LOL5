import { BrowserModule } from '@angular/platform-browser';
import { ErrorHandler, NgModule } from '@angular/core';
import { IonicApp, IonicErrorHandler, IonicModule } from 'ionic-angular';
import { SplashScreen } from '@ionic-native/splash-screen';
import { StatusBar } from '@ionic-native/status-bar';

import { MyApp } from './app.component';

import { LoginPage } from '../pages/login/login';
import { HomePage } from '../pages/home/home';
import { DesignPage } from '../pages/design/design';
import { MyimgcloudPage } from '../pages/myimgcloud/myimgcloud';
import { MyshirtsPage } from '../pages/myshirts/myshirts';
import { ContactusPage } from '../pages/contactus/contactus';
import { HowtousePage } from '../pages/howtouse/howtouse';

import { HttpModule } from '@angular/http';
import { FileTransfer, FileUploadOptions, FileTransferObject } from '@ionic-native/file-transfer';
import { File } from '@ionic-native/file';
import { IonicStorageModule } from '@ionic/storage'
import { Base64ToGallery } from '@ionic-native/base64-to-gallery';

@NgModule({
  declarations: [
    MyApp,
    HomePage,
    DesignPage,
    LoginPage,
    MyimgcloudPage,
    MyshirtsPage,
    HowtousePage,
    ContactusPage
  ],
  imports: [
    HttpModule,
    BrowserModule,
    IonicStorageModule.forRoot(),
    IonicModule.forRoot(MyApp)
  ],
  bootstrap: [IonicApp],
  entryComponents: [
    MyApp,
    HomePage,
    DesignPage,
    LoginPage,
    MyimgcloudPage,
    MyshirtsPage,
    ContactusPage,
    HowtousePage
  ],
  providers: [
    StatusBar,
    FileTransfer,
    FileTransferObject,
    File,
    SplashScreen,
    Base64ToGallery,
    {provide: ErrorHandler, useClass: IonicErrorHandler},
  ]
})
export class AppModule {}
