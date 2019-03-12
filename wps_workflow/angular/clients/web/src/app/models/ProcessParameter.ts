/**
 * The type of the process parameter
 * which according to the ogc wps
 * accepts literals, complex data
 * and bounding box data
 *
 * @export
 * @enum {number}
 */
export enum ProcessParameterType
{
    LITERAL,
    COMPLEX,
    BOUNDING_BOX
}

/**
 * Is referenced by artefact using the
 * parameter_id
 * Describes the input/output parameters
 * of processes
 *
 * @export
 * @interface ProcessParameter
 * @template T
 */
export interface ProcessParameter<T extends 'input' | 'output'>
{
    /**
     * ID of this object
     */
    id: number;
    /**
     * Role of this parameter, can be input or output
     */
    role: T;
    /**
     * Type of the parameter data, can be Literal, Complex or Bounding Box
     */
    type: ProcessParameterType;
    /**
     * Describing title of this parameter
     */
    title: string;
    /**
     * Explaning and abstract text of the process
     */
    abstract: string;
    /**
     * Format of the stored data, e.g. plain, string, number
     */
    format: string;
    /**
     * Minimal occurrence of the input (e.g. there can be more bands of raster file and they all can be passed as input using the same identifier)
     */
    min_occurs: number;
    /**
     * Maxium number of times, the input or output is present
     */
    max_occurs: number;
}
