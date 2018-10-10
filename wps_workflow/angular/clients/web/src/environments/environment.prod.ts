/**
 * Setting for build Environment
 * The file contents for the current environment will overwrite these during build.
 * The build system defaults to the dev environment which uses `environment.ts`, but if you do
 * `ng build --env=prod` then `environment.prod.ts` will be used instead.
 * The list of which env maps to which file can be found in `.angular-cli.json`.
 * @type {{production: boolean; ip: string}}  return settings
 */
export const environment = {
    /**
     *  true if production build settings should be used
     *  false if dev build settings should be used
     */
    production: true,
    /**
     * The root address or IP of the Angular App. Router uses this as base address
     */
    ip: 'http://127.0.0.1:8000/wps_workflow',
};
