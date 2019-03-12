import {SQLData} from '../../models/SQLData';
import {
    Component, OnInit, HostListener, ElementRef, Input, QueryList,
    ViewChildren, NgZone, ChangeDetectionStrategy, EventEmitter, Output,
    ChangeDetectorRef,
    AfterContentInit
} from '@angular/core';
import {Process} from 'app/models/Process';
import {Workflow} from 'app/models/Workflow';
import {Task, TaskState} from 'app/models/Task';
import {ProcessParameter, ProcessParameterType} from 'app/models/ProcessParameter';
import {TaskComponent} from 'app/components/task/task.component';
import {SQLDataComponent} from 'app/components/sqldata/sqldata.component';
import {trigger, transition, style, animate} from '@angular/animations';
import {window} from 'rxjs/operators/window';
import {AfterContentChecked} from '@angular/core/src/metadata/lifecycle_hooks';

/**
 * Metadata for mouse movement inside the editor. Holds Info on coords, index, etc of dragged Task, Edge or Data
 *
 * @interface MovementData
 */
interface MovementData
{
    /**
     *  Selected Input or Output an Edge comes from
     *  @type {ProcessParameter}
     */
    parameter?: ProcessParameter<'input' | 'output'>;
    /**
     * Vectors for the dragged edge
     */
    edge?: [number, number, number, number];
    /**
     * Task Object of dragged Task
     */
    task?: Task;
    /**
     * Index of dragged Task in workflow.tasks[] Array
     */
    index?: number;
    /**
     * Index of dragged Data in workflow.datas[] Array
     */
    dataId?: number;
    /**
     * Same as edge
     */
    dataEdge?: [number, number, number, number];

    /**
     * SqlData Object of dragged SqlData
     */
    data?: SQLData;
    /**
     * X-Coord of Task, Data or Parameter
     */
    x?: number;
    /**
     * Y-Coord of Task, Data or Parameter
     */
    y?: number;
    /**
     *
     */
    before?: string;
}

/**
 * Editor Component
 * Component for the workflow Editor
 *
 * @export
 * @class EditorComponent
 * @implements {OnInit}
 * @implements {AfterContentInit}
 */
@Component({
    selector: 'app-editor',
    templateUrl: './editor.component.html',
    styleUrls: ['./editor.component.scss'],
    changeDetection: ChangeDetectionStrategy.OnPush,
    animations: [
        trigger('fade', [
            transition(':leave', [
                animate('233ms ease-in-out', style({opacity: 0}))
            ]),
        ])
    ]
})
export class EditorComponent implements OnInit, AfterContentInit
{

    /**
     * current Workflow
     */
    @Input()
    public workflow: Workflow;

    /**
     * List of Processes loaded in DB
     */
    @Input()
    public processes: Process[];

    /**
     * Metadata Variable for Movement Data
     */
    private movement: MovementData = {};

    /**
     * List for undo Button
     */
    private snapshots: Workflow[] = [];

    /**
     * List of all Task Components in Editor
     */
    @ViewChildren(TaskComponent)
    public taskComponents: QueryList<TaskComponent>;

    /**
     * List of all Data Components in Editor
     */
    @ViewChildren(SQLDataComponent)
    public sqldataComponents: QueryList<SQLDataComponent>;

    /**
     * Emitter for updating current Workflow
     */
    @Output()
    public workflowChanged = new EventEmitter<Workflow>();

    /**
     * Status indicating if Workflow is running or not
     */
    @Input()
    public running = false;

    /**
     * Constructor of Component
     * Creates an instance of EditorComponent.
     *
     * @param {ElementRef} el
     * @param {NgZone} zone
     * @param {ChangeDetectorRef} cd
     * @memberof EditorComponent
     */
    public constructor(private el: ElementRef, private zone: NgZone, private cd: ChangeDetectorRef)
    {
    }


