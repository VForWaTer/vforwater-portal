import {Artefact} from 'app/models/Artefact';

/**
 * Describes the current state of a task.
 *
 * @export
 * @enum {number} TaskState state
 */
export enum TaskState
{
    /**
     * Task is not ready to be sheduled yet, workflow is still in edit
     */
    NONE,
    /**
     * Task is ready to be sheduled for execution
     */
    READY,
    /**
     * Task has been sheduled and sent to server, waits for execution by PyWPS Server
     */
    WAITING,
    /**
     * Task is being executed
     */
    RUNNING,
    /**
     * Task execution has been finished successfully, the results can be retrieved
     */
    FINISHED,
    /**
     * The execution has failed due to an error in the PyWPS Process, server availability or within the input data
     */
    FAILED,
    /**
     * The Process to this Task is no longer available on its PyWPS Server
     * The data will be kept for future reference or to restore workflows from a longer Server downtime (so Processes were not available)
     */
    DEPRECATED
}

/**
 * Tasks describe the actual task elements which are
 * displayed in the editor
 * with process_id, every task links to a process
 * which is executed if this task is run.
 *
 * @export
 * @interface Task
 */
export interface Task
{
    /**
     * ID of this object
     */
    id: number;
    /**
     * Describing Title of the Task
     */
    title: string;
    /**
     * X-Coordinate within the editor
     */
    x: number;
    /**
     * Y-Coordinate within the editor
     */
    y: number;
    /**
     * Current state of the Task, before, within or after execution
     */
    state: TaskState;
    /**
     * ID of the process this Task is an instance of.
     */
    process_id: number;
    /**
     * List of input artefacts
     */
    input_artefacts: Artefact<'input'>[];
    /**
     * List of output Artefacts
     */
    output_artefacts: Artefact<'output'>[];
    /**
     * Timestamp of when this object was created
     */
    created_at: number;
    /**
     * Timestamp of when this object was last updated or alteredv
     */
    updated_at: number;
}

