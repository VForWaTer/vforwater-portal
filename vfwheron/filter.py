import decimal
import json
import os.path

from builtins import all
from collections import Mapping

from django.core import serializers
from django.db.models import Max, Min
from django.db.models.functions import datetime
from django.utils.datetime_safe import strftime

from heron.settings import DEBUG
from vfwheron.models import TblMeta, TblVariable, LtDomain, LtLicense, LtSite, LtSoil, LtUser, TblSensor, LtProject, \
    NmMetaDomain
from django.contrib.gis.db import models


class newFiltermenu():
    menu_tables = [LtProject, LtLicense, LtSite, LtSoil, LtUser, TblMeta, TblSensor, TblVariable]
    json_menu = {}

    def build_menu(LANG='EN'):
        newFiltermenu.build_menu2(newFiltermenu, LANG)
        print(LtDomain.menu_name)
        print(LtDomain.newmenu_name[LANG])
        # menu_dict = {tables.newmenu_name[LANG]: tables for tables in newFiltermenu.menu_tables}
        childs = []
        main = []
        for menu in newFiltermenu.menu_tables:  # Loop through all tables, i.e. LtSoil, LtProject...

            try:
                menu.filter_type
            except AttributeError:
                filter_type = {}
            else:
                filter_type = menu.filter_type

            if menu == LtProject:  # LtDomain is a seperate table that needs special treatment
                # TODO: That might be a case for the model.manager
                print('Something special for LtDomain')
                child_column = menu.newcolumn_dict.keys()
                value = menu.newcolumn_dict.values()
                for child_column, value in menu.newcolumn_dict.items():  # 'elevation': {'DE': 'Hohe', 'EN': 'Elevation'}
                    child_name = value[LANG]

                print('key, value : ', child_column, value )
                grandchilds = []
                inner_child = {}
                selectables = count_grandchilds = 0
                # print(menu.objects.select_related().values_list(key, flat=True).distinct())
                query_set = menu.objects.select_related().values_list(child_column,
                                                                      flat=True).distinct()
                query_path = menu.newpath + '__' + child_column

                for grandchild_name in query_set:
                    print('name: ', grandchild_name)
                    if grandchild_name is not None:
                        print('# # # name: ', grandchild_name)
                        # print("TblMeta.objects.filter(" + query_path + "='" + str(name) + "').count()")
                        count = eval("TblMeta.objects.filter(" + query_path + "='" + str(grandchild_name) + "').count()")
                        selectables = selectables + 1 if count > 1 else selectables
                        if count >= 0:  # TODO: change here if you don't want to have values with count=0 in menu
                            inner_grandchild = {
                                'name': str(grandchild_name),
                                'count': count,
                                'chosen': True,
                                # 'selectable': True if count > 0 else False
                            }
                            count_grandchilds = count_grandchilds + 1
                            grandchilds.append(inner_grandchild)
                        # print('grandchilds: ', grandchilds)
                    inner_child = {
                        'name': child_name,
                        'count': count_grandchilds,
                        'chosen': False,
                        'selectables': selectables
                    }
                    if selectables >= 0:
                        inner_child = {**inner_child, **{'grandchilds': grandchilds}}
                childs.append(inner_child)

                # query = eval("NmMetaDomain.objects.filter(" + query_path + "='"+name+"').count()")
                bla = LtDomain.objects.filter(pid=None)
                # print(LtDomain.objects.filter(id=LtDomain.objects.filter(pid=None)))
                # print(LtDomain.objects.filter(pid=None))
                # for i in bla:
                #     print(i.id, LtDomain.objects.filter(pid=i.id))

            # Everything except of LtDomain
            else:
                for child_column, value in menu.newcolumn_dict.items():  # key: license_abb,comercial,geology, value:Geologie ...
                    grandchilds = []
                    inner_child = {}
                    selectables = count_grandchilds = 0
                    selector_type = filter_type[child_column] if child_column in filter_type else False

                    # get available values from database tables:
                    query_set = menu.objects.select_related().values_list(child_column,
                                                                          flat=True).distinct()  # marls, schist, ...

                    # remove empty columns and columns with None values only; keep rows with None if column has values too
                    if query_set is not [None] and ((len(query_set) == 1 and query_set[0] is not None) or (len(query_set) > 1)):
                        query_path = child_column if menu.newpath is '' else menu.newpath + '__' + child_column

                        # special grandchild if selector is slider
                        if selector_type == 'slider' or selector_type == 'date':
                            # menu.objects.aggregate(min_value=Min('query_path'), max_value=Max('query_path'))
                            # print("TblMeta.objects.filter(" + menu.newpath + "='" + key + "').count()")
                            count = menu.objects.select_related().values_list(child_column,
                                                                          flat=True).distinct().count()
                            # TblMeta.objects.select_related().values_list(si)
                            # menu.objects.exclude(query_path='NaN').aggregate(min_value=Min('books__price'), max_value=Max('books__price'))
                            if selector_type == 'slider':
                                min_max = eval("TblMeta.objects.exclude(" + query_path + "='NaN').aggregate(min_value=Min('" + query_path + "'), max_value=Max('" + query_path + "'))")
                            else:
                                min_max = eval("TblMeta.objects.aggregate(min_value=Min('" + query_path + "'), max_value=Max('" + query_path + "'))")

                            selectables = selectables + 1 if count > 1 else selectables
                            inner_grandchild = {
                                # 'name': str(name),
                                'type': selector_type,
                                'count': count,
                                'chosen_min': False,
                                'chosen_max': False,
                                'selectable_min': str(min_max['min_value']),
                                'selectable_max': str(min_max['max_value']),
                            }
                            count_grandchilds = count_grandchilds + 1
                            grandchilds.append(inner_grandchild)

                        # grandchilds if no slider
                        else:
                            for grandchild_name in query_set:  # marls, schist, ...
                                if grandchild_name is not None:
                                    # print("TblMeta.objects.filter(" + query_path + "='" + str(name) + "').count()")
                                    count = eval("TblMeta.objects.filter(" + query_path + "='" + str(grandchild_name) + "').count()")
                                    # print('# # # # # #: ', count)
                                    selectables = selectables + 1 if count > 1 else selectables
                                    if count >= 0:  # TODO: change here if you don't want to have values with count=0 in menu
                                        inner_grandchild = {
                                            'name': str(grandchild_name),
                                            'count': count,
                                            'chosen': False,
                                        }
                                        count_grandchilds = count_grandchilds + 1
                                        grandchilds.append(inner_grandchild)
                    inner_child = {
                        'name': value[LANG],
                        'count': count_grandchilds,
                        'chosen': False,
                        'selectables': selectables
                    }
                    if selectables >= 0:
                        inner_child = {**inner_child, **{'grandchilds': grandchilds}}
                    childs.append(inner_child)

                inner_main = {
                    'name': menu.menu_name,
                    'childs': childs
                }
                main.append(inner_main)
                #
                # save_path = '/home/marcus/git/vforwater-portal/vfwheron/test.json'
                # file = open(save_path, "w")
                # file.write(json.dumps(main))
                # file.close()
        return 0

    def build_menu2(self, LANG='DE'):
        menu = LtSite

        try:
            menu.filter_type
        except AttributeError:
            filter_type = {}
        else:
            filter_type = menu.filter_type

        child_column = list(menu.column_dict)[0]
        selector_type = filter_type[child_column] if child_column in filter_type else False
        print('selector_type: ', selector_type)
        if selector_type:
            self.build_special_grandchilds(self, menu, selector_type)
        else:
            self.build_grandchilds(self, menu)
        return 0

    def build_grandchilds(self, menu):
        grandchilds = []
        selectables = count_grandchilds = 0

        child_column = list(menu.newcolumn_dict)[0]  # TODO: Der Loop hierfür muss ausserhalb kommen
        print('child_column: ', child_column)
        query_path = menu.newpath + '__' + child_column
        print('query_path: ', query_path)

        query_set = menu.objects.select_related().values_list(child_column,
                                                              flat=True).distinct()  # marls, schist, ...
        print('query_set: ', query_set)
        for grandchild_name in query_set:
            if grandchild_name is not None:
                count = eval("TblMeta.objects.filter(" + query_path + "='" + str(grandchild_name) + "').count()")
                selectables = selectables + 1 if count > 1 else selectables
                if count >= 0:  # TODO: change here if you don't want to have values with count=0 in menu
                    inner_grandchild = {
                        'name': str(grandchild_name),
                        'count': count,
                        'chosen': False,
                    }
                    count_grandchilds = count_grandchilds + 1
                    grandchilds.append(inner_grandchild)
        result = [grandchilds, selectables]
        print('result: ', result)
        return result

    def build_special_grandchilds(self, menu, selector_type):
        grandchilds = []
        selectables = count_grandchilds = 0
        child_column = list(menu.column_dict)[0]
        query_path = menu.newpath + '__' + child_column

        # special grandchild if selector is slider
        if selector_type == 'slider' or selector_type == 'date':
            count = menu.objects.select_related().values_list(child_column,
                                                              flat=True).distinct().count()
            if selector_type == 'slider':
                min_max = eval(
                    "TblMeta.objects.exclude(" + query_path + "='NaN').aggregate(min_value=Min('" + query_path +
                    "'), " "max_value=Max('" + query_path + "'))")
            else:
                min_max = eval(
                    "TblMeta.objects.aggregate(min_value=Min('" + query_path + "'), max_value=Max('" + query_path +
                    "'))")

            selectables = selectables + 1 if count > 1 else selectables
            inner_grandchild = {
                # 'name': str(name),
                'type': selector_type,
                'count': count,
                'chosen_min': False,
                'chosen_max': False,
                'selectable_min': str(min_max['min_value']),
                'selectable_max': str(min_max['max_value']),
            }
            count_grandchilds = count_grandchilds + 1
            grandchilds.append(inner_grandchild)

        result = [grandchilds, selectables]
        print('result2: ', result)
        return result


