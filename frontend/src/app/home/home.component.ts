import { Component, OnInit, ViewChild } from '@angular/core';
import { FormBuilder, FormGroup, Validators } from '@angular/forms';
import { MatSnackBar } from '@angular/material/snack-bar';
import { AIResponse, Computer, Preferences } from '../models.module';
import { HomeService } from './home.service';
import { computersResolver } from './computers.resolver';
import { ActivatedRoute, Route } from '@angular/router';
import { HostListener } from '@angular/core';
import { MatStepper } from '@angular/material/stepper';
import { MatSidenav } from '@angular/material/sidenav';

@Component({
  selector: 'app-home',
  templateUrl: './home.component.html',
  styleUrl: './home.component.css'
})
export class HomeComponent implements OnInit {
  @ViewChild('stepper') stepper!: MatStepper;
  @ViewChild('sidenav') sidenav!: MatSidenav;


  aiResponses: AIResponse[] = [];
  computers: Computer[] = [];

  budgetFormGroup: FormGroup;
  usageFormGroup: FormGroup;
  chipsetFormGroup: FormGroup;
  wifiFormGroup: FormGroup;

  cols!: number;
  isLoading: boolean = false;
  opened: boolean = false;


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

      this.budgetFormGroup = this.formBuilder.group({
        budget: [, Validators.required]
      });
      this.usageFormGroup = this.formBuilder.group({
        usage: ['', Validators.required]
      });
      this.chipsetFormGroup = this.formBuilder.group({
        chipset: ['', Validators.required]
      });
      this.wifiFormGroup = this.formBuilder.group({
        need_wifi: [true, Validators.required]
      });
  
      this.onResize(); 
    }

  ngOnInit(): void {
    // this.getAIResponses();
    this.getComputers();
  }

  @HostListener('window:resize', ['$event'])
  onResize(event?: Event): void {
    this.cols = window.innerWidth <= 768 ? 1 : 2;
  }

  // getAIResponses() {
  //   this.homeService.getAIResponses().subscribe((data) => {
  //     this.aiResponses = data;
  //   })
  // }

  getComputers() {
    this.homeService.getComputers().subscribe((data) => {
      this.computers = data;
      this.isLoading = false;
    });
  }


  onSubmit(): void {
    if (
      this.budgetFormGroup.valid &&
      this.usageFormGroup.valid &&
      this.chipsetFormGroup.valid &&
      this.wifiFormGroup.valid
    ) {
      const budget = this.budgetFormGroup.value.budget;
      const chipset = this.chipsetFormGroup.value.chipset;
      const need_wifi = this.wifiFormGroup.value.need_wifi;
      const usage = this.usageFormGroup.value.usage;

      this.isLoading = true;

      this.homeService.createPreference(budget, chipset, need_wifi, usage).subscribe({
        next: (newPreference: Preferences) => {
          this.budgetFormGroup.reset();
          this.usageFormGroup.reset();
          this.chipsetFormGroup.reset();
          this.wifiFormGroup.reset();
          this.stepper.reset();

          this.homeService.createComputer(newPreference.id!).subscribe({
            next: () => {
              this.getComputers();
              this.snackBar.open('Computer created successfully!', '', { duration: 2000 });
            },
            error: () => {
              this.snackBar.open('Failed to create computer!', '', { duration: 2000 });
              this.isLoading = false;
            }
          });
        },
        error: () => {
          this.snackBar.open('Failed to create preference!', '', { duration: 2000 });
          this.isLoading = false;
        }
      });
    } else {
      this.snackBar.open('Form is invalid!', '', { duration: 2000 });
      this.isLoading = false;
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
