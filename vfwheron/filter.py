import json
import logging
from django.db.models import Max, Min
from heron.settings import DEBUG

from vfwheron.models import TblMeta, TblVariable, LtDomain, LtLicense, LtSite, LtSoil, LtUser, TblSensor, LtProject, \
    NmMetaDomain, LtQuality, LtLocation
logger = logging.getLogger(__name__)


def _build_path_value_pair(parent_menu, child, item):
    """

    :param parent_menu:
    :param child:
    :param item:
    :return:
    """
    path = ''
    value = ''
    if isinstance(item, str):
        path = parent_menu['path'] + "__" + parent_menu[child]['column'] if parent_menu['path'] != '' else \
            parent_menu[child]['column']
        value = parent_menu[child][item]['name']  # e.g. 'net radiation'
    elif isinstance(item, list):
        path = 'id__in'
        value = item
    else:
        # logger.debug('Unknown type of item.')
        print('Unknown type of item.')
    return {'path': path, 'value': value}


def build_select_filters(menu, filter_selection):
    """

    :param menu:
    :type menu:
    :param filter_selection:
    :type filter_selection:
    :return:
    :rtype:
    """
    # build queries for the filter values
    short_filter = {}
    long_filter = {}
    # build the django filter for every selection separately
    for parent in filter_selection:
        for child in filter_selection[parent]:
            query_pair = _build_path_value_pair(menu[parent], child, filter_selection[parent][child])

            # TODO: maybe use intersection to store previous queries (compare performance of both)
            # TODO: also compare .filter(x).filter(y) vs .filter(x,y). Result seems to be equal (But shouldn't!?). Time?
            short_filter.update( {query_pair['path']: query_pair['value']})
            long_filter.update({parent + child: {query_pair['path']: query_pair['value']}})

    # build filters for the menu with all selections, and filters with the selection missing where the user selected it
    # (to prevent zero values where the user made a selection)
    # in other words:
    # This is supposed to be used to see available datasets in menus where a selection is made (to see the other
    # 'options' in the active menu)
    spec_filter = {}
    for key in long_filter:
        for k in long_filter:
            if k != key:
                spec_filter.setdefault(key, {}).update(long_filter[k])

    return {'filters': short_filter, 'active_f': spec_filter}


def build_id_list(menu, filter_selection):
    """
    Build list of IDs needed to create in geoserver a layer with the selected elements
    :param menu:
    :type menu:
    :param filter_selection:
    :type filter_selection:
    :return:
    :rtype:
    """
    # build queries for the filter values
    query_filters = {}
    for parent in filter_selection:
        for child in filter_selection[parent]:
            try:
                if 'draw' in menu[parent][child]['type']:  # following https://docs.python.org/3/glossary.html#term-eafp
                    pass
            except KeyError:
                query_pair = _build_path_value_pair(menu[parent], child, filter_selection[parent][child])

                query_filters.update({'{0}'.format(query_pair['path']): query_pair['value']})

    return {'all_filters': list(TblMeta.objects.filter(**query_filters).values_list('id', flat=True))}


class FilterMethods:
    """

    """

    @staticmethod
    def selection_counts(menu, filter_selection):
        """

        :param menu:
        :type menu:
        :param filter_selection:
        :type filter_selection:
        :return:
        :rtype:
        """
        result = {}

        query_filter = build_select_filters(menu, filter_selection)
        std_query = TblMeta.objects.filter(**query_filter['filters'])
        filtermap = query_filter['active_f']
        # TODO: deactivate zero values then (at the moment deactivating wouldn't make sense/would be a hassle for user)
        for parent in menu:
            c = 1
            child_result = {}
            while "C" + str(c) in menu[parent]:
                path = menu[parent]['path'] + "__" + menu[parent]["C" + str(c)]['column'] if menu[parent]['path'] \
                    != '' else menu[parent]["C" + str(c)]['column']
                child = menu[parent]["C" + str(c)]
                query1 = TblMeta.objects.filter(**filtermap[parent + "C" + str(c)]) if parent + "C" + str(c) in \
                    filtermap else std_query
                item_result = {}
                i = 1
                c_type = child.get('type')
                if c_type is None:
                    while "I" + str(i) in child:
                        filter_items = {'{0}'.format(path): child["I" + str(i)]['name']}
                        item_result.update({"I" + str(i): query1.filter(**filter_items).count()})
                        i += 1
                elif c_type == 'draw':
                    filter_items = {'{0}'.format(path): child['name']}
                    item_result = query1.filter(**filter_items).count()
                else:
                    print('Adjust your filter.py selection_counts to type: ', c_type)
                child_result.update({"C" + str(c): item_result})
                c += 1
            result.update({parent: child_result})
        print('result of count: ', result)
        return result

    @staticmethod
    def select_data_points(menu, filter_selection):
        """

        :param menu:
        :type menu:
        :param filter_selection:
        :type filter_selection:
        :return:
        :rtype:
        """
        data_points = []
        return data_points


