import { HttpClient, HttpHeaders } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { Observable } from 'rxjs';
import { AIResponse, Computer, Preferences } from '../models.module';

@Injectable({
  providedIn: 'root'
})
export class HomeService {

  // apiUrl = 'https://pcplanner-production.up.railway.app/api/';
  apiUrl = 'http://127.0.0.1:8000/api/';

  constructor(protected http: HttpClient) { }

  getPreferences(): Observable<Preferences[]> {
    return this.http.get<Preferences[]>(this.apiUrl + 'preferences');
  }

  createPreference(budget: number, chipset: string): Observable<Preferences> {
    return this.http.post<Preferences>(this.apiUrl + 'preferences/', { budget, chipset })
  }

  // getAIResponses(): Observable<AIResponse[]> {
  //   return this.http.get<AIResponse[]>(this.apiUrl + 'chatresponses');
  // }

  // createAIResponse(preference: Preferences): Observable<any> {
  //   return this.http.post<any>(this.apiUrl + 'chatresponses/',{ preferences: preference })
  // }

  createComputer(preferences_id: number): Observable<Computer> {
    return this.http.post<Computer>(this.apiUrl + 'computers/', { preferences_id })
  }

  getComputers(): Observable<Computer[]> {
    return this.http.get<Computer[]>(this.apiUrl + 'computers');
  }

  deleteComputer(id: number): Observable<any> {
    return this.http.delete(this.apiUrl + 'computers/' + id);
  }
}


