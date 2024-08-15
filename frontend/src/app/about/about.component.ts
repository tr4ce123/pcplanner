import { Component } from '@angular/core';
import { Route } from '@angular/router';

@Component({
  selector: 'app-about',
  templateUrl: './about.component.html',
  styleUrl: './about.component.css'
})
export class AboutComponent {
  public static Route: Route = {
    path: 'about',
    component: AboutComponent,
  }
}
