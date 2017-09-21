import re

from django.db import connections
from django.core.serializers import serialize

from vfwheron.models import TblVariable, LtSite, LtSoil, TblMeta, LtDomain, LtLocation


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
    sample_location = serialize('geojson', a, fields=('srid','geometry_type','centroid_x','centroid_y',))
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

def default_menu_dict():
    v_bod_geo = LtSoil.objects.select_related().values_list('geology').distinct()
    v_bod_typ = LtSoil.objects.select_related().values_list('soil_type').distinct()
    v_besitz_ins = TblMeta.objects.select_related().values_list('creator__institution_name').distinct()
    v_besitz_nam = TblMeta.objects.select_related().values_list('creator__last_name').distinct()
    v_besitz_dep = TblMeta.objects.select_related().values_list('creator__department').distinct()
    v_dom_prj = LtDomain.objects.select_related().values_list('project__project_name').distinct()
    v_dom_dom = LtDomain.objects.select_related().values_list('domain_name').distinct()
    v_stand_nam = LtSite.objects.select_related().values_list('site_name').distinct()
    v_dat_nam = TblVariable.objects.select_related().values_list('variable_name', 'variable_symbol').distinct()
    menu_dict = [{'Boden': {'Geologie':v_bod_geo, 'Bodentyp':v_bod_typ}, 'Besitzer': {'Institutsname':v_besitz_ins,
        'Nachname':v_besitz_nam,'Department':v_besitz_dep}, 'Domäne': {'Projekt':v_dom_prj,'Domänenname':v_dom_dom},
        'Standort': {'Standortname':v_stand_nam}, 'Datentyp': {'Variablenname':v_dat_nam}}]
    return menu_dict

def get_submenu():
    # set startvalues
    v_bod_geo = v_bod_typ = v_besitz_ins = v_besitz_nam = v_besitz_dep = v_dom_prj = v_dom_dom = v_stand_nam = v_dat_nam = {'No Values': 0}

    submenu = [{'Boden': {'Geologie':v_bod_geo, 'Bodentyp':v_bod_typ}, 'Besitzer': {'Institutsname':v_besitz_ins,
        'Nachname':v_besitz_nam,'Department':v_besitz_dep}, 'Domäne': {'Projekt':v_dom_prj,'Domänenname':v_dom_dom},
        'Standort': {'Standortname':v_stand_nam}, 'Datentyp': {'Variablenname':v_dat_nam}}]
    return submenu

def get_submenu_values(top_menu_value):
    sub_menu_list = {}

    for top_level_dict in default_menu_dict():
        for top_key in top_level_dict:
            if top_key == top_menu_value:
                for sub_key in top_level_dict[top_key]:
                    sub_menu_list[sub_key] = list(top_level_dict[top_key][sub_key])
    return sub_menu_list

#
# class menu_map(object):
#     def __init__(self, top_level, sub_level, sub_level_value):
#         self.top_level = top_level
#         self.sub_level = sub_level
#         self.sub_level_value = sub_level_value
