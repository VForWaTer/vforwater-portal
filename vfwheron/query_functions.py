# TODO @Marcus: this file should work as manager in models.py
"""

"""
import re
from django.db import connections
import logging

logger = logging.getLogger(__name__)


def get_bbox_from_data(selected_ids=None):  # get bbox for available data
    """

    :param selected_ids:
    :type selected_ids:
    :return:
    :rtype:
    """
    try:
        cursor = connections['default'].cursor()  # connect to database
        if selected_ids:
            cursor.execute(
                # 'SELECT ST_Extent(ST_Transform(location, 3857)) '
                'SELECT ST_Extent(location) '
                'FROM entries WHERE entries.id in ({});'.format(selected_ids)
            )
        else:
            # request bbox in srid of openlayers:
            cursor.execute(
                # 'SELECT ST_Extent(ST_Transform(location, 3857)) '
                'SELECT ST_Extent(location) '
                'FROM entries;'
            )
        i = cursor.fetchall()[0][0]
        cursor.close()
        m = re.findall("(\d+.\d*)", i)  # get string with coordinates
    except TypeError as ex:
        print('\033[91m Exeption in loading bbox: {}\033[0m'.format(ex))
        logger.warning('\033[91m Data Extend cannot be loaded in query_functions.py. Using fixed values.\033[0m')
        # m = ['5798222.6196955', '1257192.40494065', '5798286.18312474', '1257331.99671517']
        m = ['11.221124', '52.08632', '11.222354', '52.086891']

    return list(map(lambda x: float(x), m))  # change string to list of floats
#
# def dictfetchall(cursor):
#     "Return all rows from a cursor as a dict"
#     columns = [col[0] for col in cursor.description]
#     return [
#         dict(zip(columns, row))
#         for row in cursor.fetchall()
#     ]
