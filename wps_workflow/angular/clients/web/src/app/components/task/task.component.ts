import {Component, OnInit, Input, ElementRef, Output, EventEmitter, HostListener} from '@angular/core';
import {MatDialog, MatMenu, MatMenuTrigger} from '@angular/material';
import {ProcessParameterType, ProcessParameter} from 'app/models/ProcessParameter';
import {ViewChild} from '@angular/core';
import {ProcessDialogComponent} from 'app/components/process-dialog/process-dialog.component';
import {Process} from 'app/models/Process';
import {Task, TaskState} from 'app/models/Task';
import {ArtefactDialogComponent} from 'app/components/artefact-dialog/artefact-dialog.component';

/**
 * @interface TaskParameterTuple
 * describes a tuple of a task and parameter
 */
export interface TaskParameterTuple
{
    task: Task;
    parameter: ProcessParameter<'input' | 'output'>;
}

/**
 * Component Class for the Task  in Editor
 * @export
 * @class TaskComponent
 * @implements {OnInit}
 */
@Component({
    selector: 'app-task',
    templateUrl: './task.component.html',
    styleUrls: ['./task.component.scss']
})
export class TaskComponent implements OnInit
{

    /**
     * Process to this Task
     */
    @Input()
    public process: Process;

    /**
     *  Task Model to this Component
     */
    @Input()
    public task: Task;

    /**
     *  Parameter Input Container Reference
     */
    @ViewChild('inputs')
    public inputContainer: ElementRef;

    /**
     *  Parameter Output Container Reference
     */
    @ViewChild('outputs')
    public outputContainer: ElementRef;

    /**
     * Trigger for context menu
     */
    @ViewChild(MatMenuTrigger)
    public menuComponent: MatMenuTrigger;

    /**
     * Emitter for Edge drag function
     */
    @Output()
    public parameterDrag = new EventEmitter<ProcessParameter<'input' | 'output'>>();

    /**
     * Emitter for Edge drop function
     */
    @Output()
    public parameterDrop = new EventEmitter<ProcessParameter<'input' | 'output'>>();

    /**
     * Emitter for delete function
     */
    @Output()
    public taskRemove = new EventEmitter<Task>();

    /**
     * Emitter for Artefact change/delete function
     */
    @Output()
    public changeArtefact = new EventEmitter<[TaskParameterTuple, object]>();

    /**
     * Status variable if workflow is running
     */
    @Input()
    public running = false;

    /**
     * holds coordinates where mouse button was pressed
     */
    private mouseDownPos: number[];

    /**
     * creates a task object
     * @param {MatDialog} dialog material dialog
     * @param {ElementRef} el element reference to component
     */
    public constructor(public dialog: MatDialog, private el: ElementRef)
    {
    }

    /**
     * Component setup
     * @memberOf TaskComponent
     */
    public ngOnInit()
    {

    }

    /**
     * Getter for task execute state
     * @returns Touple of name and color of state
     */
    public get stateInfo(): { name: string, color: string }
    {
        const infoMap = [
            {state: TaskState.DEPRECATED, name: 'DEPRECATED', color: '#E91E63'},
            {state: TaskState.FAILED, name: 'FAILED', color: '#F44336'},
            {state: TaskState.FINISHED, name: 'FINISHED', color: '#2196F3'},
            {state: TaskState.READY, name: 'READY', color: '#9E9E9E'},
            {state: TaskState.RUNNING, name: 'RUNNING', color: '#FFC107'},
            {state: TaskState.WAITING, name: 'WAITING', color: '#03A9F4'},
        ];

        return infoMap.find(info => info.state === this.task.state);
    }

    /**
     * EventListener for mouseDown Event
     * triggered when the user clicks
     * sets local var to the mouse coordinates
     * @param {MouseEvent} event Event variable
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
     * triggered when user releases mouse button
     * opens the context menu and resets local mouseDownPos Variable
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
     * EventListener for context menu click
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
        this.taskRemove.emit(this.task);
    }

    /**
     * opens the process dialog
     */
    public openDetail()
    {
        this.dialog.open(ProcessDialogComponent, {
            data: this.process
        });
    }

