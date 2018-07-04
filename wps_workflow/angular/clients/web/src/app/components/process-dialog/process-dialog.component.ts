import { Component, OnInit, Inject } from '@angular/core';
import { MAT_DIALOG_DATA } from '@angular/material';
import { Process } from 'app/models/Process';
import { ProcessParameterType } from 'app/models/ProcessParameter';
import { ProcessService } from 'app/services/process.service';

@Component({
  selector: 'app-process-dialog',
  templateUrl: './process-dialog.component.html',
  styleUrls: ['./process-dialog.component.scss']
})
export class ProcessDialogComponent implements OnInit {

  /**
   * creates a process dialog object
   * @param process the associated process
   */
  constructor( @Inject(MAT_DIALOG_DATA) public process: Process) { }

  ngOnInit() {
  }

  /**
   * returns the name of the parameter type
   * @param type the type of the parameter
   */
  public getTypeName(type: ProcessParameterType) {
    return ProcessService.getTypeName(type);
  }

  /**
   * returns the color of the parameter type
   * @param type the type of the parameter
   */
  public getTypeColor(type: ProcessParameterType) {
    return ProcessService.getTypeColor(type);
  }
}
