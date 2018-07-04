import {
  Component, OnInit, HostListener, ElementRef, Input, QueryList,
  ViewChildren, NgZone, ChangeDetectionStrategy, EventEmitter, Output,
  ChangeDetectorRef,
  AfterContentInit
} from '@angular/core';
import { Process } from 'app/models/Process';
import { Workflow } from 'app/models/Workflow';
import { Task, TaskState } from 'app/models/Task';
import { ProcessParameter } from 'app/models/ProcessParameter';
import { TaskComponent } from 'app/components/task/task.component';
import { trigger, transition, style, animate } from '@angular/animations';
import { window } from 'rxjs/operators/window';
import { AfterContentChecked } from '@angular/core/src/metadata/lifecycle_hooks';

/**
 * Metadata for mouse movement inside the editor.
 *
 * @interface MovementData
 */
interface MovementData {
  parameter?: ProcessParameter<'input' | 'output'>;
  edge?: [number, number, number, number];
  task?: Task;
  index?: number;
  x?: number;
  y?: number;
  before?: string;
}

/**
 * Editor Component.
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
        animate('233ms ease-in-out', style({ opacity: 0 }))
      ]),
    ])
  ]
})
export class EditorComponent implements OnInit, AfterContentInit {

  @Input()
  public workflow: Workflow;

  @Input()
  public processes: Process[];

  private movement: MovementData = {};

  private snapshots: Workflow[] = [];

  @ViewChildren(TaskComponent)
  public taskComponents: QueryList<TaskComponent>;


  @Output()
  public workflowChanged = new EventEmitter<Workflow>();

  @Input()
  public running = false;

  /**
   * Creates an instance of EditorComponent.
   *
   * @param {ElementRef} el
   * @param {NgZone} zone
   * @param {ChangeDetectorRef} cd
   * @memberof EditorComponent
   */
  public constructor(private el: ElementRef, private zone: NgZone, private cd: ChangeDetectorRef) {
  }


  /**
   * Component setup.
   *
   * @memberof EditorComponent
   */
  ngOnInit() {
    // Create initial workflow if no workflow is provided
    if (!this.workflow) {
      this.empty();
    }
  }

  /**
   * Is Called after all child components are ready.
   *
   * @memberof EditorComponent
   */
  ngAfterContentInit(): void {
    this.workflowChanged.emit(this.workflow);
    this.scrollToMiddle();
    setTimeout(() => this.detectChanges(), 100);
    setTimeout(() => this.detectChanges(), 1000);
  }


  /**
   * Empties snapshots
   *
   * @memberof EditorComponent
   */
  public empty() {
    this.snapshots = [];
    this.movement = {};
  }

  /**
   * Is called when an edge is clicked.
   *
   * @param edges the workflows edges
   */
  public clickEdge(edges) {

    // Delete edge
    if (this.running) { return; }

    const id = edges[4];
    const index = this.workflow.edges.findIndex(edge => edge.id === id);
    if (index !== -1) {
      this.snapshot();
      this.workflow.edges.splice(index, 1);
      this.workflowChanged.emit(this.workflow);
    }
  }

  /**
   * Move canvas to the middle.
   *
   * @memberof EditorComponent
   */
  public scrollToMiddle() {
    const native: HTMLElement = this.el.nativeElement;
    native.scrollTo(500, 500);
  }

  /**
   * Changes an artefact.
   *
   * @param event the event that triggers the call
   */
  public changeArtefact(event) {
    this.snapshot();
    let task: Task = event[0].task;
    task = this.workflow.tasks.find(t => t.id === task.id);
    const parameter: ProcessParameter<'input' | 'output'> = event[0].parameter;
    if (event[1] === null) {
      // Remove Artefact
      const index = task.input_artefacts.findIndex(artefact => artefact.parameter_id === parameter.id);
      if (index < 0) {
        return;
      }
      task.input_artefacts.splice(index, 1);
    } else {

      let changed = false;
      for (const entry of task.input_artefacts) {
        if (entry.parameter_id === event[0].parameter.id) {
          entry.data = event[1].value;
          entry.updated_at = (new Date).getTime();
          changed = true;
        }
      }
      if (!changed) {
        // Add artefact
        const data: any = event[1];
        if (parameter.role === 'input') {
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
      for (const currentInputArtefact of task.input_artefacts) {
        for (const currentEdge of this.workflow.edges) {
          if (currentEdge.to_task_id === currentInputArtefact.task_id && currentInputArtefact.parameter_id === currentEdge.input_id) {
            this.workflow.edges = this.workflow.edges.filter(e => e !== currentEdge);
          }
        }
      }
    }


    this.workflowChanged.emit(this.workflow);
  }

  /**
   * Returns edge as svg string.
   *
   * @param edge the edge
   * @param mouse the mouse
   */
  public getSvgEdge(edge: [number, number, number, number, number], mouse = false) {
    let delta = Math.abs(edge[1] - edge[3]);
    if (mouse === true && this.movement.parameter !== undefined) {
      delta *= this.movement.parameter.role === 'input' ? -1 : 1;
    }

    return `M ${edge[0]} ${edge[1]} C ${edge[0]} ${edge[1] + delta}, ${edge[2]} ${edge[3] - delta}, ${edge[2]} ${edge[3]}`;
  }

  /**
   * Returns edge coordinates for use in SVG.
   *
   * @readonly
   * @type {[number, number, number, number, number][]}
   * @memberof EditorComponent
   */
  public get edges(): [number, number, number, number, number][] {
    if (!this.taskComponents) {
      return [];
    }

    if (!this.workflow.edges) {
      this.workflow.edges = [];
    }

    const out = [];
    const n: HTMLElement = this.el.nativeElement;
    const r = n.getBoundingClientRect();


    for (const edge of this.workflow.edges) {
      const aComponent = this.taskComponents
        .find(component => component.task.id === edge.from_task_id);

      const bComponent = this.taskComponents
        .find(component => component.task.id === edge.to_task_id);

      if (!aComponent || !bComponent) {
        return;
      }

      const a = aComponent.getParameterPosition('output', edge.output_id);
      const b = bComponent.getParameterPosition('input', edge.input_id);

      if (a === null || b === null) {
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
   * Adds the process at the given coordinates.
   *
   * @param process the process to add
   * @param x x coordinate in the editor
   * @param y y coordinate in the editor
   */
  public add(process: Process, x: number, y: number) {
    this.snapshot();
    const timestamp = (new Date()).getTime();

    // create task
    const task: Task = {
      id: -Math.round(Math.random() * 10000),
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
   * Called when changes detected
   *
   * @private
   * @memberof EditorComponent
   */
  private detectChanges(): void {
    if (!this.cd['destroyed']) {
      this.cd.detectChanges();
    }
  }

  /**
   * Removes a task from the editor.
   *
   * @param task_id the id of the task
   */
  public remove(task_id: number) {
    if (this.running) {
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
   * Finds the process with the given id.
   *
   * @param id the id of the process
   */
  public findProcess(id: number): Process {
    return this.processes.find(process => process.id === id);
  }

  /**
   * Triggered when the user starts to drag an edge from
   * a parameter to somewhere else.
   *
   * @param index the parameter index
   * @param event the user clicks on a parameter node
   */
  public dragStart(index: number, event: MouseEvent) {
    if (event.button !== 0 || this.running) {
      return;
    }
    // store index of moved task
    // no move on input/output parameter
    if (!(<HTMLElement>event.target).classList.contains('nomove')) {
      let x = event.offsetX;
      let y = event.offsetY;
      if ((<HTMLElement>event.target).localName !== 'app-task') {
        x += 16;
        y += 16;
      }
      this.movement = { index, x, y, before: JSON.stringify(this.workflow) };
    } else {
      this.movement.index = undefined;
    }
  }

  /**
   * Triggerd when the user moves his mouse.
   *
   * @param {MouseEvent} event Mouse event
   * @memberof EditorComponent
   */
  @HostListener('mousedown', ['$event'])
  public mouseDown(event: MouseEvent) {
    this.zone.runOutsideAngular(() => {
      document.addEventListener('mousemove', this.mouseMove.bind(this));
    });

  }

  /**
   * Triggered when the user moves the cursor to
   * from a parameter node to somewhere creating an edge.
   *
   * @param event the user moves the mouse
   */
  public mouseMove(event: MouseEvent) {
    // return if no task / parameter is selected
    if (this.movement.index === undefined && this.movement.edge === undefined) {
      return true;
    }

    // get movement data
    const n: HTMLElement = this.el.nativeElement;
    const r = n.getBoundingClientRect();
    const { index, x, y } = this.movement;

    if (this.movement.edge === undefined) {
      // Task movement

      // calcualte new position
      this.workflow.tasks[index].x = event.pageX + n.scrollLeft - r.left - x;
      this.workflow.tasks[index].y = event.pageY + n.scrollTop - r.top - y - 20;

    } else {
      // Parameter line drawing
      this.movement.edge[0] = n.scrollLeft - r.left + x;
      this.movement.edge[1] = n.scrollTop - r.top + y;
      this.movement.edge[2] = event.pageX + n.scrollLeft - r.left;
      this.movement.edge[3] = event.pageY + n.scrollTop - r.top;
    }
    this.detectChanges();
  }

  /**
   * Triggered when the user releases the mouse button
   * when he drags an edge from one parameter node to
   * another.
   *
   * @param event the user releases the mouse button
   */
  @HostListener('mouseup')
  public dragEnd(event) {

    if (this.movement.before !== undefined) {
      this.snapshot(JSON.parse(this.movement.before));
    }

    // reset movement data
    this.movement = {};
    // reset cursor
    document.body.style.cursor = 'default';

    document.removeEventListener('mousemove', this.mouseMove);
  }

  /**
   * Returns allways false.
   * An indicator for browsers.
   *
   * @param event drag over event
   */
  public dragOver(event: DragEvent): boolean {
    // this needs to return false validate dropping area
    return false;
  }

  /**
   * Process is dropped.
   *
   * @param event user drops element
   */
  public drop(event: DragEvent) {
    // get process data from drag and drop event
    try {
      const process: Process = JSON.parse(event.dataTransfer.getData('json'));
      this.add(process, event.offsetX - 100, event.offsetY - 50);
    } catch (e) {
    }
  }

  /**
   * Drags a parameter.
   *
   * @param parameter the parameter
   * @param task the task
   */
  public parameterDrag(parameter: ProcessParameter<'input' | 'output'>, task: TaskComponent) {
    if (this.running) {
      return;
    }


    const [x, y] = task.getParameterPosition(parameter.role, parameter.id);

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
   * Drops a parameter.
   *
   * @param parameter the parameter
   * @param task the task
   */
  public parameterDrop(parameter: ProcessParameter<'input' | 'output'>, task: TaskComponent) {
    if (this.running || !this.movement.parameter || parameter.role === this.movement.parameter.role) {
      return;
    }

    // Check same type
    if (this.movement.parameter.type !== parameter.type) {
      return;
    }

    if (this.movement.edge) {
      this.snapshot();
      const input_id = parameter.role === 'input' ? parameter.id : this.movement.parameter.id;
      const output_id = parameter.role === 'output' ? parameter.id : this.movement.parameter.id;
      const from_task_id = parameter.role === 'output' ? task.task.id : this.movement.task.id;
      const to_task_id = parameter.role === 'input' ? task.task.id : this.movement.task.id;

      this.workflow.edges.push({ id: -Math.round(Math.random() * 10000), from_task_id, to_task_id, input_id, output_id });
      this.workflowChanged.emit(this.workflow);
    }
  }

  /**
   * Creates a new snapshot.
   *
   * @param workflow the workflow
   */
  private snapshot(workflow?: Workflow) {
    if (workflow) {
      this.snapshots.push(workflow);
    } else {
      this.snapshots.push(JSON.parse(JSON.stringify(this.workflow)));
    }
  }

  /**
   * Loads last workflow and thus reverts change.
   *
   * @returns {void}
   * @memberof EditorComponent
   */
  public undo(): void {
    if (this.running) {
      return;
    }
    const snapshot = this.snapshots.pop();
    if (snapshot !== undefined) {
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
  public canUndo(): boolean {
    return this.snapshots.length > 0 && !this.running;
  }
}
