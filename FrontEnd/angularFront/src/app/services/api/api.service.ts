import { Injectable } from '@angular/core';
import {LoginI} from '../../models/login.interface';
import {ResponseI} from '../../models/response.interface';
import {HttpClient, HttpHeaders, HttpParams} from '@angular/common/http'
import{Observable} from 'rxjs';
import { CookieService } from "ngx-cookie-service";
@Injectable({
  providedIn: 'root'
})
export class ApiService {
  url:string="http://localhost:27017"
  errorMessage;
  form: any;

  constructor(private http:HttpClient,private cookies: CookieService) { }
  

  login(form: any): Observable<any> {
    return this.http.post<ResponseI>("http://127.0.0.1:8001/login", form);
    /* return this.http.post("https://reqres.in/api/login", username); */
  }

  /* login(user: any): Observable<any> {
    var formData: any = new FormData();
    formData.append("username", this.form.get('username').value);
    formData.append("password", this.form.get('password').value);
    return this.http.post('http://127.0.0.1:8000/login', formData)
    
  } */
  getAllIndex(): Observable<any> {
    return this.http.get("http://127.0.0.1:8001/allindex");
  }
  getIndex(index: any,id:any): Observable<any> {
    
    let params = new HttpParams().set("index",index).set("id", id); //Create new HttpParams
    return this.http.get("http://127.0.0.1:8001/index", {params: params});
  }
  
  register(user: any): Observable<any> {
    return this.http.post("https://reqres.in/api/register", user);
  }
  setToken(token: string) {
    this.cookies.set("token", token);
  }
  getToken() {
    return this.cookies.get("token");
  }
  getUser(user: any): Observable<any> {
    return this.http.get("http://127.0.0.1:8001/user",{
      params: { username:user }});
  }
  getUserLogged() {
    const token = this.getToken();
    // Aquí iría el endpoint para devolver el usuario para un token
  }

}