    /**
     * Component setup.
     * Creates initial workflow if no workflow is provided
     *
     * @memberof EditorComponent
     */
    ngOnInit()
    {
        // Create initial workflow if no workflow is provided
        if (!this.workflow)
        {
            this.empty();
        }
    }

    /**
     * Is Called after all child components are ready.
     *
     * @memberof EditorComponent
     */
    ngAfterContentInit(): void
    {
        this.workflowChanged.emit(this.workflow);
        this.scrollToMiddle();
        setTimeout(() => this.detectChanges(), 100);
        setTimeout(() => this.detectChanges(), 1000);
    }


    /**
     * Empties snapshots list and movement variable
     *
     * @memberof EditorComponent
     */
    public empty()
    {
        this.snapshots = [];
        this.movement = {};
    }

    /**
     * Is called when an edge is clicked.
     * Deletes the clicked Edge
     *
     * @param edges The edges in workflow
     */
    public clickEdge(edges)
    {
        // Delete edge
        if (this.running)
        {
            return;
        }

        const id = edges[4];
        const index = this.workflow.edges.findIndex(edge => edge.id === id);
        if (index !== -1)
        {
            this.snapshot();
            this.workflow.edges.splice(index, 1);
            this.workflowChanged.emit(this.workflow);
        }
    }


    /**
     * Is called when an dataEdge is clicked.
     * Deletes the clicked Edge
     *
     * @param dataEdges The dataEdges in workflow
     */
    public clickDataEdge(dataEdges)
    {
        // Delete edge
        if (this.running)
        {
            return;
        }

        const id = dataEdges[4];
        const index = this.workflow.dataEdges.findIndex(dataEdge => dataEdge.id === id);
        if (index !== -1)
        {
            this.snapshot();
            this.workflow.dataEdges.splice(index, 1);
            this.workflowChanged.emit(this.workflow);
        }
    }

    /**
     * Moves canvas to the middle of the screen when a workflow is loaded or Editor is initialized.
     *
     *
     * @memberof EditorComponent
     */
    public scrollToMiddle()
    {
        const native: HTMLElement = this.el.nativeElement;
        native.scrollTop;
    }

    /**
     * Changes an artefact.
     * Deletes or changes the value of an Artefact according to Edges
     *
     * @param event The event that triggers the call. Holds Parameter and Data values to create a new Artefact
     */
    public changeArtefact(event)
    {
        this.snapshot();
        let task: Task = event[0].task;
        task = this.workflow.tasks.find(t => t.id === task.id);
        const parameter: ProcessParameter<'input' | 'output'> = event[0].parameter;
        if (event[1] === null)
        {
            // Remove Artefact
            const index = task.input_artefacts.findIndex(artefact => artefact.parameter_id === parameter.id);
            if (index < 0)
            {
                return;
            }
            task.input_artefacts.splice(index, 1);
        } else
        {

            let changed = false;
            for (const entry of task.input_artefacts)
            {
                if (entry.parameter_id === event[0].parameter.id)
                {
                    entry.data = event[1].value;
                    entry.updated_at = (new Date).getTime();
                    changed = true;
                }
            }
            if (!changed)
            {
                // Add artefact
                const data: any = event[1];
                if (parameter.role === 'input')
                {
                    task.input_artefacts = task.input_artefacts || [];
                    task.input_artefacts.push({
                        parameter_id: parameter.id,
                        task_id: task.id,
                        workflow_id: this.workflow.id,
                        role: parameter.role,
                        format: data.format,
                        data: data.value,
                        created_at: (new Date).getTime(),
                        updated_at: (new Date).getTime(),
                    });
                }
            }
            for (const currentInputArtefact of task.input_artefacts)
            {
                for (const currentEdge of this.workflow.edges)
                {
                    if (currentEdge.to_task_id === currentInputArtefact.task_id && currentInputArtefact.parameter_id === currentEdge.input_id)
                    {
                        this.workflow.edges = this.workflow.edges.filter(e => e !== currentEdge);
                    }
                }
                for (const currentDataEdge of this.workflow.dataEdges)
                {
                    if (currentDataEdge.to_task_id === currentInputArtefact.task_id && currentInputArtefact.parameter_id === currentDataEdge.task_input_id)
                    {
                        this.workflow.dataEdges = this.workflow.dataEdges.filter(e => e !== currentDataEdge);
                    }
                }
            }
        }


        this.workflowChanged.emit(this.workflow);
    }

