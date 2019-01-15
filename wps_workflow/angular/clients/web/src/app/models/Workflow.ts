import {SQLData} from 'app/models/SQLData';
import {Edge} from 'app/models/Edge';
import {Task} from 'app/models/Task';
import {DataEdge} from 'app/models/DataEdge';

/**
 * A workflow contains all related
 * edges and tasks.
 *
 * @export
 * @interface Workflow
 */
export interface Workflow
{
    /**
     * ID of this object
     */
    id: number;
    /**
     * Describing title of the workflow
     */
    title: string;
    /**
     * List of Edges between Tasks
     */
    edges: Edge[];
    /**
     * List of Tasks in workflow
     */
    tasks: Task[];
    /**
     * List of Datasets in workflow
     */
    datas: SQLData[];
    /**
     * List of Edges between Datasets and Tasks in workflow
     */
    dataEdges: DataEdge[];
    /**
     * ID of the workflow creator user
     */
    creator_id: number;
    /**
     * Bool value if this workflow is shared with other users
     */
    shared: boolean;
    /**
     * Number value from 0 to 100 showing the execution progress of the whole workflow
     */
    percent_done: number;
    /**
     * Timestamp of when this object was created
     */
    created_at: number;
    /**
     * Timestamp of when this object was last updated or alteredv
     */
    updated_at: number;
}
