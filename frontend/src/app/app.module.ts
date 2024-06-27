import { BrowserModule } from '@angular/platform-browser';
import { NgModule } from '@angular/core';
import { provideHttpClient, withInterceptorsFromDi } from '@angular/common/http';
import { FormsModule } from '@angular/forms';

import { AppComponent } from './app.component';
import { HomeComponent } from './home/home.component';
import { AppRoutingModule } from './app-routing.module';
import { provideAnimationsAsync } from '@angular/platform-browser/animations/async';

// Material UI
import { MatButtonModule } from '@angular/material/button'
import { MatIconModule } from '@angular/material/icon'
import { MatDividerModule } from '@angular/material/divider'
import { MatToolbarModule } from '@angular/material/toolbar';
import { MatFormFieldModule } from '@angular/material/form-field';
import { MatCardModule } from '@angular/material/card';
import { MatInputModule } from '@angular/material/input';
import { ReactiveFormsModule } from '@angular/forms';
import { MatSnackBarModule } from '@angular/material/snack-bar'
import { MatGridListModule } from '@angular/material/grid-list'
import { MatSelectModule } from '@angular/material/select'
import { MatProgressBarModule } from '@angular/material/progress-bar'
import { MatStepperModule } from '@angular/material/stepper'
import { MatListModule } from '@angular/material/list'
import { MatSidenavModule } from '@angular/material/sidenav'

@NgModule({ declarations: [
        AppComponent,
        HomeComponent
    ],
    bootstrap: [AppComponent], imports: [BrowserModule,
        FormsModule,
        AppRoutingModule,
        // Material UI
        MatButtonModule,
        MatIconModule,
        MatDividerModule,
        MatToolbarModule,
        MatFormFieldModule,
        MatCardModule,
        MatInputModule,
        ReactiveFormsModule,
        MatSnackBarModule,
        MatGridListModule,
        MatSelectModule,
        MatProgressBarModule,
        MatStepperModule,
        MatListModule,
        MatSidenavModule
    ], providers: [
        provideAnimationsAsync(),
        provideHttpClient(withInterceptorsFromDi())
    ] })
export class AppModule { }
