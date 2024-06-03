import { Component, OnInit } from '@angular/core';
import { FormBuilder, FormGroup, Validators } from '@angular/forms';
import { MatSnackBar } from '@angular/material/snack-bar';
import { AIResponse, Computer, Preferences } from '../models.module';
import { HomeService } from './home.service';

@Component({
  selector: 'app-home',
  templateUrl: './home.component.html',
  styleUrl: './home.component.css'
})
export class HomeComponent implements OnInit {

  // preferences: Preferences[] = [];
  aiResponses: AIResponse[] = [];
  computers: Computer[] = [];

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
    // this.getPreferences();
    // this.getAIResponses();
    this.getComputers();
  }

  // getPreferences() {
  //   this.homeService.getPreferences().subscribe((data) => {
  //     this.preferences = data;
  //   });
  // }

  // getAIResponses() {
  //   this.homeService.getAIResponses().subscribe((data) => {
  //     this.aiResponses = data;
  //   })
  // }

  getComputers() {
    this.homeService.getComputers().subscribe((data) => {
      this.computers = data;
    });
  }


  onSubmit(): void {
    if (this.preferenceForm.valid) {
      const budget = this.preferenceForm.value.budget;
      this.homeService.createPreference(budget).subscribe((newPreference: Preferences) => {
        this.preferenceForm.reset();

        this.homeService.createComputer(newPreference.id).subscribe(() => {
          this.getComputers();
        })
      })
      this.snackBar.open('Success!', '', { duration: 2000 });
    } else {
      this.snackBar.open('Failed!', '', { duration: 2000 });
    }
  }

}
