import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { RouterModule, Routes } from '@angular/router';
import { HomeComponent } from './home/home.component';
import { BuilderComponent } from './builder/builder.component';
import { EasyBuilderComponent } from './easy-builder/easy-builder.component';
import { LandingPageComponent } from './landing-page/landing-page.component';
import { AboutComponent } from './about/about.component'

const routes: Routes = [
  // Default is home
  { path: '', redirectTo: '/welcome', pathMatch: 'full'},
  // Undefined routes go back to home
  // { path: '**', redirectTo: '/home' },
  HomeComponent.Route,
  BuilderComponent.Route,
  EasyBuilderComponent.Route,
  LandingPageComponent.Route,
  AboutComponent.Route
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
