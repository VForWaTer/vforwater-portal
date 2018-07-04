import { Component, OnInit, Input, HostListener, HostBinding, ElementRef } from '@angular/core';
import { MatDialog } from '@angular/material';
import { ProcessParameterType } from 'app/models/ProcessParameter';
import { ProcessDialogComponent } from 'app/components/process-dialog/process-dialog.component';
import { Process } from 'app/models/Process';


@Component({
  selector: 'app-process',
  templateUrl: './process.component.html',
  styleUrls: ['./process.component.scss']
})
export class ProcessComponent implements OnInit {

  @Input()
  public process: Process;

  @HostBinding('draggable')
  public draggable = true;

  /**
   * triggered if host clicks
   */
  @HostListener('click')
  public hostClicked() {
    this.openDialog();
  }

  /**
   * creates a process object
   * @param dialog the dialog that opens a process dialog
   * @param el element reference
   */
  public constructor(public dialog: MatDialog, private el: ElementRef) { }

  /**
   * opens a process dialog
   */
  public openDialog() {
    this.dialog.open(ProcessDialogComponent, {
      data: this.process
    });
  }

  /**
   * returns the color of the parameter
   * @param type the parameter type
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
   * triggered if user starts to drag element
   * @param event the user starts dragging an element
   */
  @HostListener('dragstart', ['$event'])
  public dragStart(event: DragEvent) {
    const native: HTMLElement = this.el.nativeElement;

    for (let i = 0; i < native.childElementCount; i++) {
      const c = native.children[i];
      if (c.classList.contains('container')) {
        event.dataTransfer.setDragImage(c, c.clientWidth / 2, c.clientHeight / 2);
        event.dataTransfer.setData('json', JSON.stringify(this.process));
        break;
      }
    }

  }



  public ngOnInit() {

  }

}