class Menu:
    """
    Class to build the menu for server and client from the models.
    The used Tables are defined in the menu_list.
    The hierarchical structure of the menu is Parent - Child - Item, where Parents are the respective tables,
    Childs represent the columns and Items the content of a column.
    """

    # The order here is used as order for the menu on the client
    # menu_list = [LtDomain, LtLicense, LtQuality, LtSite, LtSoil, LtUser, TblMeta, TblSensor, TblVariable]
    # #queries [LtLocation(2), LtLicense(10), LtQuality(8), LtSite(47), LtSoil(8), LtUser(17), TblMeta(307), TblSensor(18), TblVariable(19)]
    # => TODO: TblMeta holds information about time of dataset => write view/something to reduce queries!
    # TODO: Check queries in detail (LtLocation is okay!)
    menu_list = [LtLocation, LtLicense, LtQuality, LtSite, LtSoil, LtUser, TblSensor, TblVariable]
    # menu_list = [LtLocation, LtLicense, LtQuality, LtSite, LtSoil, LtUser, TblMeta, TblSensor, TblVariable]

    def __init__(self, user='default'):
        """

        :param user:
        :type user:
        """
        # to see menu items without content set min_amount to 0
        # self.min_amount = 0 if DEBUG else 1
        self.min_amount = 1
        self.user = user
        self.user_query_set()
        # self.user = user
        self.menu_list = Menu.menu_list
        # self.menu_list = [LtDomain]
        # self.menu()
        # self.write_json_menu()

    def user_query_set(self):
        """

        :return:
        :rtype:
        Build a base query set for the respective user
        """
        if self.user == 'default':
            query_set = TblMeta.objects.filter(license__share=True).all()
            for i in query_set:
                return
                # print('i: ', i)
                # print('query_set: ', query_set.__len__())
                # print('query_set: ', query_set.filter(tbl))

    def menu(self, user):
        """

        :param user:
        :type user:
        :return:
        :rtype:
        Function to build the actual menu
        """
        # print('ACHTUNG!!! DU BAUST EIN MENU!!!')  # One line to check how often this is accessed        count = 0
        json_menu = {}  # menu for client
        menu_map = {}  # menu for server
        count = 0
        for table in self.menu_list:
            whole_menu = Table(table, self.min_amount, self.user_query_set)
            json_table = whole_menu.json_child['client']
            map_table = whole_menu.json_child['server']
            # map_table = whole_menu.map_child
            if json_table['total'] >= self.min_amount:
                count = count + 1

                menu_dict = {
                    'name': table.menu_name,
                    'total': json_table['total'],
                    }
                menu_dict.update(json_table['C'])
                json_menu.update({'P' + str(count): menu_dict})

                map_dict = {
                    'name': table.menu_name,
                    'path': table.path,
                    }
                if getattr(table, 'filter_type', None):
                    map_dict['filter'] = table.filter_type

                map_dict.update(map_table['C'])
                menu_map.update({'P' + str(count): map_dict})
        # print('menu_map: ', menu_map)
        # print('json_menu: ', json_menu)

        return {'client': json_menu, 'server': menu_map}


