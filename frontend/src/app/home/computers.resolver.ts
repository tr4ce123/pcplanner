import { ResolveFn } from '@angular/router';
import { Injectable, inject } from '@angular/core';
import { ActivatedRouteSnapshot, RouterStateSnapshot } from '@angular/router';
import { Observable, of } from 'rxjs';
import { Computer } from '../models.module';
import { HomeService } from './home.service';


export const computersResolver: ResolveFn<Computer[]> = (route, state) => {
  return inject(HomeService).getComputers();
};