    /**
     * returns the color of the process parameter
     * @param {ProcessParameterType} type type of the process parameter
     */
    public getParameterColor(type: ProcessParameterType): string
    {
        switch (type)
        {
            case ProcessParameterType.LITERAL:
                return '#03A9F4';
            case ProcessParameterType.COMPLEX:
                return '#FFC107';
            case ProcessParameterType.BOUNDING_BOX:
                return '#4CAF50';
            default:
                return '#000000';
        }
    }

    /**
     * EventListener for mouseDown Event on Parameter
     * triggered when user clicks on a parameter of task.
     * @param {ProcessParameter} parameter clicked parameter
     * @param {MouseEvent} event Event Var
     */
    public parameterMouseDown(parameter: ProcessParameter<'input' | 'output'>, event: MouseEvent)
    {
        if (this.hasArtefact(parameter))
        {
            return;
        }

        this.mouseDownPos = [event.pageX, event.pageY];
        this.parameterDrag.emit(parameter);
    }

    /**
     * EventListener for mouseUp Event on Parameter
     * triggered when user releases the mouse button on a parameter (clicking it) and opens the artefact dialog
     * @param {ProcessParameter} parameter clicked parameter
     * @param {MouseEvent} event Event Var
     */
    public parameterMouseUp(parameter: ProcessParameter<'input' | 'output'>, event: MouseEvent)
    {
        if (this.mouseDownPos && this.mouseDownPos[0] === event.pageX && this.mouseDownPos[1] === event.pageY)
        {
            // Can't open output dialog when editing
            if (parameter.role === 'output' && !this.running)
            {
                return;
            }
            // Can't open input dialog when running
            if (parameter.role === 'input' && this.running)
            {
                return;
            }
            // Can't open output artefakt without a result
            if (
                parameter.role === 'output' &&
                this.task.output_artefacts.findIndex(artefact => artefact.parameter_id === parameter.id) === -1
            )
            {
                return;
            }


            this.dialog.open(ArtefactDialogComponent, {
                data: {
                    task: this,
                    parameter
                }
            });
        } else
        {
            if (!this.hasArtefact(parameter)) // TODO & if has edge from parameter
            {
                this.parameterDrop.emit(parameter);
            }
        }
    }

    /**
     * adds data to an artefact
     * @param {ProcessParameter} parameter process parameter
     * @param data the added data
     */
    public addArtefact(parameter: ProcessParameter<'input' | 'output'>, data: object)
    {
        this.changeArtefact.emit([{task: this.task, parameter}, data]);
    }

    /**
     * removes the artefact to the clicked parameter
     * @param {ProcessParameter} parameter
     */
    public removeArtefact(parameter: ProcessParameter<'input' | 'output'>)
    {
        this.changeArtefact.emit([{task: this.task, parameter}, null]);
    }

    /**
     * returns if the task component has an artefact
     * @param {ProcessParameter} parameter process parameter
     */
    public hasArtefact(parameter: ProcessParameter<'input' | 'output'>): boolean
    {
        if (!this.task.input_artefacts || !this.task.output_artefacts)
        {
            return false;
        }

        if (parameter.role === 'input')
        {
            return -1 !== this.task.input_artefacts.findIndex(artefact => artefact.parameter_id === parameter.id);
        } else if (this.running)
        {
            return -1 !== this.task.output_artefacts.findIndex(artefact => artefact.parameter_id === parameter.id);
        }
        return false;
    }

    /**
     * returns the parameter position
     * @param role the parameter role which can either be input or output
     * @param id the parameter id
     */
    public getParameterPosition(role: 'input' | 'output', id: number): [number, number]
    {
        const n: HTMLDivElement = (role === 'input' ? this.inputContainer : this.outputContainer).nativeElement;

        for (let i = 0; i < n.childElementCount; i++)
        {
            if (n.children[i].getAttribute('data-id') === '' + id)
            {
                const rect = n.children[i].getBoundingClientRect();
                return [rect.left + 11, rect.top + 11];
            }
        }
        return null;
    }

}
