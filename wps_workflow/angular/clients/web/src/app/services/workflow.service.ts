import { Injectable } from '@angular/core';
import { Workflow } from '../models/Workflow';
import { Edge } from '../models/Edge';
import { TaskState } from '../models/Task';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs/Observable';
import { map, switchMap } from 'rxjs/operators';
import { MatSnackBar } from '@angular/material';
import { Process } from 'app/models/Process';
import { ProcessService } from 'app/services/process.service';
import { environment } from 'environments/environment';

/**
 * Different workflow validation results
 */
export enum WorkflowValidationResult {
  /**
   * Unknown Error
   */
  ERROR,
  /**
   * Valid workflow
   */
  SUCCESSFUL,
  /**
   * Workflow title too long
   */
  TITLE_TOO_LONG,
  /**
   * Workflow title too short
   */
  TITLE_TOO_SHORT,
  /**
   * Workflow is empty
   */
  EMPTY,
  /**
   * Workflow has a task with loop to itself
   */
  LOOP_TO_SAME_TASK,
  /**
   * Workflow has edges to tasks with not matching in-/output types
   */
  WRONG_INPUT_TYPES,
  /**
   * Workflow has a task without inputs
   */
  MISSING_TASK_INPUT,
  /**
   * Missing Workflow
   */
  MISSING_WORKFLOW,
  /**
   * Missing Processes
   */
  MISSING_PROCESSES,
  /**
   * Workflow has a cycle
   */
  CYCLE_IN_WORKFLOW,
  /**
   * Workflow has task with multiple inputs
   */
  MULIPLE_INPUTS,
}

/**
 * Fetches workflow data from server.
 *
 * @export
 * @class WorkflowService
 */
@Injectable()
export class WorkflowService {
  private processes?: Process[];

  /**
   * Constructs workflowService.
   *
   * @param {HttpClient} http
   * @param {MatSnackBar} bar
   * @param {ProcessService} processService
   */
  constructor(private http: HttpClient, private bar: MatSnackBar, private processService: ProcessService) {
    this.processService.all().subscribe(processes => this.processes = processes);
  }

  /**
   * Returns Observable of all Workflows.
   *
   * @returns {Observable<Workflow[]>}
   */
  public all(): Observable<Workflow[]> {
    return this.http.get<Workflow[]>(`${environment.ip}/workflow/`, { withCredentials: true });
  }

  /**
   * Returns Observable of the Workflow with the given id.
   *
   * @param {number} id
   * @returns {Observable<Workflow>}
   */
  public get(id: number): Observable<Workflow> {
    return this.http.get<Workflow>(`${environment.ip}/workflow/${id}`, { withCredentials: true });
  }

  /**
   * Create an Observable to a given partial workflow.
   *
   * @param {Partial<Workflow>} workflow
   * @returns {Observable<Workflow>}
   */
  public create(workflow: Partial<Workflow>): Observable<Workflow> {
    return this.http.post<Workflow>(`${environment.ip}/workflow/`, workflow, { withCredentials: true });
  }

  /**
   * Refreshes the observable of the given workflow.
   *
   * @param {number} id
   * @param {Partial<Workflow>} workflow
   * @returns {Observable<Workflow>}
   */
  public update(id: number, workflow: Partial<Workflow>): Observable<Workflow> {
    this.bar.open(`Updated Workflow`, 'CLOSE', { duration: 2500 });
    return this.http.patch<Workflow>(`${environment.ip}/workflow/${id}`, workflow, { withCredentials: true });
  }

  /**
   * Removes the workflow with the given id.
   *
   * @param {number} id
   * @returns {Promise<boolean>}
   */
  public async remove(id: number): Promise<boolean> {
    this.bar.open(`Deleted Workflow`, 'CLOSE', { duration: 2500 });
    return this.http.delete<boolean>(`${environment.ip}/workflow/${id}`, { withCredentials: true }).toPromise();

  }

  /**
   * Returns if the workflow is running (workflow can't be running if not runnable).
   *
   * @param {Partial<Workflow>} workflow
   * @returns {boolean}
   */
  public isRunning(workflow: Partial<Workflow>): boolean {
    if (!workflow || !workflow.tasks || workflow.tasks.length === 0) {
      return false;
    }
    for (const task of workflow.tasks) {
      if (task.state !== TaskState.NONE) {
        return true;
      }
    }
    return false;
  }

