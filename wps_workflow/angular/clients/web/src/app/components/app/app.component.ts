import {Component} from '@angular/core';
import {Router, ActivatedRoute, NavigationEnd} from '@angular/router';
import {UserService} from 'app/services/user.service';
import {catchError} from 'rxjs/operators';

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
export class AppComponent
{

    showNav = true;
    admin = false;

    /**
     * Creates an instance of AppComponent.
     *
     * @param {Router} router
     * @param {UserService} userService
     * @memberof AppComponent
     */
    public constructor(private router: Router, private userService: UserService)
    {
        this.admin = false;
        userService.get()
            .subscribe(
                user =>
                {
                    if (user['error'])
                    {
                        this.admin = false;
                    } else
                    {
                        this.admin = user.is_staff;
                    }
                },
                err => this.admin = false
            );

    }
}
