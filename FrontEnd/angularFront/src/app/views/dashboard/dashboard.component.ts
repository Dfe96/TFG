import { Component, OnInit } from '@angular/core';
import{ApiService} from '../../services/api/api.service';
import { Injectable } from '@angular/core';
@Component({
  selector: 'app-dashboard',
  templateUrl: './dashboard.component.html',
  styleUrls: ['./dashboard.component.css']
})
@Injectable()
export class DashboardComponent implements OnInit {
  allindex!: JSON;
  id!: string;
  index!: JSON;
  indexresult!:JSON;
  indexresult1!:any;
  indexInput!:JSON;
  idinput!: string;
  docinput!: JSON;
  constructor(
    public ApiService: ApiService,
 
    ) {}
  ngOnInit() {
    this.ApiService.getAllIndex().subscribe(data => {
      
      console.log(data)
      
      this.allindex=data
      console.log(this.allindex)
  })
    
  }
  getallindex(){
    this.ApiService.getAllIndex().subscribe(data => {
      
        console.log(data)
    })
  }
  getIndex(){
    this.ApiService.getIndex(this.index,this.id).subscribe(data => {

        console.log(data)
        this.indexresult=data
    })
  }
  postindex(){
    this.ApiService.postIndex(this.indexInput,this.idinput,this.docinput).subscribe(data => {

        console.log(data)
        this.indexresult1=data
        
    })
  }
 
}