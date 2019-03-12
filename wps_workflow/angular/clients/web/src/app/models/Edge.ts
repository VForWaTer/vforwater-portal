/**
 * Connect two tasks with each other, the end points
 * are fixed to a specific input/output.
 *
 * @export
 * @interface Edge
 */
export interface Edge
{
    /**
     * ID of this object
     */
    id: number;
    /**
     * The ID of the Task object this edge comes from
     */
    from_task_id: number;
    /**
     * The ID of the Task this edge leads to
     */
    to_task_id: number;
    /**
     * The ID of the input artefact of the target Task
     */
    input_id: number;
    /**
     * The ID of the output artefact of the source Task
     */
    output_id: number;
}
