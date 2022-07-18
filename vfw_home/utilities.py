from django.utils import translation, timezone


# TODO: added embargo end in def get_accessible_data query. Check if the following function is still needed.
from vfw_home.models import Entries


def has_pending_embargo(embargo, embargo_end):
    """
    Send the information if there is an embargo and end date to check if embargo is still valid.
    Careful: Uses a naive local timezone.
    :param embargo: boolean
    :type embargo: boolean
    :param embargo_end: date
    :type embargo_end: datetime
    :return: boolean
    """
    pending = True
    if embargo is False or (embargo is True and timezone.make_naive(timezone.now()) > embargo_end):
        pending = False

    return pending


def human_readable_bool(bool_val):
    """
    Translate the boolean value to yes or no in the language of the user
    :param bool_val: bool
    :return: string
    """
    yesno = translation.gettext('No')
    if bool_val:
        yesno = translation.gettext('Yes')

    return yesno


def verbose_expiry_info(embargo, embargo_end):
    """
    Send the information if there is an embargo and end date to check if embargo is still valid.
    Careful: Uses a naive local timezone.
    :param embargo: boolean
    :type embargo: boolean
    :param embargo_end: date
    :type embargo_end: datetime
    :return: boolean
    :param embargo:
    :param embargo_end:
    :return: string
    """
    has_embargo = translation.gettext('Pending')
    if embargo is True and timezone.make_naive(timezone.now()) > embargo_end:
        has_embargo = translation.gettext('Expired')

    return has_embargo


def entry_has_data(entry: int) -> bool:
    """
    Check if Entries object has a datasource and consequently actual data.
    :param entry: entry id as integer
    :return: boolean
    """
    data = Entries.objects.values('datasource').filter(id=entry)
    if data[0]['datasource'] is not None:
        return True
    else:
        return False
