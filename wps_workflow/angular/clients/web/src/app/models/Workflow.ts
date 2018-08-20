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
    id: number;
    title: string;
    edges: Edge[];
    tasks: Task[];
    datas: SQLData[];
    dataEdges: DataEdge[];
    creator_id: number;
    shared: boolean;
    percent_done: number;
    created_at: number;
    updated_at: number;
}