    /**
     * Returns edge as svg string.
     *
     * @param edge The edge to be returned as string
     * @param {bool} mouse the mouse
     */
    public getSvgEdge(edge: [number, number, number, number, number], mouse = false)
    {
        let delta = Math.abs(edge[1] - edge[3]);
        if (mouse === true && this.movement.dataId !== undefined)
        {
            delta *= 1;
        }
        if (mouse === true && this.movement.parameter !== undefined)
        {
            delta *= this.movement.parameter.role === 'input' ? -1 : 1;
        }

        return `M ${edge[0]} ${edge[1]} C ${edge[0]} ${edge[1] + delta}, ${edge[2]} ${edge[3] - delta}, ${edge[2]} ${edge[3]}`;
    }

    /**
     * Returns dataEdge as svg string.
     *
     * @param edge The edge to be returned as string
     * @param {bool} mouse the mouse
     */
    public getSvgDataEdge(dataedge: [number, number, number, number, number], mouse = false)
    {
        let delta = Math.abs(dataedge[1] - dataedge[3]);
        if (mouse === true && this.movement.dataId !== undefined)
        {
            delta *= 1;
        }
        if (mouse === true && this.movement.parameter !== undefined)
        {
            delta *= this.movement.parameter.role === 'input' ? -1 : 1;
        }

        return `M ${dataedge[0]} ${dataedge[1]} C ${dataedge[0]} ${dataedge[1] + delta}, ${dataedge[2]} ${dataedge[3] - delta}, ${dataedge[2]} ${dataedge[3]}`;
    }

    /**
     * Returns edge coordinates for use in SVG.
     *
     * @readonly
     * @type {[number, number, number, number, number][]}
     * @memberof EditorComponent
     */
    public get edges(): [number, number, number, number, number][]
    {
        if (!this.taskComponents)
        {
            return [];
        }

        if (!this.workflow.edges)
        {
            this.workflow.edges = [];
        }

        const out = [];
        const n: HTMLElement = this.el.nativeElement;
        const r = n.getBoundingClientRect();


        for (const edge of this.workflow.edges)
        {

            const aComponent = this.taskComponents
                .find(component => component.task.id === edge.from_task_id);

            const bComponent = this.taskComponents
                .find(component => component.task.id === edge.to_task_id);

            if (!aComponent || !bComponent)
            {
                return;
            }

            const a = aComponent.getParameterPosition('output', edge.output_id);
            const b = bComponent.getParameterPosition('input', edge.input_id);

            if (a === null || b === null)
            {
                return;
            }

            out.push([
                a[0] - r.left + n.scrollLeft,
                a[1] - r.top + n.scrollTop,
                b[0] - r.left + n.scrollLeft,
                b[1] - r.top + n.scrollTop,
                edge.id
            ]);
        }
        return out;
    }

    /**
     * Returns data edge coordinates for use in SVG.
     *
     * @readonly
     * @type {[number, number, number, number, number][]}
     * @memberof EditorComponent
     */
    public get dataedges(): [number, number, number, number, number][]
    {
        if (!this.sqldataComponents || !this.taskComponents)
        {
            return [];
        }

        if (!this.workflow.dataEdges)
        {
            this.workflow.dataEdges = [];
        }

        const out = [];
        const n: HTMLElement = this.el.nativeElement;
        const r = n.getBoundingClientRect();


        for (const dataEdge of this.workflow.dataEdges)
        {

            const aComponent = this.sqldataComponents
                .find(component => component.sqldata.id === dataEdge.from_sqldata_id);

            const bComponent = this.taskComponents
                .find(component => component.task.id === dataEdge.to_task_id);

            if (!aComponent || !bComponent)
            {
                return;
            }

            const a = aComponent.getDataPosition(0);
            const b = bComponent.getParameterPosition('input', dataEdge.task_input_id);

            if (a === null || b === null)
            {
                return;
            }

            out.push([
                a[0] - r.left + n.scrollLeft,
                a[1] - r.top + n.scrollTop,
                b[0] - r.left + n.scrollLeft,
                b[1] - r.top + n.scrollTop,
                dataEdge.id
            ]);
        }
        return out;
    }


