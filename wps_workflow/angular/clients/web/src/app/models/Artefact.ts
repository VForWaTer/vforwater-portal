/**
 * Describes the structure of input/output which
 * is used for tasks and also contains the data.
 *
 * @export
 * @interface Artefact
 * @template T
 */
export interface Artefact<T> {
    parameter_id: number;
    task_id: number;
    workflow_id: number;
    role: T;
    format: string;
    data: string;
    created_at: number;
    updated_at: number;
}
