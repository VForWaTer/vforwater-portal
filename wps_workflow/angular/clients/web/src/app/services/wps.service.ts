import { Injectable } from '@angular/core';
import { WPS } from '../models/WPS';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs/Observable';
import { map, switchMap, catchError } from 'rxjs/operators';
import { ErrorObservable } from 'rxjs/observable/ErrorObservable';
import { MatSnackBar } from '@angular/material';
import { environment } from 'environments/environment';

/**
 * Fetches wps data from server.
 *
 * @export
 * @class WpsService
 */
@Injectable()
export class WpsService {
  /**
   * Constructs wps service.
   *
   * @param {HttpClient} http
   * @param {MatSnackBar} bar
   */
  constructor(private http: HttpClient, private bar: MatSnackBar) { }


  /**
   * Returns an observable to all WPS.
   *
   * @returns {Observable<WPS[]>}
   */
  public all(): Observable<WPS[]> {
    return this.http.get<WPS[]>(`${environment.ip}/wps/`, { withCredentials: true });
  }


  /**
   * Create WPS and returns observable of WPS.
   * currently disabled
   *
   * @param {string} url
   * @returns {Observable<WPS>}
   */
  public create(url: string): Observable<WPS> {
    this.bar.open(`Created WPS`, 'CLOSE', { duration: 3000 });
    return this.http.post<WPS>(`${environment.ip}/wps/`, url, { withCredentials: true }).pipe(
      catchError((error) => {
        this.bar.open(`ERROR. Can not add WPS Server. Wrong URL?`, 'CLOSE', { duration: 5000 });
        return new ErrorObservable(`can't create wps`);
      })
    );
  }

  /**
   * Removes WPS with given id.
   *
   * @param {number} id
   * @returns {Promise<boolean>}
   */
  public async remove(id: number): Promise<boolean> {
    this.bar.open(`Deleted WPS`, 'CLOSE', { duration: 3000 });
    return this.http.delete<boolean>(`${environment.ip}/wps/${id}`, { withCredentials: true }).toPromise();
  }

  /**
   * Refreshes all wps servers.
   *
   * @returns {Promise<boolean>} Refresh succsessful
   * @memberof WpsService
   */
  public async refresh(): Promise<boolean> {
    this.bar.open(`Refreshed WPS Processes`, 'CLOSE', { duration: 3000 });
    const result = this.http.get<boolean>(`${environment.ip}/wps_refresh/`, { withCredentials: true }).toPromise();
    return result['error'] === undefined;
  }
}
