import { Component, OnInit } from '@angular/core';
import { FormBuilder, FormGroup, Validators } from '@angular/forms';
import { Route } from '@angular/router';
import { BuilderService } from '../builder/builder.service';
import { MatSnackBar } from '@angular/material/snack-bar';
import { Computer, Preferences, computerComponent } from '../models.module';
import { trigger, state, style, transition, animate, query, stagger } from '@angular/animations'

@Component({
  selector: 'app-easy-builder',
  templateUrl: './easy-builder.component.html',
  styleUrl: './easy-builder.component.css',
  animations: [
    trigger('listAnimation', [
      transition('* => *', [
        query(':enter', [
          style({ opacity: 0 }),
          stagger(200, [
            animate('1s', style({ opacity: 1 }))
          ])
        ], { optional: true })
      ])
    ]),
    trigger('fadeIn', [
      transition(':enter', [ // On enter
        style({ opacity: 0 }),
        animate('1s', style({ opacity: 1 })) // Fade in over 1 second
      ])
    ])
  ]
})

export class EasyBuilderComponent implements OnInit{
  showDetails: boolean = false;
  justCreated: boolean = false;

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
      if (this.computers.length && this.justCreated) {
        setTimeout(() => this.scrollToNewComputer(), 10); 
        this.justCreated = false;
      }  
    });
  }

  getComponentArray(components: { [key: string]: computerComponent }): computerComponent[] {
    return Object.values(components);
  }



  onSubmit(): void {
    if (this.budgetFormGroup.valid) {
      const budget = this.budgetFormGroup.value.budget;
    
      this.builderService.createPreference(budget, null, null, null).subscribe({
        next: (newPreference: Preferences) => {
          this.budgetFormGroup.reset();
    
          this.builderService.createComputer(newPreference.id!).subscribe({
            next: () => {
              this.justCreated = true; // Set flag to true when a new computer is created
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

  toggleDetails(): void {
    this.showDetails = !this.showDetails;
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

  

  private scrollToNewComputer(): void {
    const computerComponents = document.querySelectorAll('.custom-pc-container');
    const lastComputerComponent = computerComponents[computerComponents.length - 1];
    lastComputerComponent.scrollIntoView({ behavior: 'smooth' });

  }
}