import decimal
import json
import os.path

from builtins import all
from django.db.models import Max, Min
from django.db.models.functions import datetime
from django.utils.datetime_safe import strftime

from vfwheron.models import TblMeta, TblVariable, LtDomain, LtLicense, LtSite, LtSoil, LtUser, TblSensor, NmMetaDomain
from django.contrib.gis.db import models


class newFiltermenu():
    menu_tables = [LtDomain, LtLicense, LtSite, LtSoil, LtUser, TblMeta, TblSensor, TblVariable]
    json_menu = {}

    def build_menu(LANG='DE'):
        print(LtDomain.menu_name)
        print(LtDomain.newmenu_name['DE'])
        menu_dict = {tables.newmenu_name[LANG]: tables for tables in newFiltermenu.menu_tables}
        childs = []
        for menu in newFiltermenu.menu_tables:  # Loop through all tables, i.e. LtSoil,...


            try:
                menu.filter_type
            except AttributeError:
                filter_type = {}
            else:
                filter_type = menu.filter_type

            if menu == LtDomain:  # LtDomain is a seperate table that needs special treatment
                # TODO: That might be a case for the model.manager
                print('Something special for LtDomain')
                # query = eval("NmMetaDomain.objects.filter(" + query_path + "='"+name+"').count()")

            # elif menu == TblMeta:
            #     print('Überleg Dir was für TblMeta!')  # TODO

            else:
                for key, value in menu.newcolumn_dict.items():  # key: license_abb,comercial,geology, value:Geologie ...
                    grandchilds = []
                    selectables = 0
                    key_type = filter_type[key] if key in filter_type else False
                    print('specialmenu: ', key_type)
                    countgrandchilds = 0
                    print('key, value: ', key, value[LANG])
                    # get available values from database tables:
                    query_set = menu.objects.select_related().values_list(key,
                                                                          flat=True).distinct()  # marls, schist, ...
                    innerchild = {}

                    # remove empty columns and columns with None values only; keep rows with None if column has values too
                    if query_set is not [None] and ((len(query_set) == 1 and query_set[0] is not None) or (len(query_set) > 1)):
                        # print(' * * * * key: ', key, type(key))
                        # print(' * * * * menu.newpath: ', menu.newpath, type(menu.newpath))
                        query_path = key if menu.newpath is '' else menu.newpath + '__' + key
                        # print(' * * * * query_path: ', query_path)

                        if key_type == 'slider' or key_type == 'date':
                            print('yes, I am special')
                            # menu.objects.aggregate(min_value=Min('query_path'), max_value=Max('query_path'))
                            print('menu, query_path ', query_path)
                            # print("TblMeta.objects.filter(" + menu.newpath + "='" + key + "').count()")
                            count = menu.objects.select_related().values_list(key,
                                                                          flat=True).distinct().count()
                            # TblMeta.objects.select_related().values_list(si)
                            # menu.objects.exclude(query_path='NaN').aggregate(min_value=Min('books__price'), max_value=Max('books__price'))
                            if key_type == 'slider':
                                min_max = eval("TblMeta.objects.exclude(" + query_path + "='NaN').aggregate(min_value=Min('" + query_path + "'), max_value=Max('" + query_path + "'))")
                            else:
                                min_max = eval("TblMeta.objects.aggregate(min_value=Min('" + query_path + "'), max_value=Max('" + query_path + "'))")

                            selectables = selectables + 1 if count > 1 else selectables
                            innergrandchild = {'name': str(name),
                                               'type': key_type,
                                               'count': count,
                                               'isselected_min': False,
                                               'isselected_max': False,
                                               'selectable_min': str(min_max['min_value']),
                                               'selectable_max': str(min_max['max_value']),
                                               'selectable': True if count > 0 else False}
                            countgrandchilds = countgrandchilds + 1
                            grandchilds.append(innergrandchild)

                        else:
                            for name in query_set:  # marls, schist, ...
                                if name is not None:
                                    print('# # # name: ', name)
                                    # print("TblMeta.objects.filter(" + query_path + "='" + str(name) + "').count()")
                                    count = eval("TblMeta.objects.filter(" + query_path + "='" + str(name) + "').count()")
                                    # print('# # # # # #: ', count)
                                    selectables = selectables + 1 if count > 1 else selectables
                                    if count >= 0:  # TODO: change here if you don't want to have values with count=0 in menu
                                        innergrandchild = {'name': str(name),
                                                           'count': count,
                                                           'isselected': False,
                                                           'selectable': True if count > 0 else False}
                                        countgrandchilds = countgrandchilds + 1
                                        grandchilds.append(innergrandchild)
                            # print('grandchilds: ', grandchilds)
                    innerchild = {'name': value[LANG],
                                  'count': countgrandchilds,
                                  'isselected': False,
                                  'selectables': selectables}
                    if selectables >= 0:
                        innerchild = {**innerchild, **{'grandchilds': grandchilds}}
                    childs.append(innerchild)

                # print('childs: ', json.dumps(childs))
                save_path = '/home/marcus/git/vforwater-portal/vfwheron/test.json'
                file = open(save_path, "w")
                file.write(json.dumps(childs))
                file.close()
                print('+  * +*+ filter_type: ',filter_type)
        return 0


