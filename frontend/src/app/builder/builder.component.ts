import { Component, OnInit, ViewChild } from '@angular/core';
import { FormBuilder, FormGroup, Validators } from '@angular/forms';
import { MatSnackBar } from '@angular/material/snack-bar';
import { AIResponse, Computer, Preferences, computerComponent } from '../models.module';
import { BuilderService } from './builder.service';
import { ActivatedRoute, Route } from '@angular/router';
import { HostListener } from '@angular/core';
import { MatStepper } from '@angular/material/stepper';
import { BreakpointObserver, Breakpoints } from '@angular/cdk/layout';
import { trigger, state, style, transition, animate, query, stagger } from '@angular/animations'
import { map, Observable, startWith } from 'rxjs';

@Component({
  selector: 'app-builder',
  templateUrl: './builder.component.html',
  styleUrl: './builder.component.css',
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
      transition(':enter', [
        style({ opacity: 0 }),
        animate('1s', style({ opacity: 1 }))
      ])
    ])
  ]
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

  aiForm: FormGroup;
  budgetFormGroup: FormGroup;
  usageFormGroup: FormGroup;
  chipsetFormGroup: FormGroup;
  wifiFormGroup: FormGroup;

  cols!: number;
  isLoading: boolean = false;
  opened: boolean = false;
  justCreated: boolean = false;

  showAIForm: boolean = false;
  isFormLoading: boolean = false;

  options: string[] = [
    'What are some changes you would suggest?', 
    'How can I ensure my computer is future proofed?', 
    'What games will I be able to play with this build?',
    'What are some alternative ways I can balance this budget?'
  ];
  filteredOptions!: Observable<string[]>;
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

      this.aiForm = this.formBuilder.group({
        userPrompt: ['', Validators.required]
      });
  
      this.onResize(); 
      this.breakpointObserver.observe([Breakpoints.Handset]).subscribe(result => {
        this.stepperOrientation = result.matches ? 'vertical' : 'horizontal';
      });
  
    }

  ngOnInit(): void {
    // this.getAIResponses();
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
              this.justCreated = true;
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

  submitAIRequest(computer: Computer): void {
    if (this.aiForm.valid) {
      const userPrompt = this.aiForm.value.userPrompt;
      this.isFormLoading = true;
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
          this.isFormLoading = false;
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

  toggleAIForm(computer: Computer): void {
    computer.showAIForm = !computer.showAIForm;
  }
}
