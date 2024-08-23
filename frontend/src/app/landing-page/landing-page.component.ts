import { Component } from '@angular/core';
import {  Route } from '@angular/router';
import { trigger, transition, style, animate, query, stagger } from '@angular/animations';


@Component({
  selector: 'app-landing-page',
  templateUrl: './landing-page.component.html',
  styleUrl: './landing-page.component.css',
  animations: [
    trigger('fadeIn', [
      transition(':enter', [
        style({ opacity: 0 }),
        animate('1s', style({ opacity: 1 }))
      ])
    ]),
  ],
  

})
export class LandingPageComponent {
  public static Route: Route = {
    path: 'welcome',
    component: LandingPageComponent,
  }

  typedText = '';
  private fullText = 'Welcome to PCPlanner';
  private currentIndex = 0;
  private typingSpeed = 150;

  showButton = false;


  constructor() { }

  ngOnInit(): void {
    this.typeWriterEffect();
  }

  private typeWriterEffect(): void {
    if (this.currentIndex < this.fullText.length) {
      this.typedText += this.fullText.charAt(this.currentIndex);
      this.currentIndex++;
      setTimeout(() => this.typeWriterEffect(), this.typingSpeed);
    } else {
      this.showButton = true;
    }
  }

}
