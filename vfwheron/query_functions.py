import re

from django.db import connections


def get_bbox_from_data():
    # get bbox for available data
    cursor = connections['vforwater'].cursor() # connect to database
    # request bbox in srid of openlayers
    cursor.execute('SELECT ST_Extent(ST_Transform(ST_SetSRID(ST_Point(centroid_x, centroid_y),srid),3857)) FROM lt_location;')
    m = re.findall("(\d+.\d*)", cursor.fetchall()[0][0]) # get string with coordinates
    dataExt = list(map(lambda x: float(x), m)) # change string to list of floats
    return dataExt

def get_filter_values():
    start_values = 0
    return start_values