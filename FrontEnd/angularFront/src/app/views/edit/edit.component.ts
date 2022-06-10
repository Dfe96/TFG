import { Component, OnInit,ViewChild } from '@angular/core';



@Component({
  selector: 'app-edit',
  templateUrl: './edit.component.html',
  styleUrls: ['./edit.component.css']
})
export class EditComponent implements OnInit {

  constructor() { }

  ngOnInit(): void {
 
  }
  deleteentireIndex(){
    console.log("DELETED")
    
    /*this.ApiService.deleteentireIndex(this.indexNameInputTodelete,).subscribe(data => {

        console.log(data)
        this.deleteResponse=data
        
    })*/
  }
  clickMethod(name: string) {
    if(confirm("Are you sure to delete "+name)) {this.deleteentireIndex()
      
    }
  }

}
