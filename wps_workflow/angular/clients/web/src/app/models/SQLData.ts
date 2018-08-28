/**
 * Model for dragged and dropped Data Element from Datastore
 *
 * @export
 * @interface SQLData
 */
export interface SQLData
{
    /**
     * ID of this object
     */
    id: number;
    /**
     * Describing title of the selected dataset
     */
    title: string;
    /**
     * X-Coordinate within the editor
     */
    x: number;
    /**
     * Y-Coordinate within the editor
     */
    y: number;
    /**
     * Data held in this object. Data is always a number being an ID within a database which is resolved in a SQL query
     */
    data: number;
}

