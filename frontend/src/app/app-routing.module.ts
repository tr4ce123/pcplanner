import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { RouterModule, Routes } from '@angular/router';
import { HomeComponent } from './home/home.component';
import { BuilderComponent } from './builder/builder.component';

const routes: Routes = [
  // Default is home
  { path: '', redirectTo: '/home', pathMatch: 'full'},
  // Undefined routes go back to home
  // { path: '**', redirectTo: '/home' },
  HomeComponent.Route,
  BuilderComponent.Route
]

@NgModule({
  declarations: [],
  imports: [
    CommonModule,
    RouterModule.forRoot(routes)
  ],
  exports: [RouterModule]
})
export class AppRoutingModule { }
