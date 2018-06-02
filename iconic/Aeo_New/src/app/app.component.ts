import { Component ,ViewChild} from '@angular/core';
import { Nav,Platform } from 'ionic-angular';
import { StatusBar } from '@ionic-native/status-bar';
import { SplashScreen } from '@ionic-native/splash-screen';

import { LoginPage } from '../pages/login/login';
import { HomePage } from '../pages/home/home';
import { MyshirtsPage } from '../pages/myshirts/myshirts';
import { MyimgcloudPage } from '../pages/myimgcloud/myimgcloud';
import { ContactusPage } from '../pages/contactus/contactus';
import { HowtousePage } from '../pages/howtouse/howtouse';


@Component({
  templateUrl: 'app.html'
})

export class MyApp {
  @ViewChild(Nav) nav: Nav;

  rootPage:any = LoginPage;
  pages: Array<{title: string, component: any}>;
 
  constructor(platform: Platform, statusBar: StatusBar, splashScreen: SplashScreen) {
    platform.ready().then(() => {
      statusBar.styleDefault();
      splashScreen.hide();
    });

this.pages=[
{title: 'Select product', component: HomePage},
{title: 'My shirts', component: MyshirtsPage},
{title: 'My image cloud', component: MyimgcloudPage},
{title: 'How to use', component: HowtousePage},
{title: 'Contact us', component: ContactusPage}
]
  }

 openPage(page) {
            this.nav.setRoot(page.component);
  }

 logout() {
        this.nav.setRoot(LoginPage);
  }

}

