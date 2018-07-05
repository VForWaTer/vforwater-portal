import { ProcessParameter } from 'app/models/ProcessParameter';

/**
 * Processes are the actual wps processes which are provided
 * by the wps servers.
 *
 * @export
 * @interface Process
 */
export interface Process {
    id: number;
    title: string;
    abstract: string;
    identifier: string;
    inputs: ProcessParameter<'input'>[];
    outputs: ProcessParameter<'output'>[];
    wps_id: number;
    created_at: number;
    updated_at: number;
}
