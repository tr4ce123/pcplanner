import { Component, OnInit } from '@angular/core';
import { Preferences } from '../models.module';
import { HomeService } from './home.service';

@Component({
  selector: 'app-home',
  templateUrl: './home.component.html',
  styleUrl: './home.component.css'
})
export class HomeComponent implements OnInit {

  preferences: Preferences[] = [];

  constructor(private homeService: HomeService) {}

  ngOnInit(): void {
    this.getPreferences();
  }

  getPreferences() {
    this.homeService.getPreferences().subscribe((data) => {
      this.preferences = data;
    });
  }
}
