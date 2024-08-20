import { Component, HostBinding } from '@angular/core';
import { Router, NavigationEnd, Event as RouterEvent } from '@angular/router';
import { filter, map } from 'rxjs/operators';

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrl: './app.component.css'
})
export class AppComponent {
  title = 'frontend';

  showToolbar: boolean = true;
  showFooter: boolean = true;

  @HostBinding('style.--toolbar-margin')
  get toolbarMargin() {
    return this.showToolbar ? '80px' : '0px';
  }


  constructor(private router: Router) {
    this.router.events.pipe(
      filter((event: RouterEvent): event is NavigationEnd => event instanceof NavigationEnd),
      map(event => event as NavigationEnd)
    ).subscribe((event: NavigationEnd) => {
      this.showToolbar = !event.urlAfterRedirects.startsWith('/welcome');
      this.showFooter = !event.urlAfterRedirects.startsWith('/welcome');

    });
  }

}
