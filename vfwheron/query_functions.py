# TODO @Marcus: this file should work as manager in models.py

import re
import os
import requests
from django.db import connections
from django.core.serializers import serialize

from vfwheron.models import LtLocation


def get_bbox_from_data(): # get bbox for available data
    cursor = connections['vforwater'].cursor() # connect to database
    # request bbox in srid of openlayers:
    cursor.execute('SELECT ST_Extent(ST_Transform(ST_SetSRID(ST_Point(centroid_x, centroid_y),srid),3857)) FROM lt_location;')
    m = re.findall("(\d+.\d*)", cursor.fetchall()[0][0]) # get string with coordinates
    cursor.close()
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


def build_id_list(ids):
    id_list = []
    for h in ids:
        for i in h.values():
            id_list.append(i)
    return id_list


# def get_submenu_with_count(top_menu_value, selection, cache):
#     sub_menu_dict = {}
#     # print('complete_menu_list(): ', complete_menu_list())
#     complete_menu_list = FilterMenu.get_menu('complete_menu')
#     for top_level_dict in complete_menu_list: # complete top_level_dict in function object
#         for top_key in top_level_dict: # all top_level names (top_key = Boden, Besitzer...)
#             if top_key == top_menu_value: # check which menu has been clicked
#                 for sub_key in top_level_dict[top_key]: # all sub_level_names (sub_key = Geologie, Bodentyp...)
#                     # print('top_level_dict: ', top_level_dict)
#                     # print('top_key: ', top_key)               # (top_key = Boden, Besitzer...)
#                     # print('sub_key: ', sub_key)               # (sub_key = Geologie, Bodentyp...)
#                     sub_menu_dict[sub_key] = dict(top_level_dict[top_key][sub_key])  # all values to choose from / Boolean if chosen
#                     # set checked keys as True:
#                     if selection:
#                         for get_key, get_value in sub_menu_dict[sub_key].items():
#                             if get_key in selection:
#                                 sub_menu_dict[sub_key][get_key] = True;
#     return sub_menu_dict


def dictfetchall(cursor):
    "Return all rows from a cursor as a dict"
    columns = [col[0] for col in cursor.description]
    return [
        dict(zip(columns, row))
        for row in cursor.fetchall()
    ]
