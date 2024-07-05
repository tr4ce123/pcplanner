import { Component, OnInit } from '@angular/core';
import { FormBuilder, FormGroup, Validators } from '@angular/forms';
import { Route } from '@angular/router';
import { BuilderService } from '../builder/builder.service';
import { MatSnackBar } from '@angular/material/snack-bar';
import { Computer, Preferences, computerComponent } from '../models.module';

@Component({
  selector: 'app-easy-builder',
  templateUrl: './easy-builder.component.html',
  styleUrl: './easy-builder.component.css'
})
export class EasyBuilderComponent implements OnInit{
  showDetails: boolean = false;

  public static Route: Route = {
    path: 'easy-builder',
    component: EasyBuilderComponent,
  }

  budgetFormGroup: FormGroup;
  computers: Computer[] = [];


  constructor(
    protected formBuilder: FormBuilder,
    private builderService: BuilderService, 
    protected snackBar: MatSnackBar
  ){
    this.budgetFormGroup = this.formBuilder.group({
      budget: [, Validators.required]
    });
  }

  ngOnInit(): void {
    this.getComputers();
  }

  ngOnDestroy(): void {
    this.deleteComputers();
  }


  getComputers() {
    this.builderService.getComputers().subscribe((data) => {
      this.computers = data;
    });
  }

  getComponentArray(components: { [key: string]: computerComponent }): computerComponent[] {
    return Object.values(components);
  }

  onSubmit(): void {
    if (
      this.budgetFormGroup.valid
    ) {
      const budget = this.budgetFormGroup.value.budget;

      this.builderService.createPreference(budget, null, null, null).subscribe({
        next: (newPreference: Preferences) => {
          this.budgetFormGroup.reset();

          this.builderService.createComputer(newPreference.id!).subscribe({
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

  toggleDetails(): void {
    this.showDetails = !this.showDetails;
  }


}
