import { Component, OnInit } from '@angular/core';
import{ApiService} from '../../services/api/api.service';
@Component({
  selector: 'app-dashboard',
  templateUrl: './dashboard.component.html',
  styleUrls: ['./dashboard.component.css']
})
export class DashboardComponent implements OnInit {

  constructor(public ApiService: ApiService) {}
  ngOnInit() {
    this.getUserLogged();
  }
  getUserLogged() {
    this.ApiService.getUser().subscribe(user => {
      console.log(user);
    });
  }
}