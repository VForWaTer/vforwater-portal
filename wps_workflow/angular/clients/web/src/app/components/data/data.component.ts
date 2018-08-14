import {Data} from '../../models/Data';
import {Component, OnInit, Input, ElementRef, Output, EventEmitter, HostListener} from '@angular/core';
import {ViewChild} from '@angular/core';
import {MatDialog, MatMenu, MatMenuTrigger} from '@angular/material';

/**
 * Component Class representing a dragged Data Element from the vfw-portal datastore
 * @class DataComponent
 * @export
 * @implements {OnInit}
 */
@Component({
    selector: 'app-data',
    templateUrl: './data.component.html',
    styleUrls: ['./data.component.scss']
})
export class DataComponent implements OnInit
{
    /**
     * Data object
     */
    @Input()
    public data: Data;

    /**
     * ElementRef for output parameter container
     */
    @ViewChild('outputs')
    public outputContainer: ElementRef;

    /**
     * Trigger for context menu
     */
    @ViewChild(MatMenuTrigger)
    public menuComponent: MatMenuTrigger;

    /**
     * Emitter for drag Event function
     */
    @Output()
    public dataDrag = new EventEmitter();

    /**
     * Emitter for drop Event function
     */
    @Output()
    public dataDrop = new EventEmitter();

    /**
     * Emitter for Element remove function
     */
    @Output()
    public dataRemove = new EventEmitter<Data>();

    /**
     * local variable holding coordinates where mouse was pressen
     */
    private mouseDownPos: number[];

    /**
     * Constructor
     * creates a data object
     * @param {MatDialog} dialog material dialog
     * @param {ElementRef} el element reference
     */
    public constructor(public dialog: MatDialog, private el: ElementRef)
    {
    }

    /**
     * Component setup
     */
    public ngOnInit()
    {

    }


    /**
     * EventListener for mouseDown Event
     * triggered when the user clicks and saves the coords
     * @param {MouseEvent} event Event Var
     */
    @HostListener('mousedown', ['$event'])
    public hostMouseDown(event: MouseEvent)
    {
        if (event.button === 0)
        {
            this.mouseDownPos = [event.pageX, event.pageY];
        }
    }

    /**
     * EventListener for mouseUp Event
     * triggered when user releases mouse button, resets coords in local var and opens context menu
     * @param {MouseEvent} event Event Var
     */
    @HostListener('mouseup', ['$event'])
    public hostMouseUp(event: MouseEvent)
    {
        if ((<HTMLElement>event.target).classList.contains('nomove'))
        {
            return;
        }
        if (this.mouseDownPos && this.mouseDownPos[0] === event.pageX && this.mouseDownPos[1] === event.pageY)
        {
            this.menuComponent.openMenu();
        }
        this.mouseDownPos = undefined;
    }

    /**
     * opens task menu
     * @param {MouseEvent} event Event Var
     */
    @HostListener('contextmenu', ['$event'])
    public hostContextmenu(event: MouseEvent)
    {
        this.menuComponent.openMenu();
        return false;
    }

    /**
     * deletes the task
     */
    public clickDelete()
    {
        this.dataRemove.emit(this.data);
    }


    /**
     * EventListener for mouseDown Event on component
     * triggered when user clicks on data and triggers drag function
     * @param {MouseEvent} event Event Var
     */
    public dataMouseDown(event: MouseEvent)
    {
        this.mouseDownPos = [event.pageX, event.pageY];
        this.dataDrag.emit();
    }

    /**
     * returns the output parameter position
     * @param id the data id
     * @return coordinate tuple
     */
    public getDataPosition(id: number): [number, number]
    {
        console.log("dataPosition: 1");
        const n: HTMLDivElement = this.outputContainer.nativeElement;
        console.log("dataPosition: 2");

        for (let i = 0; i < n.childElementCount; i++)
        {
            console.log("dataPosition: 3");
            if (n.children[i].getAttribute('data-id') === '' + id)
            {
                console.log("dataPosition: 4");
                const rect = n.children[i].getBoundingClientRect();
                console.log("dataPosition: 5");
                return [rect.left + 11, rect.top + 11];
            }
        }
        return null;
    }

    /**
     * returns the color for a literal Parameter
     * @return {string} color code
     */
    public getParameterColor(): string
    {
        return '#03A9F4';
    }

}
