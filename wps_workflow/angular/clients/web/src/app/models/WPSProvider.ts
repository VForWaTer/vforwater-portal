/**
 * The provider contains the most
 * important information about the
 * wps server which is the url
 *
 * @export
 * @interface WPSProvider
 */
export interface WPSProvider
{
    /**
     * ID of this object
     */
    id: number;
    /**
     * Describing title of the Provider
     */
    title: string;
    /**
     * Homepage of the provider
     */
    site: string;
}