    /**
     * Adds a Process as Task to the Editor and Workflow at the given coordinates.
     *
     * @param process the selected process to add
     * @param x x coordinate in the editor
     * @param y y coordinate in the editor
     */
    public add(process: Process, x: number, y: number)
    {
        this.snapshot();
        const timestamp = (new Date()).getTime();

        // create task
        const task: Task = {
            id: -Math.round(Math.random() * 10000),
            title: process.title,
            x,
            y,
            state: TaskState.NONE,
            process_id: process.id,
            input_artefacts: [],
            output_artefacts: [],
            created_at: timestamp,
            updated_at: timestamp,
        };

        // add task to current workflow
        this.workflow.tasks.push(task);
        this.workflowChanged.emit(this.workflow);
        this.detectChanges();
    }

    /**
     * Adds a dropped Dataset from vfwportal Datastore as Data Object to the Editor and Workflow
     *
     * @param data value of dataset representing id of query in database
     * @param x X Coordinate in Editor
     * @param y Y Coordinate in Editor
     */
    public addData(data: number, x: number, y: number)
    {
        const dataElement: SQLData = {
            id: -Math.round(Math.random() * 10000),
            title: "SQL Query id " + data,
            x,
            y,
            data,
        };

        if (this.workflow.datas === undefined)
        {
            this.workflow = {
                id: this.workflow.id,
                title: this.workflow.title,
                edges: this.workflow.edges,
                tasks: this.workflow.tasks,
                datas: [],
                dataEdges: [],
                creator_id: this.workflow.creator_id,
                shared: this.workflow.shared,
                created_at: this.workflow.created_at,
                updated_at: this.workflow.updated_at,
                percent_done: this.workflow.percent_done,
            };
            this.workflowChanged.emit(this.workflow);
            this.detectChanges();
        }

        this.workflow.datas.push(dataElement);
        this.workflowChanged.emit(this.workflow);
        this.detectChanges();
    }

    /**
     * Called when changes detected
     *
     * @private
     * @memberof EditorComponent
     */
    private detectChanges(): void
    {
        if (!this.cd['destroyed'])
        {
            this.cd.detectChanges();
        }
    }

    /**
     * Removes a task from the editor.
     *
     *
     * @param task_id the id of the task to remove
     */
    public remove(task_id: number)
    {
        if (this.running)
        {
            return;
        }

        this.snapshot();
        const index = this.workflow.tasks.findIndex(task => task.id === task_id);
        this.workflow.tasks.splice(index, 1);
        this.workflow.edges = this.workflow.edges.filter(edge => edge.from_task_id !== task_id && edge.to_task_id !== task_id);

        this.detectChanges();
        this.workflowChanged.emit(this.workflow);
    }

    /**
     * Removes a Data from the Editor.
     *
     * @param data_id the id of the data object to remove
     */
    public dataRemove(data_id: number)
    {
        if (this.running)
        {
            return;
        }

        this.snapshot();
        const index = this.workflow.datas.findIndex(sqldata => sqldata.id === data_id);
        this.workflow.datas.splice(index, 1);
        this.workflow.dataEdges = this.workflow.dataEdges.filter(dataEdge => dataEdge.from_sqldata_id !== data_id);

        this.detectChanges();
        this.workflowChanged.emit(this.workflow);
    }

    /**
     * Finds the process with the given id.
     *
     * @param id the id of the process
     */
    public findProcess(id: number): Process
    {
        return this.processes.find(process => process.id === id);
    }