# TODO: There is no need to have this as models.Manager (Didn't use it). Find a better place for class
class FilterMenu(models.Manager):
    print('here')
    newFiltermenu.build_menu()
    print(LtDomain.objects.select_related().values_list('domain_name', flat=True).distinct().count())
    # print(NmMetaDomain.objects.filter(meta__variable__variable_name = 'Lufttemperatur'))
    print(TblMeta.objects.filter(nmmetadomain__domain__domain_name='x'))
    # print(TblMeta.objects.filter(sp))
    # print(TblMeta.objects.filter('NmMetaDomain__LtDomain__domain_name'))

    # Define here which tables to use; which columns are used is defined in the respective table
    menu_tables = [LtDomain, LtLicense, LtSite, LtSoil, LtUser, TblMeta, TblSensor, TblVariable]
    menu_dict = {tables.menu_name: tables for tables in menu_tables}

    def get_menu(detail_of_menu):
        general_struct = []

        for menu in FilterMenu.menu_tables:  # LtSoil,...
            sub_struct = {}
            for key, value in menu.column_dict.items():  # key: geology value: Geologie ...
                query_set = menu.objects.select_related().values_list(key, flat=True).distinct()  # marls, schist, ...
                if len(query_set) >= 1 and query_set[0] is not None:
                    # TODO: some query_sets give numbers --> other menu (from ... to ... instead of tick selection)
                    if detail_of_menu == 'submenu':
                        sub_struct.update({value: {'No Values': 0}})
                    elif detail_of_menu == 'complete_menu':
                        sub_struct.update({value: {str(key): False for key in query_set}})
            if sub_struct:
                general_struct.append({menu.menu_name: sub_struct})
        # print ('menu to send: ', general_struct)
        return general_struct

    # TODO: Can this be integrated in get_menu ? Might become confusing...
    # TODO: check if FilterMenu.menu_dict can be used to eliminate a loop or if
    def tick_submenu(top_menu_value, selection, cache_obj):
        submenu = {}

        for menu_dict in FilterMenu.get_menu('complete_menu'):  # complete menu in function object
            for key_1, value_1 in menu_dict.items():  # all top_level names (key_1 = Boden, Besitzer...)
                if key_1 == top_menu_value:  # check which menu has been clicked / Boden, Besitzer...
                    for key_2 in menu_dict[key_1]:  # all sub_level_names (key_2 = Geologie, Bodentyp...)
                        submenu[key_2] = dict(menu_dict[key_1][key_2])  # all values to choose from / Boolean if chosen
                        # set checked keys as True:
                        counts = FilterMenu.count_query(cache_obj, key_1, key_2, submenu[key_2].items())
                        for add_numbers, org_value in menu_dict[key_1][key_2].items():
                            submenu[key_2].update({add_numbers: [org_value, counts[add_numbers][0]]})
                        if selection:
                            for tick_key, tick_value in submenu[key_2].items():  # marls [True 651]
                                if tick_key in selection:
                                    submenu[key_2][tick_key][0] = True

        return submenu

    def count_query(cache_obj, active_m_key=False, active_key=False,
                    submenu_key=False):  # ,  active_value=False):  # Boden Geologie Sandstone
        # def build_sub_query(cache_obj, active_m_key=False, active_key=False, active_value=False): # Boden Geologie Sandstone
        m_map = {}
        paths = {}
        dataset_count = {}
        for menu in FilterMenu.menu_tables:
            m_map.update({menu.menu_name: {value: key for key, value in menu.column_dict.items()}})
            paths.update({value: key for key, value in menu.column_dict.items()})

        for values_3 in submenu_key:
            filter_list = django_data = ''
            if active_m_key and active_key:  # and active_value:
                active_filter_aswellas = FilterMenu.menu_dict[active_m_key].path + "__" + m_map[active_m_key][
                    active_key]  # meta__soil__geology
                filter_list = ".filter(" + active_filter_aswellas + "='" + values_3[0] + "')"

            for m_key in FilterMenu.menu_tables:
                # print('FilterMenu.menu_tables: ', FilterMenu.menu_tables)
                if m_key.menu_name in cache_obj and m_key.menu_name is not active_m_key:
                    for cache_key, cache_value in cache_obj.get(m_key.menu_name).items():  # e.g. Geologie: Sandstone
                        filter_aswellas = m_key.path + "__" + m_map[m_key.menu_name][
                            cache_key]  # e.g. soil +__+ geology
                        for value in cache_value:
                            filter_list = filter_list + ".filter(" + filter_aswellas + "='" + value + "')"

            django_data = eval("NmMetaDomain.objects" + filter_list + ".values('meta_id')")
            locations = django_data.values('meta__site__id').distinct()
            # bla = TblMeta.objects.filter(id=django_data)
            # print('django_data: ', bla)
            # selected_coords = (django_data.objects.filter(meta_id__geometry = LtLocation).distinct())
            # print('len: ', len(selected_coords))
            dataset_count.update({values_3[0]: [len(django_data), django_data]})
        # print('{values_3[0]: django_data}: ', {values_3[0]: [len(django_data), django_data]})
        return dataset_count

    def build_queryset(cache_obj):
        m_map = {}
        for menu in FilterMenu.menu_tables:
            m_map.update({menu.menu_name: {value: key for key, value in menu.column_dict.items()}})

        filter_list = django_data = ''
        for m_key in FilterMenu.menu_tables:
            if m_key.menu_name in cache_obj:
                for cache_key, cache_value in cache_obj.get(m_key.menu_name).items():  # e.g. Geologie: Sandstone
                    filter_aswellas = m_key.path + "__" + m_map[m_key.menu_name][cache_key]  # e.g. soil +__+ geology
                    for value in cache_value:
                        filter_list = filter_list + ".filter(" + filter_aswellas + "='" + value + "')"
                django_data = eval("NmMetaDomain.objects" + filter_list + ".values('meta_id')")
        # print(' + + + ++ ++ :  ', LtDomain.objects.filter(pid = None).all())

        return django_data
