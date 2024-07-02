import { Component } from '@angular/core';
import { FormBuilder } from '@angular/forms';
import { MatSnackBar } from '@angular/material/snack-bar';
import { ActivatedRoute, Route } from '@angular/router';

@Component({
  selector: 'app-home',
  templateUrl: './home.component.html',
  styleUrl: './home.component.css',
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


}
