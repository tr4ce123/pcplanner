import { Component, OnInit, ViewChild } from '@angular/core';
import { FormBuilder, FormGroup, Validators } from '@angular/forms';
import { MatSnackBar } from '@angular/material/snack-bar';
import { AIResponse, Computer, Preferences, computerComponent } from '../models.module';
import { BuilderService } from './builder.service';
import { ActivatedRoute, Route } from '@angular/router';
import { HostListener } from '@angular/core';
import { MatStepper } from '@angular/material/stepper';
import { BreakpointObserver, Breakpoints } from '@angular/cdk/layout';
@Component({
  selector: 'app-builder',
  templateUrl: './builder.component.html',
  styleUrl: './builder.component.css'
})
export class BuilderComponent implements OnInit{
  public static Route: Route = {
    path: 'builder',
    component: BuilderComponent,
  }

  @ViewChild('stepper') stepper!: MatStepper;
  stepperOrientation: 'horizontal' | 'vertical' = 'horizontal';


  aiResponses: AIResponse[] = [];
  computers: Computer[] = [];

  budgetFormGroup: FormGroup;
  usageFormGroup: FormGroup;
  chipsetFormGroup: FormGroup;
  wifiFormGroup: FormGroup;

  cols!: number;
  isLoading: boolean = false;
  opened: boolean = false;
  // preferences: Preferences[] = [];
  
  constructor(
    private builderService: BuilderService, 
    protected formBuilder: FormBuilder,
    protected snackBar: MatSnackBar,
    private route: ActivatedRoute,
    private breakpointObserver: BreakpointObserver
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
        usage: ['']
      });
      this.chipsetFormGroup = this.formBuilder.group({
        chipset: ['']
      });
      this.wifiFormGroup = this.formBuilder.group({
        need_wifi: [true]
      });
  
      this.onResize(); 
      this.breakpointObserver.observe([Breakpoints.Handset]).subscribe(result => {
        this.stepperOrientation = result.matches ? 'vertical' : 'horizontal';
      });
  
    }

  ngOnInit(): void {
    // this.getAIResponses();
    this.getComputers();
  }

  ngOnDestroy(): void {
    this.deleteComputers();
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
    this.builderService.getComputers().subscribe((data) => {
      this.computers = data;
      this.isLoading = false;
    });
  }

  getComponentArray(components: { [key: string]: computerComponent }): computerComponent[] {
    return Object.values(components);
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

      this.builderService.createPreference(budget, chipset, need_wifi, usage).subscribe({
        next: (newPreference: Preferences) => {
          this.budgetFormGroup.reset();
          this.usageFormGroup.reset();
          this.chipsetFormGroup.reset();
          this.wifiFormGroup.reset();
          this.stepper.reset();

          this.builderService.createComputer(newPreference.id!).subscribe({
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
    this.builderService.deleteComputer(computer.id!).subscribe({
      next: () => {
        this.snackBar.open('Computer deleted successfully!', '', { duration: 2000 });
        this.getComputers();
      },
      error: () => {
        this.snackBar.open('Failed to delete computer!', '', { duration: 2000 });
      }
    });
  }

  private deleteComputers(): void {
    if (this.computers.length > 0) {
      this.computers.forEach(computer => {
        this.builderService.deleteComputer(computer.id!).subscribe({
          next: () => {}
        });
      });
    }
  }
}
