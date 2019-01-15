import {WPSProvider} from 'app/models/WPSProvider';

/**
 * Wps contains data about a wps server
 *
 * @export
 * @interface WPS
 */
export interface WPS
{
    /**
     * ID of this object
     */
    id: number;
    /**
     * Provider who operates this server
     */
    provider: WPSProvider;
    /**
     * Describing title of the server
     */
    title: string;
    /**
     * Explaning and abstract text of the process
     */
    abstract: string;
}
