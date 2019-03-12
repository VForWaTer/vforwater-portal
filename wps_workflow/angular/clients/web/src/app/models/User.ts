/**
 * Logged in user.
 *
 * @export
 * @interface User
 */
export interface User
{
    /**
     * ID of the object
     */
    id: number;
    /**
     * Unique name of the user
     */
    username: string;
    /**
     * Bool value if this user has staff privileges. Staff members can log in to the django admin page
     */
    is_staff: boolean;
    /**
     * Bool value if this user has admin privileges. Admin members can log in to the django admin page and alter DB entries
     */
    is_admin: boolean;
}
