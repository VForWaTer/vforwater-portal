import { Component, OnInit, Input, ElementRef, Output, EventEmitter, HostListener } from '@angular/core';
import { MatDialog, MatMenu, MatMenuTrigger } from '@angular/material';
import { ProcessParameterType, ProcessParameter } from 'app/models/ProcessParameter';
import { ViewChild } from '@angular/core';
import { ProcessDialogComponent } from 'app/components/process-dialog/process-dialog.component';
import { Process } from 'app/models/Process';
import { Task, TaskState } from 'app/models/Task';
import { ArtefactDialogComponent } from 'app/components/artefact-dialog/artefact-dialog.component';

/**
 * describes a tuple of a task and parameter
 */
export interface TaskParameterTuple {
  task: Task;
  parameter: ProcessParameter<'input' | 'output'>;
}

@Component({
  selector: 'app-task',
  templateUrl: './task.component.html',
  styleUrls: ['./task.component.scss']
})
export class TaskComponent implements OnInit {

  @Input()
  public process: Process;

  @Input()
  public task: Task;

  @ViewChild('inputs')
  public inputContainer: ElementRef;

  @ViewChild('outputs')
  public outputContainer: ElementRef;

  @ViewChild(MatMenuTrigger)
  public menuComponent: MatMenuTrigger;

  @Output()
  public parameterDrag = new EventEmitter<ProcessParameter<'input' | 'output'>>();

  @Output()
  public parameterDrop = new EventEmitter<ProcessParameter<'input' | 'output'>>();

  @Output()
  public taskRemove = new EventEmitter<Task>();

  @Output()
  public changeArtefact = new EventEmitter<[TaskParameterTuple, object]>();

  @Input()
  public running = false;

  private mouseDownPos: number[];

  /**
   * creates a task object
   * @param dialog material dialog
   * @param el element reference
   */
  public constructor(public dialog: MatDialog, private el: ElementRef) { }

  public ngOnInit() {

  }

  /**
   * @returns the task state as an object
   */
  public get stateInfo(): { name: string, color: string } {
    const infoMap = [
      { state: TaskState.DEPRECATED, name: 'DEPRECATED', color: '#E91E63' },
      { state: TaskState.FAILED, name: 'FAILED', color: '#F44336' },
      { state: TaskState.FINISHED, name: 'FINISHED', color: '#2196F3' },
      { state: TaskState.READY, name: 'READY', color: '#9E9E9E' },
      { state: TaskState.RUNNING, name: 'RUNNING', color: '#FFC107' },
      { state: TaskState.WAITING, name: 'WAITING', color: '#03A9F4' },
    ];

    return infoMap.find(info => info.state === this.task.state);
  }

  /**
   * triggered when the user clicks
   * @param event the user clicks the mouse button
   */
  @HostListener('mousedown', ['$event'])
  public hostMouseDown(event: MouseEvent) {
    if (event.button === 0) {
      this.mouseDownPos = [event.pageX, event.pageY];
    }
  }

  /**
   * triggered when user releases mouse button
   * @param event user releases mouse button
   */
  @HostListener('mouseup', ['$event'])
  public hostMouseUp(event: MouseEvent) {
    if ((<HTMLElement>event.target).classList.contains('nomove')) {
      return;
    }
    if (this.mouseDownPos && this.mouseDownPos[0] === event.pageX && this.mouseDownPos[1] === event.pageY) {
      this.menuComponent.openMenu();
    }
    this.mouseDownPos = undefined;
  }

  /**
   * opens task menu
   * @param event context menu event
   */
  @HostListener('contextmenu', ['$event'])
  public hostContextmenu(event: MouseEvent) {
    this.menuComponent.openMenu();
    return false;
  }

  /**
   * deletes the task
   */
  public clickDelete() {
    this.taskRemove.emit(this.task);
  }

  /**
   * opens the process dialog
   */
  public openDetail() {
    this.dialog.open(ProcessDialogComponent, {
      data: this.process
    });
  }

  /**
   * returns the color of the process parameter
   * @param type type of the process parameter
   */
  public getParameterColor(type: ProcessParameterType): string {
    switch (type) {
      case ProcessParameterType.LITERAL: return '#03A9F4';
      case ProcessParameterType.COMPLEX: return '#FFC107';
      case ProcessParameterType.BOUNDING_BOX: return '#4CAF50';
      default: return '#000000';
    }
  }

  /**
   * triggered when user clicks on task
   * @param parameter process parameter
   * @param event user clicks mouse
   */
  public parameterMouseDown(parameter: ProcessParameter<'input' | 'output'>, event: MouseEvent) {
    if (this.hasArtefact(parameter)) {
      return;
    }

    this.mouseDownPos = [event.pageX, event.pageY];
    this.parameterDrag.emit(parameter);
  }

  /**
   * opens artefact dialog
   * @param parameter process parameter
   * @param event user releases mouse button
   */
  public parameterMouseUp(parameter: ProcessParameter<'input' | 'output'>, event: MouseEvent) {
    if (this.mouseDownPos && this.mouseDownPos[0] === event.pageX && this.mouseDownPos[1] === event.pageY) {
      // Can't open output dialog when editing
      if (parameter.role === 'output' && !this.running) {
        return;
      }
      // Can't open input dialog when running
      if (parameter.role === 'input' && this.running) {
        return;
      }
      // Can't open output artefakt without a result
      if (
        parameter.role === 'output' &&
        this.task.output_artefacts.findIndex(artefact => artefact.parameter_id === parameter.id) === -1
      ) {
        return;
      }


      this.dialog.open(ArtefactDialogComponent, {
        data: {
          task: this,
          parameter
        }
      });
    } else {
      if (!this.hasArtefact(parameter)) {
        this.parameterDrop.emit(parameter);
      }
    }
  }

  /**
   * adds data to an artefact
   * @param parameter process parameter
   * @param data the added data
   */
  public addArtefact(parameter: ProcessParameter<'input' | 'output'>, data: object) {
    this.changeArtefact.emit([{ task: this.task, parameter }, data]);
  }

  public removeArtefact(parameter: ProcessParameter<'input' | 'output'>) {
    this.changeArtefact.emit([{ task: this.task, parameter }, null]);
  }

  /**
   * returns if the task component has an artefact
   * @param parameter process parameter
   */
  public hasArtefact(parameter: ProcessParameter<'input' | 'output'>): boolean {
    if (!this.task.input_artefacts || !this.task.output_artefacts) {
      return false;
    }

    if (parameter.role === 'input') {
      return -1 !== this.task.input_artefacts.findIndex(artefact => artefact.parameter_id === parameter.id);
    } else if (this.running) {
      return -1 !== this.task.output_artefacts.findIndex(artefact => artefact.parameter_id === parameter.id);
    }
    return false;
  }

  /**
   * returns the parameter position
   * @param role the parameter role which can either be input or output
   * @param id the parameter id
   */
  public getParameterPosition(role: 'input' | 'output', id: number): [number, number] {
    const n: HTMLDivElement = (role === 'input' ? this.inputContainer : this.outputContainer).nativeElement;

    for (let i = 0; i < n.childElementCount; i++) {
      if (n.children[i].getAttribute('data-id') === '' + id) {
        const rect = n.children[i].getBoundingClientRect();
        return [rect.left + 11, rect.top + 11];
      }
    }
    return null;
  }

}