def selection_counts(menu, filter_selection):
    for parent in filter_selection.keys():

        parent_name = menu.get(parent).get("name")
        print('*** parent name: ', parent_name)
        for child in filter_selection.get(parent):
            child_name = menu.get(parent).get(child).get("name")
            print('** child name: ', child_name)
            item = filter_selection.get(parent).get(child)
            item_name = menu.get(parent).get(child).get(item).get("name")
            print('* item_name: ', item_name)
            # total = TblMeta.objects.filter(self.query_paths[grand_child]='values').count()
            # total = eval("TblMeta.objects.filter(" + self.query_paths[grand_child] + "='" + values + "').count()")
    return 0


class Menu():
    def __init__(self, lang='EN'):
        """
        :type table: object
        """
        # to see menu items without content set min_amount to 0
        # self.min_amount = 0 if DEBUG else 1
        self.min_amount = 1
        self.lang = lang
        # self.menu_list = [LtDomain, LtLicense, LtSite, LtSoil, LtUser, TblMeta, TblSensor, TblVariable]
        self.menu_list = [LtLicense, LtSite, LtSoil, LtUser, TblMeta, TblSensor, TblVariable]
        # self.menu_list = [LtDomain]
        # self.menu()
        # self.json_menu()
        self.menu_map()

    # TODO: Here is a complete map of the menu is build. Better: Build it only with elements that are used in the menu
    def menu_map(self):
        print(' - - -- - - NEVER HERE *** ***')
        maped_menu = {}
        for table in self.menu_list:
            # print('table: ', table)
            # print('name: ', table.newmenu_name[self.lang])
            # print('path: ', table.newpath)
            print('*** column: ', table.newcolumn_dict)
            for child in table.newcolumn_dict.keys():
                print('* child: ', child)
                print('** child: ', table.newcolumn_dict[child][self.lang])
                # TblMeta.objects.filter(variable__variable_name='Lufttemperatur')
                path = table.newpath+"__"+child if table.newpath != '' else child
                print('***: ', TblMeta.objects.values_list(path).distinct())
                # total = eval("TblMeta.objects.filter(" + path + "='" + values + "').count()")
            maped_menu[table.newmenu_name[self.lang]] = table.newpath
        print('maped_menu: ', maped_menu)
        return maped_menu

    def menu(self):
        print('ACHTUNG!!! DU BAUST EIN MENU!!!')
        count = 0
        json_menu = {}
        # menu_map = {}
        for table in self.menu_list:
            whole_menu = Table(table, self.min_amount, self.lang)
            json_table = whole_menu.json_child
            if json_table['total'] >= self.min_amount:
                count = count + 1
                menu_dict = {
                    'name': table.newmenu_name[self.lang],
                    # 'chosen': False,
                    'total': json_table['total'],
                }
                menu_dict.update(json_table['C'])
                json_menu.update({'P' + str(count): menu_dict})

        return json_menu

    # def json_menu(self):
    #     json_menu = json.dumps(self.menu())
    #
    #     if DEBUG:  # write the json menu for the web-site to file in DEBUG mode
    #         save_path = '/home/marcus/git/vforwater-portal/vfwheron/test.json'
    #         file = open(save_path, "w")
    #         file.write(json_menu)
    #         file.close()
    #
    #     return json_menu


