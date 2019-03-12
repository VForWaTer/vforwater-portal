/**
 * Describes the structure of input/output which
 * is used for tasks and also contains the data.
 *
 * @export
 * @interface Artefact
 * @template T
 */
export interface Artefact<T>
{
    /**
     *  ID of the parameter to this Artefact
     */
    parameter_id: number;
    /**
     * ID of the task holding this Artefact
     */
    task_id: number;
    /**
     * ID of the workflow containing this Artefact
     */
    workflow_id: number;
    /**
     * Role of this Artefact, can be input or output
     */
    role: T;
    /**
     * Format of the stored data, e.g. plain, string, number
     */
    format: string;
    /**
     *  The stored data itself formatted as string.
     */
    data: string;
    /**
     * Timestamp of when this object was created
     */
    created_at: number;
    /**
     * Timestamp of when this object was last updated or altered
     */
    updated_at: number;
}