    /**
     * EventListener for dragStart Event
     * Triggered when the user starts to drag an edge from
     * a parameter to somewhere else and saves metadata to movement var.
     * resets movement.index when no parameter is dragged
     *
     * @param index the parameter index
     * @param {MouseEvent} event event var
     */
    public dragStart(index: number, event: MouseEvent)
    {
        if (event.button !== 0 || this.running)
        {
            return;
        }
        // store index of moved task
        // no move on input/output parameter
        if (!(<HTMLElement>event.target).classList.contains('nomove'))
        {
            let x = event.offsetX;
            let y = event.offsetY;
            if ((<HTMLElement>event.target).localName !== 'app-task' && (<HTMLElement>event.target).localName !== 'app-sqldata')
            {
                x += 16;
                y += 16;
            }
            this.movement = {index, x, y, before: JSON.stringify(this.workflow)};
        } else
        {
            this.movement.index = undefined;
        }
    }

    /**
     * EventListener for dragStart Event on Data
     * Triggered when the user starts to drag an edge from
     * a Data output to somewhere else and saves metadata to movement var.
     * resets movement.index when no parameter is dragged
     *
     * @param dataId The index of the Data Element in workflow.datas[]
     * @param {MouseEvent} event Event var
     */
    public dataDragStart(dataId: number, event: MouseEvent)
    {
        if (event.button !== 0 || this.running)
        {
            return;
        }
        // store index of moved task
        // no move on input/output parameter
        if (!(<HTMLElement>event.target).classList.contains('nomove'))
        {
            let x = event.offsetX;
            let y = event.offsetY;
            if ((<HTMLElement>event.target).localName !== 'app-sqldata' && (<HTMLElement>event.target).localName !== 'app-task')
            {
                x += 16;
                y += 16;
            }
            this.movement = {dataId, x, y, before: JSON.stringify(this.workflow)};
        } else
        {
            //this.movement.index = undefined;
            this.movement.dataId = undefined; //this.workflow.datas[data].data;
        }
    }

    /**
     * EventListener for mouseDown Event
     * Triggerd when the user clicks (and holds) the left mouse Button.
     * Adds and binds the mousemove Eventlistener
     *
     * @param {MouseEvent} event Mouse event
     * @memberof EditorComponent
     */
    @HostListener('mousedown', ['$event'])
    public mouseDown(event: MouseEvent)
    {
        this.zone.runOutsideAngular(() =>
        {
            document.addEventListener('mousemove', this.mouseMove.bind(this));
        });

    }

    /**
     * EventListener for mouseMove Event
     * Calculates the Coordinates for moving a Task, Data or Edge
     * Triggered when the user moves his mouse.
     * Is only triggered when the right mouse Button is clicked (or held down)
     * Reason: The associated Eventlistener is only added when mouseDown is triggered
     *
     *
     *
     * @param {MouseEvent} event Event variable
     */
    public mouseMove(event: MouseEvent)
    {
        // return if no task / parameter is selected
        if (this.movement.index === undefined && this.movement.edge === undefined && this.movement.dataId === undefined && this.movement.dataEdge === undefined)
        {
            return true;
        }

        // get movement data
        const n: HTMLElement = this.el.nativeElement;
        const r = n.getBoundingClientRect();
        const {index, dataId, x, y} = this.movement;


        if (this.movement.edge === undefined && this.movement.dataId === undefined && this.movement.dataEdge === undefined)
        {
            // Task movement
            // calcualte new position
            this.workflow.tasks[index].x = event.pageX + n.scrollLeft - r.left - x;
            this.workflow.tasks[index].y = event.pageY + n.scrollTop - r.top - y - 20;
        }
        else if (this.movement.edge === undefined && this.movement.index === undefined && this.movement.dataEdge == undefined)
        {
            this.workflow.datas[dataId].x = event.pageX + n.scrollLeft - r.left - x;
            this.workflow.datas[dataId].y = event.pageY + n.scrollTop - r.top - y - 20;
        }
        else if (this.movement.index === undefined && this.movement.dataEdge == undefined && this.movement.dataId === undefined)
        {
            // Parameter line drawing
            this.movement.edge[0] = n.scrollLeft - r.left + x;
            this.movement.edge[1] = n.scrollTop - r.top + y;
            this.movement.edge[2] = event.pageX + n.scrollLeft - r.left;
            this.movement.edge[3] = event.pageY + n.scrollTop - r.top;
        }
        else if (this.movement.index === undefined && this.movement.edge == undefined && this.movement.dataId === undefined)
        {
            // Data line drawing
            this.movement.dataEdge[0] = n.scrollLeft - r.left + x;
            this.movement.dataEdge[1] = n.scrollTop - r.top + y;
            this.movement.dataEdge[2] = event.pageX + n.scrollLeft - r.left;
            this.movement.dataEdge[3] = event.pageY + n.scrollTop - r.top;
        }
        this.detectChanges();
    }

