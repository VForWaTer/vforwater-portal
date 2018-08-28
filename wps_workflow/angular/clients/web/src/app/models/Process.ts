import {ProcessParameter} from 'app/models/ProcessParameter';

/**
 * Processes are the actual wps processes which are provided
 * by the wps servers.
 *
 * @export
 * @interface Process
 */
export interface Process
{
    /**
     * ID of this object
     */
    id: number;
    /**
     * Describing title of the process
     */
    title: string;
    /**
     * Explaning and abstract text of the process
     */
    abstract: string;
    /**
     * Unique identifier of the process used by PyWPS
     */
    identifier: string;
    /**
     * List of input parameters
     */
    inputs: ProcessParameter<'input'>[];
    /**
     * List of output parameters
     */
    outputs: ProcessParameter<'output'>[];
    /**
     * ID of the PyWPS Server hosting this process
     */
    wps_id: number;
    /**
     * Timestamp of when this object was created
     */
    created_at: number;
    /**
     * Timestamp of when this object was last updated or altered
     */
    updated_at: number;
}
