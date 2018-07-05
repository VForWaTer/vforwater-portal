import { Component } from '@angular/core';
import { Router, ActivatedRoute, NavigationEnd } from '@angular/router';
import { UserService } from 'app/services/user.service';
import { catchError } from 'rxjs/operators';

/**
 * App Component.
 *
 * @export
 * @class AppComponent
 */
@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.scss']
})
export class AppComponent {

  showNav = true;

  /**
   * Creates an instance of AppComponent.
   *
   * @param {Router} router
   * @param {UserService} userService
   * @memberof AppComponent
   */
  public constructor(private router: Router, private userService: UserService) {
    userService.get()
      .subscribe(
        user => {
          if (user['error']) {
            this.router.navigate(['/login']);
          }
        },
        err => this.router.navigate(['/login'])
      );

    // Hide navigation bar when user is on /login
    this.router.events.subscribe(route => {
      if (route instanceof NavigationEnd) {
        if (route.url === '/login') {
          this.showNav = false;
        } else {
          this.showNav = true;
        }
      }
    });
  }
}
