import { Component, OnInit } from '@angular/core';
import{FormGroup,FormControl,Validators} from '@angular/forms'
import{ApiService} from '../../services/api/api.service';
import{LoginI} from '../../models/login.interface';
import { FormsModule } from '@angular/forms';
import { Router } from '@angular/router';
@Component({
  selector: 'app-login',
  templateUrl: './login.component.html',
  styleUrls: ['./login.component.css']
})
export class LoginComponent {
  user!: string;
  password!: string;

  constructor(public ApiService: ApiService, public router: Router) {}

  login() {
    const user = {email: this.user, password: this.password};
    this.ApiService.login(user).subscribe( data => {
      this.ApiService.setToken(data.token);
      this.router.navigateByUrl('dashboard');

    },
    error => {
      console.log(error);
    });
  }
}