  /**
   * Checks whether a workflow is finished.
   *
   * @param {Partial<Workflow>} workflow Workflow to check
   * @returns {boolean} Finished
   * @memberof WorkflowService
   */
  public finished(workflow: Partial<Workflow>): boolean {
    if (!workflow || !workflow.tasks || workflow.tasks.length === 0) {
      return false;
    }

    for (const task of workflow.tasks) {
      if (task.state !== TaskState.FINISHED
        && task.state !== TaskState.DEPRECATED
        && task.state !== TaskState.FAILED) {
        return false;
      }
    }

    return true;
  }

  /**
   * Returns if the workflow is a valid workflow for execution.
   *
   * @param {Workflow} workflow
   * @returns {WorkflowValidationResult}
   */
  public validate(workflow: Workflow): WorkflowValidationResult {
    if (!workflow) {
      return WorkflowValidationResult.MISSING_WORKFLOW;
    } else if (!this.processes) {
      return WorkflowValidationResult.MISSING_PROCESSES;
    }

    // check name
    if (!workflow.title || workflow.title.length > 255) {
      return WorkflowValidationResult.TITLE_TOO_LONG;
    } else if (workflow.title.length < 1) {
      return WorkflowValidationResult.TITLE_TOO_SHORT;
    } else if (workflow.tasks && workflow.tasks.length < 1) {
      return WorkflowValidationResult.EMPTY;
    } else if (workflow.edges) {
      for (let i = 0; i < workflow.edges.length; i++) {
        // check for loop to same task
        if (workflow.edges[i].from_task_id === workflow.edges[i].to_task_id) {
          return WorkflowValidationResult.LOOP_TO_SAME_TASK;
        }
        // check for wrong input types
        let inputTaskNumber: number = null;
        let outputTaskNumber: number = null;
        for (let j = 0; j < workflow.tasks.length; j++) {
          if (workflow.tasks[j].id === workflow.edges[i].to_task_id) {
            inputTaskNumber = workflow.tasks[j].process_id;
          }
          if (workflow.tasks[j].id === workflow.edges[i].from_task_id) {
            outputTaskNumber = workflow.tasks[j].process_id;
          }
        }
        let inputProcessNumber: number = null;
        let outputPrecessNumber: number = null;
        for (let k = 0; k < this.processes.length; k++) {
          if (this.processes[k].id === inputTaskNumber) {
            inputProcessNumber = k;
          }
          if (this.processes[k].id === outputTaskNumber) {
            outputPrecessNumber = k;
          }
        }
        let processParameterTypeCorrect = false;
        for (let l = 0; l < this.processes[inputProcessNumber].inputs.length; l++) {
          for (let m = 0; m < this.processes[outputPrecessNumber].outputs.length; m++) {
            if (this.processes[inputProcessNumber].inputs[l].type === this.processes[outputPrecessNumber].outputs[m].type) {
              processParameterTypeCorrect = true;
            }
          }
        }
        if (!processParameterTypeCorrect) {
          return WorkflowValidationResult.WRONG_INPUT_TYPES;
        }
      }

    }
    // check for missing input
    if (workflow.tasks && workflow.edges) {
      for (let i = 0; i < workflow.tasks.length; i++) {
        let numberOfInputs = 0;
        for (let k = 0; k < workflow.edges.length; k++) {
          if (workflow.edges[k].to_task_id === workflow.tasks[i].id) {
            numberOfInputs++;
          }
        }

        numberOfInputs += workflow.tasks[i].input_artefacts.length;

        for (let j = 0; j < this.processes.length; j++) {
          if (workflow.tasks[i].process_id === this.processes[j].id) {
            if (numberOfInputs < this.processes[j].inputs.length) {
              return WorkflowValidationResult.MISSING_TASK_INPUT;
            }
          }
        }
      }
    }
    // cycle check
    if (workflow.tasks && workflow.edges) {
      for (let i = 0; i < workflow.tasks.length; i++) {
        for (let j = 0; j < workflow.edges.length; j++) {
          let checkedTasks: number[] = [];
          if (workflow.tasks[i].id === workflow.edges[j].to_task_id) {


            const visitedTasks: number[] = [];
            if (!this.contains(checkedTasks, workflow.edges[j].from_task_id)) {
              if (this.checkCycle(workflow.edges[j], workflow, visitedTasks)) {
                return WorkflowValidationResult.CYCLE_IN_WORKFLOW;
              }
              checkedTasks = visitedTasks;
            }
          }
        }
      }
    }

    // check for multiple inputs
    if (workflow.edges) {
      for (let i = 0; i < workflow.edges.length; i++) {
        for (let j = i + 1; j < workflow.edges.length; j++) {
          if (workflow.edges[i].to_task_id === workflow.edges[j].to_task_id && workflow.edges[i].input_id === workflow.edges[j].input_id) {
            return WorkflowValidationResult.MULIPLE_INPUTS;
          }
        }
      }
    }


    return WorkflowValidationResult.SUCCESSFUL;
  }

