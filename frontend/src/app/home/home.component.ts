import { Component, OnInit } from '@angular/core';
import { FormBuilder, FormGroup, Validators } from '@angular/forms';
import { MatSnackBar } from '@angular/material/snack-bar';
import { AIResponse, Preferences } from '../models.module';
import { HomeService } from './home.service';

@Component({
  selector: 'app-home',
  templateUrl: './home.component.html',
  styleUrl: './home.component.css'
})
export class HomeComponent implements OnInit {

  preferences: Preferences[] = [];
  aiResponses: AIResponse[] = [];

  preferenceForm: FormGroup;

  constructor(
    private homeService: HomeService, 
    protected formBuilder: FormBuilder,
    protected snackBar: MatSnackBar
    ) {
      this.preferenceForm = this.formBuilder.group({
        budget: [0, Validators.required]
      });  
    }

  ngOnInit(): void {
    this.getPreferences();
    this.getAIResponses();
  }

  getPreferences() {
    this.homeService.getPreferences().subscribe((data) => {
      this.preferences = data;
    });
  }

  getAIResponses() {
    this.homeService.getAIResponses().subscribe((data) => {
      this.aiResponses = data;
    })
  }

  onSubmit(): void {
    if (this.preferenceForm.valid) {
      const budget = this.preferenceForm.value.budget;
      this.homeService.createPreference(budget).subscribe((newPreference: Preferences) => {
        this.preferences.push(newPreference);
        this.preferenceForm.reset();

        this.homeService.createAIResponse(newPreference.id).subscribe((newAIResponse: AIResponse) => {
          this.aiResponses.push(newAIResponse);
        })
      })
      this.snackBar.open('Success!', '', { duration: 2000 });
    } else {
      console.log('Form is invalid');
    }
  }

}