    /**
     * EventListener for dragEnd Event
     * Detects the end of a drag event.
     * Resets movement var and unbinds mousemove listener
     * Triggered when the user releases the mouse button
     * when he drags an edge from one parameter node to
     * another.
     *
     * @param event Event var
     */
    @HostListener('mouseup')
    public dragEnd(event)
    {

        if (this.movement.before !== undefined)
        {
            this.snapshot(JSON.parse(this.movement.before));
        }

        // reset movement data
        this.movement = {};
        // reset cursor
        document.body.style.cursor = 'default';

        document.removeEventListener('mousemove', this.mouseMove);
    }

    /**
     * EventListener for dragOver Event
     * An indicator for browsers, always returns false
     *
     * @param {DragEvent} event drag over event var
     * @returns bool false
     */
    public dragOver(event: DragEvent): boolean
    {
        // this needs to return false validate dropping area
        return false;
    }

    /**
     * EventListener for drop Event
     * Triggered when Process or Data is dropped into the Editor and adds them to the workflow
     *
     * @param {DragEvent} event Event var
     */
    public drop(event: DragEvent)
    {
        // get process data from drag and drop event
        try
        {
            const data = parseInt(event.dataTransfer.getData('data'), 10);
            if (!isNaN(data))
            {
                this.addData(data, event.offsetX - 100, event.offsetY - 50);
            }
            else
            {
                const process: Process = JSON.parse(event.dataTransfer.getData('json'));
                this.add(process, event.offsetX - 100, event.offsetY - 50);
            }
        } catch (e)
        {
            console.log(e)
        }
    }

    /**
     * Starts the parameter edge drag from a Task. Saves Task, Parameter and coords to movement var
     *
     * @param parameter the dragged parameter
     * @param task the task the parameter is dragged from
     */
    public parameterDrag(parameter: ProcessParameter<'input' | 'output'>, task: TaskComponent)
    {
        if (this.running)
        {
            return;
        }


        const [x, y] = task.getParameterPosition(parameter.role, parameter.id);


        console.log('parameterDrag!');

        this.movement = {
            edge: [0, 0, 0, 0],
            task: task.task,
            parameter,
            x, y
        };

        // Set cursor
        document.body.style.cursor = 'pointer';
    }

