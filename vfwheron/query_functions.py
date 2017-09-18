import re

from django.db import connections

from vfwheron.models import TblVariable, LtSite, LtSoil, LtLocation, LtProject, TblMeta, NmMetaDomain, LtDomain


def get_bbox_from_data(): # get bbox for available data
    cursor = connections['vforwater'].cursor() # connect to database
    # request bbox in srid of openlayers:
    cursor.execute('SELECT ST_Extent(ST_Transform(ST_SetSRID(ST_Point(centroid_x, centroid_y),srid),3857)) FROM lt_location;')
    m = re.findall("(\d+.\d*)", cursor.fetchall()[0][0]) # get string with coordinates
    return list(map(lambda x: float(x), m)) # change string to list of floats 

def get_filter_values():
    start_values = 0
    return start_values

def get_first_level():
    first_level =  {'variable':'Datentyp', 'soil':'Boden', 'site':'Standort','publisher':'Besitzer',
    'nmmetadomain':'Domäne'}
    return first_level

def get_submenu():
    # b[1].variable_name
    # print('****: ',list(b))
    v_bod_geo = {'No Values':0}
    v_bod_typ = {'No Values':0}
    v_besitz_ins = {'No Values':0}
    v_besitz_nam = {'No Values':0}
    v_besitz_dep = {'No Values':0}
    v_dom_prj = {'No Values':0}
    v_dom_dom = {'No Values':0}
    v_stand_nam = {'No Values':0}
    v_dat_nam = {'No Values':0}

    # second_level = [{'Boden': ['Geologie', 'Bodentyp']}, {'Besitzer': ['Institution Name', 'Nachname', 'Department']},
    #     {'Domäne': ['Projekt', 'Name der Domäne']}, {'Standort': ['Standort Name']},{'Datentyp': ['Name der Variable']}]
    #second_level = [{'Boden': [{'Geologie':vBodGeo}, {'Bodentyp':vBodTyp}]}, {'Besitzer': [{'Institution Name':vBesIns},
    #    {'Nachname':vBesNam},{'Department':vBesDep}]}]
    submenu = [{'Boden': [{'Geologie':v_bod_geo}, {'Bodentyp':v_bod_typ}]}, {'Besitzer': [{'Institutsname':v_besitz_ins},
        {'Nachname':v_besitz_nam},{'Department':v_besitz_dep}]},{'Domäne': [{'Projekt':v_dom_prj},{'Domänenname':v_dom_dom}]},
        {'Standort': [{'Standortname':v_stand_nam}]},{'Datentyp': [{'Variablenname':v_dat_nam}]}]
    return submenu

def default_menu_dict():
    # get_unit_id = TblVariable.objects.select_related('unit').values_list('variable_name', 'variable_symbol')
    # all_variable_names = get_unit_id.values('variable_name', 'variable_symbol', 'unit__unit_symbol')

    v_bod_geo = LtSoil.objects.select_related().values_list('geology').distinct()

    # v_loc_coord = LtLocation.objects.select_related('srid').all()
    # print(' + + + + +   NO !')
    # if not LtSite.objects.select_related().exists():
    v_bod_typ = LtSoil.objects.select_related().values_list('soil_type').distinct()
    v_besitz_ins = TblMeta.objects.select_related().values_list('creator__institution_name').distinct()
    v_besitz_nam = TblMeta.objects.select_related().values_list('creator__last_name').distinct()
    v_besitz_dep = TblMeta.objects.select_related().values_list('creator__department').distinct()
    v_dom_prj = LtDomain.objects.select_related().values_list('project__project_name').distinct()
    v_dom_dom = LtDomain.objects.select_related().values_list('domain_name').distinct()
    v_stand_nam = LtSite.objects.select_related().values_list('site_name').distinct()
    v_dat_nam = TblVariable.objects.select_related().values_list('variable_name', 'variable_symbol').distinct()
    # print('** ** **: ',list(v_dat_nam))
    menu_dict = [{'Boden': [{'Geologie':v_bod_geo}, {'Bodentyp':v_bod_typ}]}, {'Besitzer': [{'Institutsname':v_besitz_ins},
        {'Nachname':v_besitz_nam},{'Department':v_besitz_dep}]},{'Domäne': [{'Projekt':v_dom_prj},{'Domänenname':v_dom_dom}]},
        {'Standort': [{'Standortname':v_stand_nam}]},{'Datentyp': [{'Variablenname':v_dat_nam}]}]
    return menu_dict

def get_menu_names():
    menu_names = {'Boden':'Geologie', 'Boden':'Bodentyp', 'publisher__institution_name':'Institution Name', 
        'publisher__last_name':'Nachname', 'publisher__department':'Department',
       'nmmetadomain__domain__project__project_name':'Projekt', 'site__site_name':'Standort Name', 
       'variable__variable_name':'Name der Variable', 'nmmetadomain__domain__domain_name':'Name der Domäne'}
    return menu_names

def get_submenu_values(top_menu_value):
    sub_menu_list = {}
    for top_level_dict in default_menu_dict():
        # print('***, top_level_dict: ', top_level_dict)
        for top_level_key, top_level_values in top_level_dict.items():
            # print(top_level_key)
            # print(top_level_values)
            for sub_level in top_level_values:
                for sub_level_key, sub_level_values in sub_level.items():
                    # print(top_level_key)
                    # print(sub_level_key)
                    # print(list(sub_level_values))
                    if top_level_key == top_menu_value:
                        sub_menu_list[sub_level_key] = list(sub_level_values)
    print(sub_menu_list)
    return sub_menu_list
                    # print('2, m.values(): ', m.values())
        # for n in m.values():
            # print('3, n: ', n)
            # print('4, n[0]: ', n[0])
            # for o in n:
                # print ('5:', o.keys(), o.values())

        # top_level=

class menu_map(object):
    def __init__(self, top_level, sub_level, sub_level_value):
        self.top_level = top_level
        # self.top_level_link = top_level_link
        self.sub_level = sub_level
        self.sub_level_value = sub_level_value

    # first_level = ''
    # first_level_link = ''
    # second_level = ''
    # second_level_link = ''

