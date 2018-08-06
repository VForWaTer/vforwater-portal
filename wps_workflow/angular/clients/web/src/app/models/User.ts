/**
 * Logged in user.
 *
 * @export
 * @interface User
 */
export interface User
{
    id: number;
    username: string;
    is_staff: boolean;
    is_admin: boolean;
}
