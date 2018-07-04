/**
 * Connect two tasks with each other, the end points
 * are fixed to a specific input/output.
 *
 * @export
 * @interface Edge
 */
export interface Edge {
    id: number;
    from_task_id: number;
    to_task_id: number;
    input_id: number;
    output_id: number;
}
