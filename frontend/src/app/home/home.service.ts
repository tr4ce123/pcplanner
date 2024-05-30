import { HttpClient, HttpHeaders } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { Observable } from 'rxjs';
import { AIResponse, Computer, Preferences } from '../models.module';

@Injectable({
  providedIn: 'root'
})
export class HomeService {

  apiUrl = 'http://localhost:8000/api/';

  constructor(protected http: HttpClient) { }

  getPreferences(): Observable<Preferences[]> {
    return this.http.get<Preferences[]>(this.apiUrl + 'preferences');
  }

  createPreference(budget: number): Observable<Preferences> {
    return this.http.post<Preferences>(this.apiUrl + 'preferences/', {budget})
  }

  getAIResponses(): Observable<AIResponse[]> {
    return this.http.get<AIResponse[]>(this.apiUrl + 'chatgpt');
  }

  createAIResponse(preferenceId: number): Observable<any> {
    return this.http.post<any>(this.apiUrl + 'chatgpt/', { preferenceId })
  }

  getComputers(): Observable<Computer[]> {
    return this.http.get<Computer[]>(this.apiUrl + 'computers');
  }
}


