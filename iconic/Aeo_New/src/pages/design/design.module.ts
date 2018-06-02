import { NgModule } from '@angular/core';
import { IonicPageModule } from 'ionic-angular';
import { DesignPage } from './design';

@NgModule({
  declarations: [
    DesignPage,
  ],
  imports: [
    IonicPageModule.forChild(DesignPage),
  ],
})
export class DesignPageModule {}
