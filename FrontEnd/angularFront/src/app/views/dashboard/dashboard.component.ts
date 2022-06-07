import { Component, OnInit, ViewChild } from '@angular/core';
import{ApiService} from '../../services/api/api.service';
import { Injectable } from '@angular/core';
import { BreakpointObserver } from '@angular/cdk/layout';
import { MatSidenav } from '@angular/material/sidenav';
@Component({
  selector: 'app-dashboard',
  templateUrl: './dashboard.component.html',
  styleUrls: ['./dashboard.component.css']
})
@Injectable()
export class DashboardComponent implements OnInit {
  allindex!: JSON;
  public id: string="";
  index!: JSON;
  indexresult!:JSON;
  indexresult1!:any;
  indexresult2!:any;
  indexNameInput!:string;
  public indexNameInput1: string="";
  public idinput: string="";
  public idinput1: string="";
  docinput!: JSON;
  docconverted!:any;
  componentToShow: String="";
  myUsername="";
 
  public file:any =[]
  constructor(
    public ApiService: ApiService,
    private observer: BreakpointObserver,
    ) {}
  ngOnInit() {
    this.ApiService.getAllIndex().subscribe(data => {
      
      console.log(data)
      
      this.allindex=data
      console.log(this.allindex)
      this.myUsername=this.ApiService.getMyuser();

});
  
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
    this.ApiService.postIndex(this.indexNameInput1,this.idinput,this.docinput).subscribe(data => {

        console.log(data)
        this.indexresult1=data
        
    })
  }
  files: File[] = [];

  changeComponent(componentToShow) {
    console.log("mostro cambia a "+componentToShow)
    this.componentToShow = componentToShow;
  }

  onSelect(event) {
    console.log(event);
    this.files.push(...event.addedFiles);
  }

  onRemove(event) {
    console.log(event);
    this.files.splice(this.files.indexOf(event), 1);
  }
  captureFile(event):any{
    
    const filecaptured=event.target.files[0]
    this.file.push(filecaptured)
    console.log(event.target.files);

  }
  uploadFile(){
    try{
      var formData: any = new FormData();
      
      
      this.file.forEach(element => {
      //console.log(element);
      formData.append("file",element)
      
      })
      
     
      this.ApiService.postpdf(formData,this.idinput1,this.indexNameInput1).subscribe(data => {

        console.log(data)
        this.indexresult2=data
        
      })
    

    }catch(e){
      console.log('ERROR',e)
    }

  }
 
}