class Table():
    def __init__(self, table, min_amount, lang='EN'):
        """
        :type table: object
        """
        self.min_amount = min_amount
        self.lang = lang
        self.table_name = table
        self.child_columns = table.newcolumn_dict.keys()
        self.get_query_set()
        self.get_query_path()
        self.get_filter_type()
        self.json_child = self.build_json_child

    def get_filter_type(self):
        try:
            self.table_name.filter_type
        except AttributeError:
            self.filter_type = {}
        else:
            self.filter_type = self.table_name.filter_type

    def get_query_set(self):
        self.child = {}
        for columns in self.child_columns:
            query_set = self.table_name.objects.select_related().values_list(columns, flat=True).distinct()
            if not (len(query_set) <= 1 and query_set[0] is None):
                self.child[columns] = query_set


    def get_query_path(self):
        self.query_paths = {}
        for columns in self.child_columns:
            if self.table_name.newpath == '':
                query_path = columns
            else:
                query_path = self.table_name.newpath + '__' + columns
            self.query_paths[columns] = query_path

    @property
    def build_json_child(self):
        counter = 0
        json_all_childs = {}
        result = {}

        for grand_child in self.child_columns:
            grandchilds = {}
            recursive = False
            if grand_child in self.child and grand_child is not None:
                # build different menus according to the type defined in the model:
                if grand_child in self.filter_type:
                    switch = self.filter_type[grand_child]
                    if switch == 'slider':
                        result = self.build_slider_json(grand_child)
                    elif switch == 'date':
                        result = self.build_date_json(grand_child)
                    # Recursive is one single table, so the build process is highly customized to that single table
                    elif switch == 'recursive':
                        result = self.build_recursive_json(grand_child)
                        recursive = True
                else:
                    result = self.build_default_json(grand_child)

                if recursive:
                    counter = result['total']
                    json_all_childs = result['json']
                else:
                    grandchilds.update({'name': self.table_name.newcolumn_dict[grand_child][self.lang],
                                        'total': result['total'],
                                        # 'chosen': False
                                        })
                    grandchilds.update(result['json'])
                    if result['total'] >= self.min_amount:
                        counter = counter + 1
                        json_all_childs.update({'C' + str(counter): grandchilds})

        result = {'total': counter, 'C': json_all_childs}
        return result

    def build_default_json(self, grand_child):
        all_grandchilds = {}
        counter = 0
        for values in self.child[grand_child]:
            if values is not None:
                total = eval("TblMeta.objects.filter(" + self.query_paths[grand_child] + "='" + values + "').count()")
                grandchild_dict = {
                    'name': values,
                    'total': total,
                    # 'chosen': False,
                }
                if total >= self.min_amount:
                    counter = counter + 1
                    all_grandchilds.update({'I' + str(counter) : grandchild_dict})
        # if there are no values for the submenu, return nothing
        result = {'json': all_grandchilds, 'total': counter}
        return result

    def build_slider_json(self, grand_child):
        counter = 0
        total = len(self.child[grand_child])
        # total = eval("TblMeta.objects.filter(" + grand_child + ").count()")
        try:
            min_max = eval("TblMeta.objects.exclude(" + self.query_paths[grand_child] +
                           "='NaN').aggregate(min_value=Min('" + self.query_paths[grand_child] + "'), max_value=Max('" +
                           self.query_paths[grand_child] + "'))")
        except ValueError:
            min_max = eval("TblMeta.objects.aggregate(min_value=Min('" + self.query_paths[grand_child] +
                           "'), max_value=Max('" + self.query_paths[grand_child] + "'))")
        grandchild_dict = {
            'type': 'slider',
            'total': total,
            'chosen_min': False,
            'chosen_max': False,
            'selectable_min': str(min_max['min_value']),
            'selectable_max': str(min_max['max_value']),
        }
        if total >= self.min_amount:
            counter = counter + 1
        result = {'json': grandchild_dict, 'total': counter}
        return result

    def build_date_json(self, grand_child):
        counter = 0
        total = len(self.child[grand_child])
        min_max = eval("TblMeta.objects.aggregate(min_value=Min('" + self.query_paths[grand_child] + "'), max_value=Max('"
                       + self.query_paths[grand_child] + "'))")
        grandchild_dict = {
                'type': 'date',
                'total': total,
                'chosen_min': False,
                'chosen_max': False,
                'selectable_min': str(min_max['min_value']),
                'selectable_max': str(min_max['max_value']),
            }
        if total >= self.min_amount:
            counter = counter + 1
        result = {'json': grandchild_dict, 'total': counter}
        return result

    def build_recursive_json(self, grand_child):
        # Recursive is one single table, so the build process is highly customized to that single table
        parent_queryset = eval(self.table_name.mother+'.objects.all()')
        project_values = parent_queryset.values("project_name", "id")

        all_childs = {}
        child_counter = 0
        for project in project_values:
            project_name = project['project_name']
            project_id = project['id']

            recursive_child = parent_queryset.filter(ltdomain__pid=None).filter(project_name=project_name).values("ltdomain__domain_name", "ltdomain__id")

            # build the inner child
            all_grandchilds = {}
            child_total = 0
            for child in recursive_child:
                child_name = child.get('ltdomain__domain_name')
                child_id = child.get('ltdomain__id')

                ltdomain_query = parent_queryset.filter(ltdomain__pid=child_id)
                grandchild_values = ltdomain_query.values("ltdomain__domain_name", "ltdomain__id")

                # build the innermost menu
                grandchild_counter = 0
                inner_grandchild = {}
                for grandchild in grandchild_values:
                    grandchild_name = grandchild['ltdomain__domain_name']

                    # build the innermost selectables:
                    grandchild_total = TblMeta.objects.filter(nmmetadomain__domain__project_id=project_id).filter(nmmetadomain__domain__pid_id=child_id).filter(nmmetadomain__domain__domain_name=grandchild_name).count()
                    if grandchild_total >= self.min_amount:
                        grandchild_json = {
                            'name': grandchild_name,
                            'total': grandchild_total,
                            # 'chosen': False,
                        }
                        grandchild_counter = grandchild_counter + 1
                        inner_grandchild.update({'I'+str(grandchild_counter):grandchild_json})

                grandchild_dict = {
                    'name': child_name,
                    'total': grandchild_counter,
                    # 'chosen': False,
                    'childtitle': self.table_name.submenu_names['subdomain'][self.lang],
                }
                grandchild_dict.update(inner_grandchild)

                if grandchild_counter >= self.min_amount:
                    child_total = child_total + 1
                    all_grandchilds.update({'C'+str(child_total): grandchild_dict})

            child_dict = {
                'type': 'recursive',
                'title': self.table_name.submenu_names['project'][self.lang],
                'name': str(project_name),
                'total': child_total,
                # 'chosen': False,
                'childtitle': self.table_name.submenu_names['domain'][self.lang],
            }

            child_dict.update(all_grandchilds)

            if child_total >= self.min_amount:
                child_counter = child_counter + 1
                all_childs.update({'C'+str(child_counter):child_dict})

        # if there are no values for the submenu, return nothing
        result = {'json': all_childs, 'total': child_counter}

        return result


    def print_properties(self):
        print('* table_name: ', self.table_name)
        print('* filter_type: ', self.filter_type)
        print('* child_columns: ', self.child_columns)
        print('* query_paths: ', self.query_paths)
        print('* child: ', self.child)


# TODO: There is no need to have this as models.Manager (Didn't use it). Find a better place for class
class FilterMenu(models.Manager):
    # test = Table(LtSite)  # LtSite)LtSoil
    # test.print_properties()
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
