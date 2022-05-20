import { NgModule } from '@angular/core';
import { BrowserModule } from '@angular/platform-browser';

import { AppRoutingModule,routingComponents } from './app-routing.module';
import { AppComponent } from './app.component';
import { HeaderComponent } from './templates/header/header.component';
import { FooterComponent } from './templates/footer/footer.component';
// import { LoginComponent } from './views/login/login.component';
// import { NewComponent } from './views/new/new.component';
// import { DashboardComponent } from './views/dashboard/dashboard.component';
// import { EditComponent } from './views/edit/edit.component';
import { ReactiveFormsModule,FormsModule } from '@angular/forms';
import  {HttpClientModule} from '@angular/common/http'
@NgModule({
  declarations: [
    AppComponent,
    HeaderComponent,
    FooterComponent,
    routingComponents
    // LoginComponent,
    // NewComponent,
    // DashboardComponent,
    // EditComponent
  ],
  imports: [
    BrowserModule,
    AppRoutingModule,
    ReactiveFormsModule,
    FormsModule,
    HttpClientModule
    
  ],
  providers: [],
  bootstrap: [AppComponent]
})
export class AppModule { }
