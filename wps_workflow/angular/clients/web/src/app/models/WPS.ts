import { WPSProvider } from 'app/models/WPSProvider';

/**
 * Wps contains data about a wps server
 *
 * @export
 * @interface WPS
 */
export interface WPS {
    id: number;
    provider: WPSProvider;
    title: string;
    abstract: string;
}
