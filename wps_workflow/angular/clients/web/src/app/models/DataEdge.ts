/**
 * Connect SQLData and Task with each other, the end points
 * are fixed to a specific input/output.
 *
 * @export
 * @interface DataEdge
 */
export interface DataEdge
{
    id: number;
    from_sqldata_id: number;
    to_task_id: number;
    task_input_id: number;
}
