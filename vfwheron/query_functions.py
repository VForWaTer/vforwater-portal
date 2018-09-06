# TODO @Marcus: this file should work as manager in models.py
"""

"""
import re
from django.db import connections


def get_bbox_from_data(selectedIds = None):  # get bbox for available data
    """

    :param selectedIds:
    :type selectedIds:
    :return:
    :rtype:
    """
    try:
        cursor = connections['vforwater'].cursor()  # connect to database
        if selectedIds:
            cursor.execute(
                    'SELECT ST_Extent(ST_Transform(ST_SetSRID(ST_Point(ST_X(geom), ST_Y(geom)),srid),3857)) FROM tbl_meta '
                    'LEFT JOIN lt_location ON tbl_meta.geometry_id = lt_location.id WHERE tbl_meta.id in (' + selectedIds + ');'
                    )
        else:
            # request bbox in srid of openlayers:
            cursor.execute(
                    'SELECT ST_Extent(ST_Transform(ST_SetSRID(ST_Point(ST_X(geom), ST_Y(geom)),srid),3857)) FROM lt_location;'
                    )
        m = re.findall("(\d+.\d*)", cursor.fetchall()[0][0])  # get string with coordinates
        cursor.close()
    except Exception as ex:
        m = ['645336.034469495', '6395474.75106861', '666358.204722283', '6416613.20733359']
    return list(map(lambda x: float(x), m))  # change string to list of floats


#
# def dictfetchall(cursor):
#     "Return all rows from a cursor as a dict"
#     columns = [col[0] for col in cursor.description]
#     return [
#         dict(zip(columns, row))
#         for row in cursor.fetchall()
#     ]