  /**
   * Checks if an array contains a variable.
   *
   * @param {Array<T>} array
   * @param {T} variable
   * @returns {boolean}
   */
  private contains<T>(array: Array<T>, variable: T): boolean {
    for (let i = 0; i < array.length; i++) {
      if (array[i] === variable) {
        return true;
      }
    }
    return false;
  }

  /**
   * Recursive method to check for cycle in workflow.
   *
   * @param {Edge} currentWorkflowEdge starting edge
   * @param {Partial<Workflow>} workflow entire workflow
   * @param {number[]} visitedTasks list of visited Tasks (empty for 1st run)
   * @returns {boolean}
   */
  private checkCycle(currentWorkflowEdge: Edge, workflow: Partial<Workflow>, visitedTasks: number[]): boolean {
    visitedTasks.push(currentWorkflowEdge.to_task_id);
    // check task at end of edge
    for (let i = 0; i < workflow.tasks.length; i++) {
      if (this.contains(visitedTasks, currentWorkflowEdge.from_task_id)) {
        return true;
      }
      if (workflow.tasks[i].id === currentWorkflowEdge.to_task_id) {
        // check for new edges at task
        let cycle = false;
        for (let j = 0; j < workflow.edges.length; j++) {
          if (workflow.edges[j].to_task_id === currentWorkflowEdge.to_task_id) {
            if (this.contains(visitedTasks, workflow.edges[j].from_task_id)) {
              return true;
            }
            for (let l = 0; l < workflow.edges.length; l++) {
              if (workflow.edges[j].from_task_id === workflow.edges[l].to_task_id) {
                const newVisitedTasks: number[] = [];
                for (let k = 0; k < visitedTasks.length; k++) {
                  newVisitedTasks.push(visitedTasks[k]);
                }
                cycle = cycle || this.checkCycle(workflow.edges[l], workflow, newVisitedTasks);
              }
            }
          }
        }
        return cycle;
      }
    }
    return false;
  }

  /**
   * Execute given workflow.
   *
   * @param {number} id
   * @returns {Promise<boolean>}
   */
  public async start(id: number): Promise<boolean> {
    const result = await this.http.get<any>(`${environment.ip}/workflow_start/${id}`).toPromise();

    if (result['error']) {
      this.bar.open(result['error'], 'CLOSE', { duration: 5000 });
      return false;
    } else {
      return true;
    }
  }

  /**
   * Refreshes workflow by a given workflow ID.
   *
   * @param {number} id Workflow ID
   * @returns {Promise<boolean>} Refresh successful
   * @memberof WorkflowService
   */
  public async refresh(id: number): Promise<boolean> {
    const result = await this.http.get<any>(`${environment.ip}/workflow_refresh/${id}`).toPromise();
    if (result['error']) {
      this.bar.open(result['error'], 'CLOSE', { duration: 5000 });
      return false;
    } else {
      return true;
    }
  }

  /**
   * Stops workflow by a given workflow id.
   *
   * @param {number} id Workflow ID
   * @returns {Promise<boolean>} Stop successful
   * @memberof WorkflowService
   */
  public async stop(id: number): Promise<boolean> {
    const result = await this.http.get<any>(`${environment.ip}/workflow_stop/${id}`).toPromise();
    if (result['error']) {
      this.bar.open(result['error'], 'CLOSE', { duration: 5000 });
      return false;
    } else {
      return true;
    }
  }
}
