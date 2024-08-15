import { Component, HostListener } from '@angular/core';
import { FormBuilder } from '@angular/forms';
import { MatSnackBar } from '@angular/material/snack-bar';
import { ActivatedRoute, Route } from '@angular/router';
import { animate, style, transition, trigger } from '@angular/animations'

@Component({
  selector: 'app-home',
  templateUrl: './home.component.html',
  styleUrl: './home.component.css',
  animations: [
    trigger('fadeIn', [
      transition(':enter', [
        style({opacity: 0}),
        animate('2s ease-out', style({opacity: 1})),
      ], { params: { delay: 0 } }),
    ]),
  ],
})
export class HomeComponent {

  public static Route: Route = {
    path: 'home',
    component: HomeComponent,
  }
  
  constructor(
    protected formBuilder: FormBuilder,
    protected snackBar: MatSnackBar,
    private route: ActivatedRoute,
    ) {
    }

  isVisibleStep1 = false;
  isVisibleStep2 = false;
  isVisibleStep3 = false;
  isVisibleWhy = false;

  @HostListener('window:scroll', ['$event'])
  onWindowScroll() {
    const step1Position = document.getElementById('step1')?.getBoundingClientRect().top ?? 0;
    const step2Position = document.getElementById('step2')?.getBoundingClientRect().top ?? 0;
    const step3Position = document.getElementById('step3')?.getBoundingClientRect().top ?? 0;
    const triggerHeight = window.innerHeight * 0.8;

    this.isVisibleStep1 = step1Position < triggerHeight;
    this.isVisibleStep2 = step2Position < triggerHeight;
    this.isVisibleStep3 = step3Position < triggerHeight;
  }

}
