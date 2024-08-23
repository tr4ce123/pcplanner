import { Component, OnInit } from '@angular/core';
import { FormBuilder, FormGroup, Validators } from '@angular/forms';
import { Route } from '@angular/router';
import { BuilderService } from '../builder/builder.service';
import { MatSnackBar } from '@angular/material/snack-bar';
import { Computer, Preferences, computerComponent } from '../models.module';
import { trigger, state, style, transition, animate, query, stagger } from '@angular/animations'
import { map, Observable, startWith } from 'rxjs';

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
  showAIForm: boolean = false;
  isLoading: boolean = false;

  options: string[] = [
    'What are some changes you would suggest?', 
    'How can I ensure my computer is future proofed?', 
    'What games will I be able to play with this build?',
    'What are some alternative ways I can balance this budget?'
  ];
  filteredOptions!: Observable<string[]>;


  public static Route: Route = {
    path: 'easy-builder',
    component: EasyBuilderComponent,
  }

  aiForm: FormGroup;
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
    this.aiForm = this.formBuilder.group({
      userPrompt: ['', Validators.required]
    });
  }

  ngOnInit(): void {
    this.getComputers();
    this.initAutocomplete();
  }

  initAutocomplete(): void {
    this.filteredOptions = this.aiForm.get('userPrompt')!.valueChanges.pipe(
      startWith(''),
      map(value => this._filter(value)) 
    );
  }
  
  private _filter(value: string): string[] {
    const filterValue = value.toLowerCase();
    return this.options.filter(option => option.toLowerCase().includes(filterValue));
  }
  


  ngOnDestroy(): void {
    this.deleteComputers();
  }

  getComputers(): void {
    this.builderService.getComputers().subscribe({
      next: (computers: Computer[]) => {
        this.computers = computers;
      },
      error: () => {
        this.snackBar.open('Failed to load computers!', '', { duration: 2000 });
      }
    });
  }

  getComponentArray(components: { [key: string]: computerComponent }): computerComponent[] {
    return Object.values(components);
  }

  toggleAIForm(computer: Computer): void {
    computer.showAIForm = !computer.showAIForm;
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

  submitAIRequest(computer: Computer): void {
    if (this.aiForm.valid) {
      const userPrompt = this.aiForm.value.userPrompt;
      this.isLoading = true;
      this.builderService.createAIResponse(computer.id, userPrompt).subscribe({
        next: response => {
          const formattedResponse = this.formatAIResponse(response.chat_response.response);
          // Find the computer in the local array and update it
          const index = this.computers.findIndex(c => c.id === computer.id);
          if (index !== -1) {
            this.computers[index].aiResponse = formattedResponse;
            this.computers = [...this.computers];
          }
          this.snackBar.open('Insights generated!', '', { duration: 2000 });
          this.toggleAIForm(computer);
          this.isLoading = false;
        },
        error: () => {
          this.snackBar.open('Failed to generate insights!', '', { duration: 2000 });
        }
      });
    }
  }

  private formatAIResponse(response: string): string {
    let cleanResponse = response.replace(/\*/g, '');

    let lines = cleanResponse.split('\n');
  
    return lines.join('\n');
  
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