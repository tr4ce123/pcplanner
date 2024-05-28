import { HttpClient, HttpHeaders } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { Observable } from 'rxjs';
import { Preferences } from '../models.module';

@Injectable({
  providedIn: 'root'
})
export class HomeService {

  apiUrl = 'http://localhost:8000/api/preferences';

  constructor(protected http: HttpClient) { }

  getPreferences(): Observable<any> {
    return this.http.get<any>(this.apiUrl);
  }
}