    /**
     * Handler for when an Edge from a Parameter is dropped onto another Parameter
     * Calculates and adds the according edge between the tasks to the workflow.
     * If one end of the edge is a Data Element, the input artefact data of the task is set to the data held in the
     * data element
     *
     * @param parameter the parameter an edge is dropped to
     * @param task the task to the dropped to parameter
     */
    public parameterDrop(parameter: ProcessParameter<'input' | 'output'>, task: TaskComponent)
    {
        if (this.running)
        {
            return;
        }
        if (this.movement.dataEdge)
        {
            if (parameter.role === 'output')
            {
                return
            }
            if (parameter.type !== ProcessParameterType.LITERAL)
            {
                return;
            }

            this.snapshot();
            const task_input_id = parameter.id;
            const from_sqldata_id = this.movement.data.id;
            const to_task_id = task.task.id;

            this.workflow.dataEdges.push({
                id: -Math.round(Math.random() * 10000),
                from_sqldata_id,
                to_task_id,
                task_input_id
            });
            this.workflowChanged.emit(this.workflow);
        }

        if (this.movement.edge)
        {
            if (!this.movement.parameter || parameter.role === this.movement.parameter.role)
            {
                return;
            }

            // Check same type
            if (this.movement.parameter.type !== parameter.type)
            {
                return;
            }

            this.snapshot();
            const input_id = parameter.role === 'input' ? parameter.id : this.movement.parameter.id;
            const output_id = parameter.role === 'output' ? parameter.id : this.movement.parameter.id;
            const from_task_id = parameter.role === 'output' ? task.task.id : this.movement.task.id;
            const to_task_id = parameter.role === 'input' ? task.task.id : this.movement.task.id;

            this.workflow.edges.push({
                id: -Math.round(Math.random() * 10000),
                from_task_id,
                to_task_id,
                input_id,
                output_id
            });
            this.workflowChanged.emit(this.workflow);
        }
    }


    /**
     * Starts the data edge drag from an Data Element.
     * Saves data indes and coords to movement var
     *
     * @param {SQLDataComponent} Data the data Element Component the drag is started from
     */
    public dataDrag(SqlData: SQLDataComponent)
    {
        console.log("before data drag!" + SqlData.sqldata.data);
        const [x, y] = SqlData.getDataPosition(0);
        const index = this.workflow.datas.findIndex(sqldata => sqldata.data === SqlData.sqldata.data);

        this.movement = {
            //dataId: index,
            dataEdge: [0, 0, 0, 0],
            data: SqlData.sqldata,
            x, y
        };

        // Set cursor
        document.body.style.cursor = 'pointer';
    }

    /**
     * Handler for when an endge is dropped to an data Element
     *
     * @param {SQLDataComponent} data the data element an edge is dropped to
     */
    public dataDrop(SqlData: SQLDataComponent)
    {
        console.log("data drop!");
        if (this.running ) //|| !this.movement.edge || !this.movement.parameter ) //|| this.movement.parameter.type !== ProcessParameterType.LITERAL)
        {
            return;
        }

        console.log("edge?" + this.movement.edge);
        if (this.movement.edge)
        {
            this.snapshot();
            
            console.log("data drop!");

            const task_input_id = this.movement.parameter.id;
            const from_sqldata_id = SqlData.sqldata.id;
            const to_task_id = this.movement.task.id;

            this.workflow.dataEdges.push({
                id: -Math.round(Math.random() * 10000),
                from_sqldata_id,
                to_task_id,
                task_input_id
            });

            this.workflowChanged.emit(this.workflow);
            
            console.log("dataedge should be there");
        }
    }

    /**
     * Creates a new snapshot.
     *
     * @param workflow the workflow
     */
    private snapshot(workflow?: Workflow)
    {
        if (workflow)
        {
            this.snapshots.push(workflow);
        } else
        {
            this.snapshots.push(JSON.parse(JSON.stringify(this.workflow)));
        }
    }

    /**
     * Loads last workflow and thus reverts change.
     *
     * @returns {void}
     * @memberof EditorComponent
     */
    public undo(): void
    {
        if (this.running)
        {
            return;
        }
        const snapshot = this.snapshots.pop();
        if (snapshot !== undefined)
        {
            this.workflow = snapshot;
        }
        this.detectChanges();
        this.workflowChanged.emit(this.workflow);
    }

    /**
     * Is supposed to return true if there is the
     * last snapshot and the workflow is not running
     * else returns false.
     *
     * @returns {boolean} Can undo
     * @memberof EditorComponent
     */
    public canUndo(): boolean
    {
        return this.snapshots.length > 0 && !this.running;
    }
}
