import { Component, OnInit, Input, ChangeDetectionStrategy } from '@angular/core';
import { Process } from 'app/models/Process';
import { WPS } from 'app/models/WPS';


@Component({
  selector: 'app-process-list',
  templateUrl: './process-list.component.html',
  styleUrls: ['./process-list.component.scss'],
  changeDetection: ChangeDetectionStrategy.OnPush
})
export class ProcessListComponent implements OnInit {

  @Input()
  public processes: Process[];

  @Input()
  public wps: WPS[];

  /**
   * creates a process list object
   */
  public constructor() { }

  public ngOnInit() { }

  /**
   * returns the process by the wps id
   * @param id the id of the wps
   */
  public processByWPS(id: number) {
    return this.processes.filter(process => process.wps_id === id);
  }
}
