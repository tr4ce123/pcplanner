import { HttpClient, HttpHeaders } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { Observable } from 'rxjs';
import { AIResponse, Preferences } from '../models.module';

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

  createAIResponse(preferenceId: number): Observable<AIResponse> {
    return this.http.post<AIResponse>(this.apiUrl + 'chatgpt/', { preferenceId })
  }
}


