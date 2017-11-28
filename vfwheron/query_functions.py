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


def build_point_sld(ids):
    url = "http://vforwater-gis.scc.kit.edu:8080/geoserver/rest/workspaces/CAOS/styles/selection"
    # url = "http://vforwater-gis.scc.kit.edu:8080/geoserver/rest/styles/new_point2"
    content = 'content-type'
    application = 'application / vnd.ogc.sld + xml'
    with open(os.path.join(os.path.join(os.path.expanduser('~'), '.vforwater'), 'secret_geoserver.txt')) as f:
        secret = f.read().strip()

    print('1')
    chosen_ids = ''
    for h in ids:
        for i in h.values():
            chosen_ids = chosen_ids+'<ogc:PropertyIsEqualTo><ogc:PropertyName>id</ogc:PropertyName>' \
                                    '<ogc:Literal>' + str(i) + '</ogc:Literal></ogc:PropertyIsEqualTo>'

    choice = '<Rule><Name>ChosenData</Name><Title>Chosen Datasets</Title><ogc:Filter><ogc:Or>' + chosen_ids + \
             '</ogc:Or> </ogc:Filter><PointSymbolizer><Graphic><Mark><WellKnownName>circle' \
             '</WellKnownName><Fill><CssParameter name="fill">#0033CC</CssParameter></Fill></Mark><Size>16</Size>' \
             '</Graphic></PointSymbolizer></Rule>'

    data = '<?xml version="1.0" encoding="ISO-8859-1"?><StyledLayerDescriptor version="1.0.0" ' \
           'xsi:schemaLocation="http://www.opengis.net/sld StyledLayerDescriptor.xsd" ' \
           'xmlns="http://www.opengis.net/sld" xmlns:ogc="http://www.opengis.net/ogc" ' \
           'xmlns:xlink="http://www.w3.org/1999/xlink" ' \
           'xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"><NamedLayer><Name>Attribute-based ' \
           'point</Name><UserStyle><Title>Attribute-based ' \
           'point</Title><FeatureTypeStyle><Rule><Name>AllData</Name><Title>All avaiable ' \
           'Datensets</Title><PointSymbolizer><Graphic><Mark><WellKnownName>circle</WellKnownName><Fill><CssParameter ' \
           'name="fill">#00DDFF</CssParameter></Fill></Mark><Size>3</Size></Graphic></PointSymbolizer></Rule>' + \
           choice + '</FeatureTypeStyle></UserStyle>  </NamedLayer></StyledLayerDescriptor>'
    # s = requests.put("http://vforwater-gis.scc.kit.edu:8080/geoserver/rest/workspaces/CAOS/styles/chosen_point", data=data,
    #                  auth=(secret), headers={'content-type': 'application/vnd.ogc.sld+xml'})
    s = eval("requests.put('"+url+"', data='"+data+"', auth=("+secret+"), headers={'"+content+"': '"+application+"'})")

    print('send request: ', s.content, s.status_code)
    return 0


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
