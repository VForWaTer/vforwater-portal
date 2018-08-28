/**
 * Connect SQLData and Task with each other, the end points
 * are fixed to a specific input/output.
 * DataEdges always come from SQLData objects and lead to an input of a Task
 *
 * @export
 * @interface DataEdge
 */
export interface DataEdge
{
    /**
     * ID of this object
     */
    id: number;
    /**
     * The ID of the SQLData object this edge comes from
     */
    from_sqldata_id: number;
    /**
     * The ID of the Task this edge leads to
     */
    to_task_id: number;
    /**
     * The ID of the input artefact of the target Task
     */
    task_input_id: number;
}
