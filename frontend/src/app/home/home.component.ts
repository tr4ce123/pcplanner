import { Component, OnInit } from '@angular/core';
import { FormBuilder, FormGroup, Validators } from '@angular/forms';
import { MatSnackBar } from '@angular/material/snack-bar';
import { AIResponse, Computer, Preferences } from '../models.module';
import { HomeService } from './home.service';
import { computersResolver } from './computers.resolver';
import { ActivatedRoute, Route } from '@angular/router';
import { HostListener } from '@angular/core';

@Component({
  selector: 'app-home',
  templateUrl: './home.component.html',
  styleUrl: './home.component.css'
})
export class HomeComponent implements OnInit {
  aiResponses: AIResponse[] = [];
  computers: Computer[] = [];

  preferenceForm: FormGroup;
  cols!: number;


  public static Route: Route = {
    path: 'home',
    component: HomeComponent,
    resolve: { computers: computersResolver }
  }
  // preferences: Preferences[] = [];
  
  constructor(
    private homeService: HomeService, 
    protected formBuilder: FormBuilder,
    protected snackBar: MatSnackBar,
    private route: ActivatedRoute,
    ) {
      // const data = this.route.snapshot.data as {
      //   computers: Computer[];
      // };
      // this.computers = data.computers;
      // console.log('Resolved computers:', data.computers);

      this.preferenceForm = this.formBuilder.group({
        budget: [0, Validators.required],
        chipset: ['', Validators.required],
        need_wifi: [true, Validators.required],
        usage: ['', Validators.required]
      });
      this.onResize(); 
    }

  ngOnInit(): void {
    // this.getPreferences();
    // this.getAIResponses();
    this.getComputers();
  }

  @HostListener('window:resize', ['$event'])
  onResize(event?: Event): void {
    this.cols = window.innerWidth <= 768 ? 1 : 2;
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
      const chipset = this.preferenceForm.value.chipset;
      const need_wifi = this.preferenceForm.value.need_wifi;
      const usage = this.preferenceForm.value.usage;

      this.homeService.createPreference(budget, chipset, need_wifi, usage).subscribe({
        next: (newPreference: Preferences) => {
          this.preferenceForm.reset();
          
          this.homeService.createComputer(newPreference.id!).subscribe({
            next: () => {
              this.getComputers();
              this.snackBar.open('Computer created successfully!', '', { duration: 2000 });
            },
            error: () => {
              this.snackBar.open('Failed to create computer!', '', { duration: 2000 });
            }
          });
        },
        error: () => {
          this.snackBar.open('Failed to create preference!', '', { duration: 2000 });
        }
      });
    } else {
      this.snackBar.open('Form is invalid!', '', { duration: 2000 });
    }
  }

  onDelete(computer: Computer) {
    this.homeService.deleteComputer(computer.id!).subscribe({
      next: () => {
        this.snackBar.open('Computer deleted successfully!', '', { duration: 2000 });
        this.getComputers();
      },
      error: () => {
        this.snackBar.open('Failed to delete computer!', '', { duration: 2000 });
      }
    });
  }

}
