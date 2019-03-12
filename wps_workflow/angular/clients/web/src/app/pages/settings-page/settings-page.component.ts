import { Component, OnInit, ViewChild, ElementRef } from '@angular/core';
import { Observable } from 'rxjs/Observable';
import { ProcessService } from 'app/services/process.service';
import { WpsService } from 'app/services/wps.service';
import { WPS } from '../../models/WPS';
import { trigger, transition, style, animate } from '@angular/animations';

/**
 * Settings page.
 *
 * @export
 * @class SettingsPageComponent
 * @implements {OnInit}
 */
@Component({
  selector: 'app-settings-page',
  templateUrl: './settings-page.component.html',
  styleUrls: ['./settings-page.component.scss'],
  animations: [
    trigger('slide', [
      transition(':enter', [
        style({ transform: 'translateX(-100%)' }),
        animate('233ms ease-in-out')
      ]),
      transition(':leave', [
        animate('233ms ease-in-out', style({ transform: 'translateX(100%)' }))
      ]),
    ])
  ]
})
export class SettingsPageComponent implements OnInit {

  wpsList: Observable<WPS[]>;

  @ViewChild('url')
  public urlComponent: ElementRef;

  /**
   * Creates an instance of SettingsPageComponent.
   *
   * @param {ProcessService} processService
   * @param {WpsService} wpsService
   * @memberof SettingsPageComponent
   */
  constructor(
    private processService: ProcessService,
    private wpsService: WpsService,
  ) {

  }

  /**
   * Component setup.
   *
   * @memberof SettingsPageComponent
   */
  public ngOnInit() {
    this.wpsList = this.wpsService.all();
  }

  /**
   * Refreshes wps servers to check for new processes.
   *
   * @memberof SettingsPageComponent
   */
  public async refresh() {
    await this.wpsService.refresh();
    this.wpsList = this.wpsService.all();
  }

  /**
   * Adds wps server by a given wps server url.
   *
   * @param {string} url WPS server url
   * @memberof SettingsPageComponent
   */
  public async add(url: string) {
    await this.wpsService.create(url).toPromise();
    this.wpsList = this.wpsService.all();
    (<HTMLInputElement>this.urlComponent.nativeElement).value = '';
  }

  /**
   * removes the wps server with the given id.
   *
   * @param id the id of the wps
   */
  public async remove(id: number) {
    await this.wpsService.remove(id);
    this.wpsList = this.wpsService.all();
  }
}
