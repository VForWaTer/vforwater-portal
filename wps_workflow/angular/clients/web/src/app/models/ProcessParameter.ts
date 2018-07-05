/**
 * The type of the process parameter
 * which according to the ogc wps
 * accepts literals, complex data
 * and bounding box data
 *
 * @export
 * @enum {number}
 */
export enum ProcessParameterType {
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
export interface ProcessParameter<T extends 'input' | 'output'> {
    id: number;
    role: T;
    type: ProcessParameterType;
    title: string;
    abstract: string;
    format: string;
    min_occurs: number;
    max_occurs: number;
}
