import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs/Observable';
import { map } from 'rxjs/operators';
import { User } from 'app/models/User';
import { Router } from '@angular/router';
import { catchError } from 'rxjs/operators/catchError';
import { ErrorObservable } from 'rxjs/observable/ErrorObservable';
import { environment } from 'environments/environment';

/**
 * Fetches users data from server.
 *
 * @export
 * @class UserService
 */
@Injectable()
export class UserService {
    constructor(private http: HttpClient, private router: Router) { }

    /**
     * Returns currently logged in user.
     *
     * @returns {Observable<User>} Logged in User.
     * @memberof UserService
     */
    public get(): Observable<User> {
        return this.http.get<User>(`${environment.ip}/user/`, { withCredentials: true }).pipe(
            map(message => {
                if (message['error']) {
                    this.router.navigate(['/login']);
                }
                return message;
            })
        );
    }

    /**
     * User login.
     *
     * @param {string} username Username
     * @param {string} password Password
     * @returns {Observable<User>} Loggedin User
     * @memberof UserService
     */
    public login(username: string, password: string): Observable<User> {
        return this.http.post<User>(`${environment.ip}/login/`, { username, password }, { withCredentials: true });
    }

    /**
     * User logout.
     *
     * @returns {Promise<any>} Logout promise
     * @memberof UserService
     */
    public async logout(): Promise<any> {
        return this.http.delete<any>(`${environment.ip}/logout/`, { withCredentials: true }).toPromise();
    }

}
