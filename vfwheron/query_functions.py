import re

from django.db import connections

from vfwheron.models import TblVariable


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

def get_second_level():
    vBodGeo = 0
    vBodTyp = 0
    vBesIns = 0
    vBesNam = 0
    vBesDep = 0
    vDomPrj = 0
    vDomDom = 0
    vStaNam = 0
    vDatNam = 0
    # second_level = [{'Boden': ['Geologie', 'Bodentyp']}, {'Besitzer': ['Institution Name', 'Nachname', 'Department']},
    #     {'Domäne': ['Projekt', 'Name der Domäne']}, {'Standort': ['Standort Name']},{'Datentyp': ['Name der Variable']}]
    #second_level = [{'Boden': [{'Geologie':vBodGeo}, {'Bodentyp':vBodTyp}]}, {'Besitzer': [{'Institution Name':vBesIns},
    #    {'Nachname':vBesNam},{'Department':vBesDep}]}]
    second_level = [{'Boden': [{'Geologie':vBodGeo}, {'Bodentyp':vBodTyp}]}, {'Besitzer': [{'Institutsname':vBesIns},
        {'Nachname':vBesNam},{'Department':vBesDep}]},{'Domäne': [{'Projekt':vDomPrj},{'Domänenname':vDomDom}]},
        {'Standort': [{'Standortname':vStaNam}]},{'Datentyp': [{'Variablenname':vDatNam}]}]
    return second_level

def get_menu_names():
    menu_names = {'Boden':'Geologie', 'Boden':'Bodentyp', 'publisher__institution_name':'Institution Name', 
        'publisher__last_name':'Nachname', 'publisher__department':'Department',
       'nmmetadomain__domain__project__project_name':'Projekt', 'site__site_name':'Standort Name', 
       'variable__variable_name':'Name der Variable', 'nmmetadomain__domain__domain_name':'Name der Domäne'}
    return menu_names
    
class menu_titles(object):
    def __init__(self, first_level, first_level_link, second_level, second_level_link):
        self.first_level = first_level
        self.first_level_link = first_level_link
        self.second_level = second_level
        self.second_level_link = second_level_link

    # first_level = ''
    # first_level_link = ''
    # second_level = ''
    # second_level_link = ''

