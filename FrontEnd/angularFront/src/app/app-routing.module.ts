import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { AppComponent } from './app.component';
import { HeaderComponent } from './templates/header/header.component';
import { FooterComponent } from './templates/footer/footer.component';
import { LoginComponent } from './views/login/login.component';
import { NewComponent } from './views/new/new.component';
import { DashboardComponent } from './views/dashboard/dashboard.component';
import { EditComponent } from './views/edit/edit.component';
import { FormsModule } from '@angular/forms';

const appRoutes: Routes = [
  {path:'',redirectTo:'login',pathMatch:'full'},
  {path:'login',component:LoginComponent,pathMatch: "full"},
  {path:'dashboard',component:DashboardComponent, pathMatch: "full"},
  {path:'new',component:NewComponent, pathMatch: "full"},
  {path:'edit',component:EditComponent,pathMatch: "full"}
];

@NgModule({
  imports: [RouterModule.forRoot(appRoutes)],
  exports: [RouterModule]
})
export class AppRoutingModule { }

export const routingComponents=RouterModule.forRoot(appRoutes);