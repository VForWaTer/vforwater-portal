import { Component, OnInit, Inject, ViewEncapsulation, ViewChild, ElementRef } from '@angular/core';
import { MAT_DIALOG_DATA, MatDialogRef } from '@angular/material';
import { ProcessParameter, ProcessParameterType } from 'app/models/ProcessParameter';
import { ProcessService } from 'app/services/process.service';
import { Process } from 'app/models/Process';
import { Task } from 'app/models/Task';
import { TaskComponent } from 'app/components/task/task.component';
import { analyzeFile } from '@angular/compiler';
import { Artefact } from 'app/models/Artefact';

interface ArtefactDialogData {
  task: TaskComponent;
  parameter: ProcessParameter<'input' | 'output'>;
}


/**
 * Artefact Dialog Component.
 *
 * @export
 * @class ArtefactDialogComponent
 * @implements {OnInit}
 */
@Component({
  selector: 'app-artefact-dialog',
  templateUrl: './artefact-dialog.component.html',
  styleUrls: ['./artefact-dialog.component.scss'],
})
export class ArtefactDialogComponent implements OnInit {

  public selectedFormat = 'markdown';
  public data: any = {};

  public editMode = true;

  public task: TaskComponent;
  public parameter: ProcessParameter<'input' | 'output'>;

  public deletable = false;

  @ViewChild('code')
  public codeComponent: ElementRef;


  /**
   * Creates an instance of ArtefactDialogComponent.
   *
   * @param {ArtefactDialogData} data
   * @param {MatDialogRef<ArtefactDialogComponent>} dialog
   * @memberof ArtefactDialogComponent
   */
  constructor(@Inject(MAT_DIALOG_DATA) data: ArtefactDialogData, public dialog: MatDialogRef<ArtefactDialogComponent>) {
    this.task = data.task;
    this.parameter = data.parameter;

    if (!this.parameter || !this.task) {
      return;
    }

    // Get all artefacts of this tasks
    const artefacts: Artefact<'input' | 'output'>[] = this.parameter.role === 'input'
      ? this.task.task.input_artefacts
      : this.task.task.output_artefacts;

    const artefact = artefacts.find(a => a.parameter_id === this.parameter.id);

    // Check if parameter has artefact
    if (artefact) {
      this.data['value'] = artefact.data;

      if (artefact.role === 'input') {
        this.data['format'] = this.parameter.format || 'string';

        if (this.parameter.type === ProcessParameterType.BOUNDING_BOX) {
          const coords = artefact.data.split(';')
            .map(value => value.split('=')[1])
            .map(value => value.split(' '));

          this.data.ux = coords[0][0];
          this.data.uy = coords[0][1];
          this.data.lx = coords[1][0];
          this.data.ly = coords[1][1];
        }
      }
      if (artefact.role === 'output') {
        this.data['format'] = artefact.format || 'string';
      }
    } else {
      this.data['format'] = this.parameter.format || 'string';
    }


    if (this.data.value) {
      this.deletable = true;
    }
  }

  /**
   * Component setup.
   *
   * @memberof ArtefactDialogComponent
   */
  public ngOnInit() {
  }

  /**
   * Checks whether the user artefact data input is valid.
   *
   * @readonly
   * @type {boolean}
   * @memberof ArtefactDialogComponent
   */
  public get valid(): boolean {

    if (this.parameter.type === ProcessParameterType.LITERAL) {
      // Check Literal Data
      if (!this.data.value || this.data.value.length === 0) {
        return false;
      }

      switch (this.data.format) {
        case 'string': return true;
        case 'float': return !isNaN(this.data.value);
        case 'integer': return /^-?[0-9]+$/.test(this.data.value);
        default: return true; /* Match any type */
      }
    } else if (this.parameter.type === ProcessParameterType.COMPLEX) {
      // Check Compley Data

    } else if (this.parameter.type === ProcessParameterType.BOUNDING_BOX) {
      // Check Bounding Box Data

      // All fields must exist
      if (this.data.ux === undefined
        || this.data.uy === undefined
        || this.data.lx === undefined
        || this.data.lx === undefined) {
        return false;
      }

    } else {
      console.log(`Error: Process Type Not Found ${this.parameter.type}`);
    }

    return true;
  }

  /**
   * Returns name and color of artefact type.
   *
   * @param {number} type Type id
   * @returns {[string, string]} Name, Color pair
   * @memberof ArtefactDialogComponent
   */
  public getTypeInfo(type: number): [string, string] {
    return [ProcessService.getTypeName(type), ProcessService.getTypeColor(type)];
  }

  /**
   * Is used to change input of the different input types
   * as every input type requires different fields,
   * we have to differ between them
   *
   * @memberof ArtefactDialogComponent
   */
  public clickEditButton() {
    const el: HTMLElement = this.codeComponent.nativeElement;

    if (this.editMode) {
      el.className = '';
      el.innerHTML = '';

      const format = this.parameter.type === ProcessParameterType.COMPLEX
        ? this.selectedFormat
        : 'markdown';

      el.classList.add(format);

      const data = this.parameter.type === ProcessParameterType.BOUNDING_BOX
        ? `UpperCorner=${this.data.ux} ${this.data.uy};LowerCorner=${this.data.lx} ${this.data.ly}`
        : this.data.value;

      if (data) {
        el.appendChild(document.createTextNode(data));
      }

    }

    this.editMode = !this.editMode;
  }

  /**
   * Saves the artefacts modified input.
   *
   * @returns {void}
   * @memberof ArtefactDialogComponent
   */
  public save(): void {
    if (!this.data) {
      return;
    }

    const out = {
      value: this.parameter.type === ProcessParameterType.BOUNDING_BOX
        ? `UpperCorner=${this.data.ux} ${this.data.uy};LowerCorner=${this.data.lx} ${this.data.ly}`
        : this.data.value,

      format: this.selectedFormat === 'markdown' ? 'plain' : this.selectedFormat
    };

    if (out.value && out.value.length > 0) {
      this.task.addArtefact(this.parameter, out);
    }

    this.dialog.close();
  }

  /**
   * Removes artefact from task.
   *
   * @memberof ArtefactDialogComponent
   */
  public remove() {
    this.task.removeArtefact(this.parameter);
    this.dialog.close();
  }
}
