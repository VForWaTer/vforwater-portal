import re
from collections import defaultdict

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
    sample_location = serialize('geojson', a, fields=('srid', 'geometry_type', 'centroid_x','centroid_y',))
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



def default_menu_list():

    def build_dict(table, *column):
        num_flat = True # flat = True removes brackets around result of query - use False for a list of fields
        if len([*column]) > 1: num_flat = False
        my_query_set = table.objects.select_related().values_list(*column, flat=num_flat).distinct()
        return {key: False for key in my_query_set}

    # some unused values
    q_bod_poro = build_dict(LtSoil, 'porosity')
    q_bod_resmoi = build_dict(LtSoil, 'residual_moisture')
    q_bod_fielcap = build_dict(LtSoil, 'field_capacity')

    q_bod_geo = build_dict(LtSoil, 'geology')
    q_bod_typ = build_dict(LtSoil, 'soil_type')
    q_besitz_ins = build_dict(TblMeta, 'creator__institution_name')
    q_besitz_nam = build_dict(TblMeta, 'creator__last_name')
    q_besitz_dep = build_dict(TblMeta, 'creator__department')
    q_dom_prj = build_dict(LtDomain, 'project__project_name')
    q_dom_dom = build_dict(LtDomain, 'domain_name')
    q_stand_nam = build_dict(LtSite, 'site_name')
    q_dat_nam = build_dict(TblVariable, 'variable_name')#, TODO: 'variable_symbol') # kann Json nicht; muss EIN String werden

    boden_dict = {'Boden': {'Geologie': q_bod_geo, 'Bodentyp': q_bod_typ}}
    # boden_dict = {'Boden': {'Geologie': q_bod_geo, 'Bodentyp': q_bod_typ, 'Porosität': q_bod_poro,
    #                         'Residuale Feuchtigkeit': q_bod_resmoi, 'field capacity': q_bod_fielcap}}
    besitzer_dict = {'Besitzer': {'Institutsname':q_besitz_ins,'Nachname':q_besitz_nam,'Department':q_besitz_dep}}
    domain_dict = {'Domäne': {'Projekt':q_dom_prj,'Domänenname':q_dom_dom}}
    datentyp_dict = {'Datentyp': {'Variablenname':q_dat_nam}}
    standort_dict = {'Standort': {'Standortname':q_stand_nam}}

    # TODO: Check how often database is accessed just to build the menu_list!
    menu_list = [boden_dict, besitzer_dict, domain_dict, datentyp_dict, standort_dict]

    return menu_list

def get_submenu():
    # set startvalues
    q_bod_fielcap = q_bod_resmoi = q_bod_poro = q_bod_geo = q_bod_typ = q_besitz_ins = q_besitz_nam = q_besitz_dep = q_dom_prj = q_dom_dom = q_stand_nam = q_dat_nam = {'No Values': 0}

    submenu = [{'Boden': {'Geologie':q_bod_geo, 'Bodentyp':q_bod_typ}, 'Besitzer': {'Institutsname':q_besitz_ins,
        'Nachname':q_besitz_nam,'Department':q_besitz_dep}, 'Domäne': {'Projekt':q_dom_prj,'Domänenname':q_dom_dom},
        'Standort': {'Standortname':q_stand_nam}, 'Datentyp': {'Variablenname':q_dat_nam}}]
    # submenu = [{'Boden': {'Geologie':q_bod_geo, 'Bodentyp':q_bod_typ, 'Porosität':q_bod_poro,
    #     'Residuale Feuchtigkeit':q_bod_resmoi, 'field capacity': q_bod_fielcap}, 'Besitzer': {'Institutsname':q_besitz_ins,
    #     'Nachname':q_besitz_nam,'Department':q_besitz_dep}, 'Domäne': {'Projekt':q_dom_prj,'Domänenname':q_dom_dom},
    #     'Standort': {'Standortname':q_stand_nam}, 'Datentyp': {'Variablenname':q_dat_nam}}]
    return submenu

def get_submenu_values(top_menu_value, selection):
    sub_menu_dict = {}
    # print('default_menu_list(): ', default_menu_list())
    for top_level_dict in default_menu_list(): # complete top_level_dict in function object
        for top_key in top_level_dict: # all top_level names (top_key = Boden, Besitzer...)
            if top_key == top_menu_value: # check which menu has been clicked
                for sub_key in top_level_dict[top_key]: # all sub_level_names (sub_key = Geologie, Bodentyp...)
                    # print('top_level_dict: ', top_level_dict)
                    # print('top_key: ', top_key)               # (top_key = Boden, Besitzer...)
                    # print('sub_key: ', sub_key)               # (sub_key = Geologie, Bodentyp...)
                    sub_menu_dict[sub_key] = dict(top_level_dict[top_key][sub_key]) # all values to choose from and Boolea if chosen
# set checked keys as True:
                    if selection:
                        for get_key, get_value in sub_menu_dict[sub_key].items():
                            if get_key in selection:
                                sub_menu_dict[sub_key][get_key] = True;
    return sub_menu_dict

#
# class menu_map(object):
#     def __init__(self, top_level, sub_level, sub_level_value):
#         self.top_level = top_level
#         self.sub_level = sub_level
#         self.sub_level_value = sub_level_value