# use this method to write an example of the json menu to disk
#     def write_json_menu(self):
#         json_menu = json.dumps(self.menu()['client'])
#         menu_map = json.dumps(self.menu()['server'])
#
#         if DEBUG:  # write the json menu for the web-site to file in DEBUG mode
#             save_path = '/home/marcus/git/vforwater-portal/vfwheron/test.json'
#             file = open(save_path, "w")
#             file.write(json_menu)
#             file.close()
#
#             save_path = '/home/marcus/git/vforwater-portal/vfwheron/test_map.json'
#             file = open(save_path, "w")
#             file.write(menu_map)
#             file.close()
#
#         return json_menu


# TODO: Check how often 'get_filter_type' and the others are called; Shall they be properties?
class Table:
    """
    Class to get all information from each table (that is used for the menu) to build the menu.
    The models define which columns should be shown in the menu. Here the necessary information for django
    to build queries for the columns of interest is brought together.
    """
    # TODO: IMPORTANT! default query should be used with a query for a default user
    default_query = TblMeta.objects.select_related().filter(license__share=True)

    def __init__(self, table, min_amount, user_query_set):
        """

        :param table:
        :type table:
        :param min_amount:
        :type min_amount:
        :param user_query_set:
        :type user_query_set:
        :type table: object
        """
        self.filter_type = {}
        self.child = {}
        self.min_amount = min_amount
        self.user_query_set = user_query_set
        self.table_name = table
        self.child_columns = table.column_dict.keys()
        self.default_user_child_columns = {}
        self.get_query_set()
        self.get_query_path()
        self.get_filter_type()
        self.json_child = self.build_json_child

    #     TODO: Add user_query like self.default_query

    def get_filter_type(self):
        """

        :return:
        :rtype:
        check if an entry in the table has a special type,
        so there is need for a special filter, e.g. slider, date, draw
        """
        try:
            self.filter_type = self.table_name.filter_type
        except AttributeError:
            pass

        # else:
        #     self.filter_type = self.table_name.filter_type

    def get_query_set(self):
        """

        :return:
        :rtype:
        """
        for columns in self.child_columns:
            # if else when you want filter for default user
            # if self.table_name.path:
            #     table_path = self.table_name.path + '__' + columns
            #     # query_set =
            # TblMeta.objects.select_related().filter(license__share=True).values_list(table_path, flat=True).distinct()
            #     # print('query_set: ', query_set)
            #     # query1 = TblMeta.objects.select_related().filter(license__share=True)
            #     query_set = self.default_query.values_list(table_path, flat=True).distinct()
            #     # print(' * * *  * * * * query_set: ', query_set)
            #
            #     # print('query2: ', query2)
            # else:
            #     query_set = self.default_query.values_list(columns, flat=True).distinct()
            excluder = {'{0}'.format(columns): None}
            query_set = list(self.table_name.objects.select_related().distinct().exclude(**excluder).
                             values_list(columns, flat=True))
            if len(query_set) > 0:
                self.child[columns] = query_set

    def get_query_path(self):
        """

        :return:
        :rtype:
        Build the path to a column of a table for a django query
        """
        self.query_paths = {}
        for columns in self.child_columns:
            if self.table_name.path == '':
                self.query_paths[columns] = columns
            else:
                self.query_paths[columns] = self.table_name.path + '__' + columns

    @property
    def build_json_child(self):
        """

        :return:
        :rtype:
        """
        counter = 0
        json_all_childs = {}
        map_all_childs = {}
        result = {}

        for grand_child in self.child_columns:
            grandchilds = {}
            map_grandchilds = {}
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
                        # TODO: Check if https://docs.djangoproject.com/en/2.0/ref/models/querysets/#prefetch-related
                        # can help
                        result = self.build_recursive_json(grand_child)
                        recursive = True
                    elif switch == 'draw':
                        result = self.build_draw_json(grand_child)
                else:
                    result = self.build_default_json(grand_child)

                if recursive:
                    counter = result['total']
                    json_all_childs = result['json']
                    map_all_childs = result['server']
                else:
                    # print('* * * * * grand_child: ', grand_child)
                    # print('* * * * * result["total"]: ', result['total'])
                    grandchilds.update(
                            dict(name=self.table_name.column_dict[grand_child], total=result['total']))
                    map_grandchilds.update({
                        'name': self.table_name.column_dict[grand_child],
                        'column': grand_child,
                        })

                    grandchilds.update(result['json'])
                    map_grandchilds.update(result['server'])

                    if result['total'] >= self.min_amount:
                        counter = counter + 1
                        json_all_childs.update({'C' + str(counter): grandchilds})
                        map_all_childs.update({'C' + str(counter): map_grandchilds})

        result = {'total': counter, 'C': json_all_childs}
        map_result = {'C': map_all_childs}
        # print('client: ', result)
        # print('server: ', map_result)
        return {'client': result, 'server': map_result}

    def build_default_json(self, grand_child):
        """

        :param grand_child:
        :type grand_child:
        :return:
        :rtype:
        """
        all_grandchilds = {}
        map_grandchilds = {}
        counter = 0
        for values in self.child[grand_child]:
            if values is not None:
                filtermap = {'{0}'.format(self.query_paths[grand_child]): values}
                total = TblMeta.objects.filter(**filtermap).count()
                grandchild_dict = {
                    'name': values,
                    'total': total,
                    # 'chosen': False,
                    }
                map_grandchild_dict = {
                    'name': values,
                    }

                if total >= self.min_amount:
                    counter = counter + 1
                    all_grandchilds.update({'I' + str(counter): grandchild_dict})
                    map_grandchilds.update({'I' + str(counter): map_grandchild_dict})
        # if there are no values for the submenu, return nothing
        return {'json': all_grandchilds, 'total': counter, 'server': map_grandchilds}

    def build_slider_json(self, grand_child):
        """

        :param grand_child:
        :type grand_child:
        :return:
        :rtype:
        """
        counter = 0
        total = len(self.child[grand_child])
        keyword = self.query_paths[grand_child]
        print('keyword: ', keyword)
        excl_nan = {'{0}'.format(keyword): 'NaN'}
        excl_none = {'{0}'.format(keyword): None}
        c_min = {'{0}'.format('min_value'): Min(keyword)}
        c_max = {'{0}'.format('max_value'): Max(keyword)}
        # total = eval("TblMeta.objects.filter(" + grand_child + ").count()")
        try:
            # min_max = eval("TblMeta.objects.exclude(" + self.query_paths[grand_child] +
            #             "='NaN').aggregate(min_value=Min('" + self.query_paths[grand_child] + "'), max_value=Max('" +
            #                self.query_paths[grand_child] + "'))")
            min_max = TblMeta.objects.exclude(**excl_nan).exclude(**excl_none).aggregate(**c_min, **c_max)
            print('min_max: ', min_max)
        except ValueError:
            # min_max = eval("TblMeta.objects.aggregate(min_value=Min('" + self.query_paths[grand_child] +
            #                "'), max_value=Max('" + self.query_paths[grand_child] + "'))")
            min_max = TblMeta.objects.aggregate(**c_min, **c_max)
            return {'json': '', 'total': 0, 'server': ''}
        grandchild_dict = {
            'type': 'slider',
            'total': total,
            'chosen_min': False,
            'chosen_max': False,
            'selectable_min': str(min_max['min_value']),
            'selectable_max': str(min_max['max_value']),
            }
        map_grandchild_dict = {
            'type': 'slider',
            'selectable_min': str(min_max['min_value']),
            'selectable_max': str(min_max['max_value']),
            }
        if total >= self.min_amount:
            counter = counter + 1
        return {'json': grandchild_dict, 'total': counter, 'server': map_grandchild_dict}

    def build_date_json(self, grand_child):
        """

        :param grand_child:
        :type grand_child:
        :return:
        :rtype:
        """
        print('date')
        counter = 0
        total = len(self.child[grand_child])
        d_min = {'{0}'.format('min_value'): Min(self.query_paths[grand_child])}
        d_max = {'{0}'.format('max_value'): Max(self.query_paths[grand_child])}

        min_max = TblMeta.objects.aggregate(**d_min, **d_max)
        # min_max = eval("TblMeta.objects.aggregate(min_value=Min('" + self.query_paths[grand_child] + "'),
        #   max_value=Max('" + self.query_paths[grand_child] + "'))")
        grandchild_dict = {
            'type': 'date',
            'total': total,
            'chosen_min': False,
            'chosen_max': False,
            'selectable_min': str(min_max['min_value']),
            'selectable_max': str(min_max['max_value']),
            }

        map_grandchild_dict = {
            'type': 'date',
            'selectable_min': str(min_max['min_value']),
            'selectable_max': str(min_max['max_value']),
            }
        if total >= self.min_amount:
            counter = counter + 1
        return {'json': grandchild_dict, 'total': counter, 'server': map_grandchild_dict}

    def build_recursive_json(self, grand_child):
        """

        :param grand_child:
        :type grand_child:
        :return:
        :rtype:
        """
        # Recursive is one single table, so the build process is highly customized to that single table
        parent_queryset = eval(self.table_name.mother + '.objects.all()')
        project_values = parent_queryset.values("project_name", "id")

        all_childs = {}
        map_childs = {}
        child_counter = 0
        for project in project_values:
            project_name = project['project_name']
            project_id = project['id']

            recursive_child = parent_queryset.filter(ltdomain__pid=None).filter(project_name=project_name).\
                values("ltdomain__domain_name", "ltdomain__id")

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
                    # TODO: IMPORTANT! Check which result is right. Maybe all three cases in one Filter?
                    # grandchild_total = TblMeta.objects.filter(nmmetadomain__domain__project_id=project_id,
                    # nmmetadomain__domain__pid_id=child_id, nmmetadomain__domain__domain_name=grandchild_name).count()
                    grandchild_total = TblMeta.objects.filter(nmmetadomain__domain__project_id=project_id).\
                        filter(nmmetadomain__domain__pid_id=child_id).\
                        filter(nmmetadomain__domain__domain_name=grandchild_name).count()
                    if grandchild_total >= self.min_amount:
                        grandchild_json = {
                            'name': grandchild_name,
                            'total': grandchild_total,
                            # 'chosen': False,
                            }
                        grandchild_counter = grandchild_counter + 1
                        inner_grandchild.update({'I' + str(grandchild_counter): grandchild_json})

                grandchild_dict = {
                    'name': child_name,
                    'total': grandchild_counter,
                    # 'chosen': False,
                    'childtitle': self.table_name.submenu_names['subdomain'],
                    }
                grandchild_dict.update(inner_grandchild)

                if grandchild_counter >= self.min_amount:
                    child_total = child_total + 1
                    all_grandchilds.update({'C' + str(child_total): grandchild_dict})

            child_dict = {
                'type': 'recursive',
                'title': self.table_name.submenu_names['project'],
                'name': str(project_name),
                'total': child_total,
                # 'chosen': False,
                'childtitle': self.table_name.submenu_names['domain'],
                }

            child_dict.update(all_grandchilds)

            if child_total >= self.min_amount:
                child_counter = child_counter + 1
                all_childs.update({'C' + str(child_counter): child_dict})

        # if there are no values for the submenu, return nothing
        return {'json': all_childs, 'total': child_counter, 'server': map_childs}

    def build_draw_json(self, grand_child):
        """

        :param grand_child:
        :type grand_child:
        :return:
        :rtype:
        """
        # types = TblMeta.objects.values_list('geometry__geometry_type', flat=True).distinct().
        #   exclude(geometry__geometry_type=None)
        counter = 0
        # for values in self.child[grand_child]:  # for now only for POINT data
        values = 'POINT'
        # total = TblMeta.objects.filter(geometry__geometry_type=values).count()
        filtermap = {'{0}'.format(self.query_paths[grand_child]): values}
        total = TblMeta.objects.filter(**filtermap).count()
        grandchild_dict = {
            'type': 'draw',
            'name': values,
            'total': total,
            # 'chosen': False,
            }
        map_grandchild_dict = {
            'type': 'draw',
            'name': values,
            }

        if total >= self.min_amount:
            counter = counter + 1
            # all_grandchilds.update({'I' + str(counter): grandchild_dict})
            # map_grandchilds.update({'I' + str(counter): map_grandchild_dict})
        # if there are no values for the submenu, return nothing
        return {'json': grandchild_dict, 'total': counter, 'server': map_grandchild_dict}

    def print_properties(self):
        """

        :return:
        :rtype:
        """
        print('* table_name: ', self.table_name)
        print('* filter_type: ', self.filter_type)
        print('* child_columns: ', self.child_columns)
        print('* query_paths: ', self.query_paths)
        print('* child: ', self.child)
