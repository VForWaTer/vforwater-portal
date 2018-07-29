import { Data } from '../../models/Data';
import { Component, OnInit, Input, ElementRef, Output, EventEmitter, HostListener } from '@angular/core';
import { ViewChild } from '@angular/core';
import { MatDialog, MatMenu, MatMenuTrigger } from '@angular/material';


@Component({
  selector: 'app-data',
  templateUrl: './data.component.html',
  styleUrls: ['./data.component.scss']
})
export class DataComponent implements OnInit {

  @Input()
  public data: Data;
  
  @ViewChild('outputs')
  public outputContainer: ElementRef;
  
  @ViewChild(MatMenuTrigger)
  public menuComponent: MatMenuTrigger;
  
  @Output()
  public dataDrag = new EventEmitter();
  
  @Output()
  public dataDrop = new EventEmitter();

  @Output()
  public dataRemove = new EventEmitter<Data>();

  private mouseDownPos: number[];
  
  /**
   * creates a data object
   * @param dialog material dialog
   * @param el element reference
   */
  public constructor(public dialog: MatDialog, private el: ElementRef) { }

  public ngOnInit() {
  
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
    this.dataRemove.emit(this.data);
  }

  
  
  /**
   * triggered when user clicks on task
   * @param parameter process parameter
   * @param event user clicks mouse
   */
  public dataMouseDown(event: MouseEvent) {
    this.mouseDownPos = [event.pageX, event.pageY];
    this.dataDrag.emit();
  }

   /**
   * returns the parameter position
   * @param role the parameter role which can either be input or output
   * @param id the parameter id
   */
  public getDataPosition(id: number): [number, number] {
      console.log("dataPosition: 1");
    const n: HTMLDivElement = this.outputContainer.nativeElement;
      console.log("dataPosition: 2");
      
    for (let i = 0; i < n.childElementCount; i++) {
        console.log("dataPosition: 3");
      if (n.children[i].getAttribute('data-id') === '' + id) {
          console.log("dataPosition: 4");
        const rect = n.children[i].getBoundingClientRect();
        console.log("dataPosition: 5");
        return [rect.left + 11, rect.top + 11];
      }
    }
    return null;
  }
  
  /**
   * returns the color of the process parameter
   * @param type type of the process parameter
   */
  public getParameterColor(): string {
      return '#03A9F4';
  }
  
}
