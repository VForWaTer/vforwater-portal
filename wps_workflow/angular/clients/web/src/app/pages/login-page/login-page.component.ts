import { Component, OnInit, ViewChild, ElementRef } from '@angular/core';
import { Observable } from 'rxjs/Observable';
import { ProcessService } from 'app/services/process.service';
import { WpsService } from 'app/services/wps.service';
import { WPS } from '../../models/WPS';
import { trigger, transition, style, animate } from '@angular/animations';
import { UserService } from 'app/services/user.service';
import { Router } from '@angular/router';
import { MatSnackBar } from '@angular/material';
import { map } from 'rxjs/operators/map';

/**
 * Simple login page.
 *
 * @export
 * @class LoginPageComponent
 * @implements {OnInit}
 */
@Component({
  selector: 'app-login-page',
  templateUrl: './login-page.component.html',
  styleUrls: ['./login-page.component.scss'],
})
export class LoginPageComponent implements OnInit {

  public loggedIn: Observable<boolean>;


  constructor(
    private userService: UserService,
    private router: Router,
    private bar: MatSnackBar
  ) {

  }

  /**
   * Component setup.
   *
   * @memberof LoginPageComponent
   */
  public ngOnInit(): void {
    this.loggedIn = this.userService.get().pipe(
      map(user => user !== undefined && user['error'] === undefined)
    );
  }

  /**
   * User login.
   *
   * @param {string} username Login name
   * @param {string} password Login Password
   * @memberof LoginPageComponent
   */
  public login(username: string, password: string) {
    this.userService.login(username, password).subscribe(user => {
      if (!user || user['error']) {
        this.bar.open(`Wrong Username or Password`, 'CLOSE', { duration: 2500 });
      } else {
        this.router.navigate(['/']);
      }
    });
  }

  /**
   * User logout.
   *
   * @memberof LoginPageComponent
   */
  public async logout() {
    await this.userService.logout();
    this.router.navigateByUrl('/');
  }
}
