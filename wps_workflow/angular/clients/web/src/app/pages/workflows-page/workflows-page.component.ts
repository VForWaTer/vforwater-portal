import { Component, OnInit } from '@angular/core';
import { WorkflowService, WorkflowValidationResult } from 'app/services/workflow.service';
import { Workflow } from 'app/models/Workflow';
import { Observable } from 'rxjs/Observable';
import { Router } from '@angular/router';
import { ProcessService } from 'app/services/process.service';
import { Process } from 'app/models/Process';
import { take } from 'rxjs/operators/take';
import { delay } from 'rxjs/operators/delay';

/**
 * Workflow list page.
 *
 * @export
 * @class WorkflowsPageComponent
 * @implements {OnInit}
 */
@Component({
  selector: 'app-workflows-page',
  templateUrl: './workflows-page.component.html',
  styleUrls: ['./workflows-page.component.scss']
})
export class WorkflowsPageComponent implements OnInit {

  public workflows: Workflow[];
  public processes: Process[];

  public openedWorkflowID = -1;
  private running = [];

  /**
   * Creates an instance of WorkflowsPageComponent.
   *
   * @param {ProcessService} processService
   * @param {WorkflowService} workflowService
   * @param {Router} router
   * @memberof WorkflowsPageComponent
   */
  constructor(
    private processService: ProcessService,
    private workflowService: WorkflowService,
    private router: Router,
  ) {

  }

  /**
   * Component setup.
   *
   * @memberof WorkflowsPageComponent
   */
  public ngOnInit() {
    this.workflowService.all().subscribe(workflows => this.workflows = workflows);
    this.processService.all().subscribe(processes => this.processes = processes);
  }

  /**
   * Checks whether a workflow is opened.
   *
   * @param workflow the workflow which is checked
   */
  public opened(workflow: Workflow) {
    this.openedWorkflowID = workflow.id;
  }

  /**
   * Checks whether a workflow is closed.
   *
   * @param workflow the workflow which is checked
   */
  public closed(workflow: Workflow) {
    if (this.openedWorkflowID === workflow.id) {
      this.openedWorkflowID = -1;
    }
  }

  /**
   * Removes a workflow.
   *
   * @param id Workflow id
   */
  public remove(id: number) {
    const index = this.workflows.findIndex(workflow => workflow.id === id);
    if (index !== -1) {
      this.workflows.splice(index, 1);
      this.workflowService.remove(id);
    }
  }

  /**
   * Routes to the editor opening a workflow.
   *
   * @param id Workflow id
   */
  public edit(id: number) {
    this.router.navigate([`/editor/${id}`]);
  }

  /**
   * Gets a workflow from the database.
   *
   * @param id Workflow id
   */
  public getWorkflow(id: number): Observable<Workflow> {
    return this.workflowService.get(id);
  }

  /**
   * Executes a workflow.
   *
   * @param id Workflow id
   */
  public run(id: number) {
    this.workflowService.start(id);
    this.running.push(id);
  }

  /**
   * Validates a given workflow.
   *
   * @param workflow Workflow object
   */
  public validate(workflow): boolean {
    return this.workflowService.validate(workflow) === WorkflowValidationResult.SUCCESSFUL;
  }

  /**
   * Checks if a workflow is running.
   *
   * @param worflow Workflow to check
   */
  public runs(workflow: Workflow): boolean {
    return this.workflowService.isRunning(workflow) || this.running.includes(workflow.id);
  }

  /**
   * Checks if a workflow is finished.
   *
   * @param worflow Workflow to check
   */
  public finished(workflow: Workflow): boolean {
    return this.workflowService.finished(workflow);
  }
}
