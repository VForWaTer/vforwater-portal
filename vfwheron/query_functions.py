# TODO @Marcus: this file should work as manager in models.py

import re
import os
import requests
from django.db import connections
from django.core.serializers import serialize

from vfwheron.models import LtLocation
from time import time

def get_bbox_from_data(): # get bbox for available data
    try:
        cursor = connections['vforwater'].cursor() # connect to database
        # request bbox in srid of openlayers:
        cursor.execute('SELECT ST_Extent(ST_Transform(ST_SetSRID(ST_Point(ST_X(geom), ST_Y(geom)),srid),3857)) FROM lt_location;')
        m = re.findall("(\d+.\d*)", cursor.fetchall()[0][0]) # get string with coordinates
        cursor.close()
    except:
        m = ['645336.034469495', '6395474.75106861', '666358.204722283', '6416613.20733359']
    return list(map(lambda x: float(x), m)) # change string to list of floats


def get_sample_locations():
    sample_location = LtLocation.objects.select_related().values_list('geom').distinct()
    a = LtLocation.objects.select_related().all()
    # a = Basiseinzugsgebiet.objects.select_related().all()
    sample_location = serialize('geojson', a, fields=('srid', 'geometry_type', 'centroid_x', 'centroid_y',))
#     cursor = connections["vforwater"].cursor() # connect to database
#     cursor.execute("SELECT ST_AsGeoJSON(ST_Transform(ST_SetSRID(ST_Point(centroid_x, centroid_y),srid),3857))::json FROM lt_location;")
#     locations = cursor.fetchall()
#
#     # print(locations)
#     # TODO: serialize kann gültiges json erstellen. --> model anpassen
#     # a=serialize('geojson', cursor.fetchall(),
#     #           geometry_field='point',
#     #           fields=('name',))
#     cursor.close()
#     # print(a)
#     print(LtLocation.objects.select_related().values_list('geom').distinct())
    return sample_location


def dictfetchall(cursor):
    "Return all rows from a cursor as a dict"
    columns = [col[0] for col in cursor.description]
    return [
        dict(zip(columns, row))
        for row in cursor.fetchall()
    ]
