import { NgModule } from '@angular/core';
import { IonicPageModule } from 'ionic-angular';
import { MyshirtsPage } from './myshirts';

@NgModule({
  declarations: [
    MyshirtsPage,
  ],
  imports: [
    IonicPageModule.forChild(MyshirtsPage),
  ],
})
export class MyshirtsPageModule {}
