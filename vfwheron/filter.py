from heron.settings import DEBUG
from django.db.models import Max, Min

from vfwheron.models import TblMeta, TblVariable, LtDomain, LtLicense, LtSite, LtSoil, LtUser, TblSensor, LtProject, \
    NmMetaDomain


def build_select_filters(menu, filter_selection):
    # build queries for the filter values
    all_filters = ''
    single_filters = {}
    query_filters = {}
    # build the django filter for every selection separately
    for parent in filter_selection:
        for child in filter_selection[parent]:
            item = filter_selection[parent][child]

            path = menu[parent]['path'] + "__" + menu[parent][child]['column'] if menu[parent]['path'] != '' else \
            menu[parent][child]['column']
            value = menu[parent][child][item]['name']

            # TODO: maybe use intersection to store previous queries (compare performance of both)
            # TODO: also compare .filter(x).filter(y) vs .filter(x,y). Result seems to be equal (But shouldn't!?). Time?
            single_filters.update({parent+child:path+"='"+value+"'"})

    # build filters for the menu with all selections, and filters with the selection missing where the user selected it
    # (to prevent zero values where the user made a selection)
    for key in single_filters:
        all_filters += single_filters[key]+','
        spec_filter = ''
        for k in single_filters:
            if k != key:
                spec_filter += single_filters[k]+','
        query_filters.update({key: spec_filter})
    return {'all_filters': all_filters, 'one_excluded': query_filters}


def newbuild_id_list(menu, filter_selection):
    # build queries for the filter values
    query_filters = ''
    # build the django filter for every selection separately
    for parent in filter_selection:
        for child in filter_selection[parent]:
            item = filter_selection[parent][child]

            path = menu[parent]['path'] + "__" + menu[parent][child]['column'] if menu[parent]['path'] != '' else menu[parent][child]['column']
            value = menu[parent][child][item]['name']
            query_filters += path+"='"+value+"', "

    std_query = "TblMeta.objects.filter(" + query_filters + ").values_list('id', flat=True)"
    return {'all_filters':  list(eval(std_query))}


class FilterMethods:

    @staticmethod
    def selection_counts(menu, filter_selection):
        result = {}

        query_filter = build_select_filters(menu, filter_selection)
        std_query = "TblMeta.objects.filter("+query_filter['all_filters']+")"
        # TODO: deactivate zero values then (at the moment deactivating wouldn't make sense/would be a hassle for the user
        for parent in menu:
            c = 1
            child_result = {}
            while "C" + str(c) in menu[parent]:
                path = menu[parent]['path'] + "__" + menu[parent]["C" + str(c)]['column'] if menu[parent]['path'] != '' else menu[parent]["C" + str(c)]['column']
                child = menu[parent]["C" + str(c)]
                query1 = "TblMeta.objects.filter("+query_filter['one_excluded'][parent + "C" + str(c)]+")" if parent+"C" + str(c) in query_filter['one_excluded'] else std_query
                item_result = {}
                i = 1
                while "I"+str(i) in child:
                    value = child["I"+str(i)]['name']
                    item_result.update({"I"+str(i): eval(query1 + ".filter(" + path+"='"+value + "').count()")})
                    i += 1
                child_result.update({"C" + str(c): item_result})
                c += 1
            result.update({parent: child_result})
        return result

    @staticmethod
    def select_data_points(menu, filter_selection):
        data_points = []
        return data_points


class Menu:
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

    def menu(self):
        # print('ACHTUNG!!! DU BAUST EIN MENU!!!')  # One line to check how often this is accessed        count = 0
        json_menu = {}  # menu for client
        menu_map = {}  # menu for server
        count = 0
        for table in self.menu_list:
            whole_menu = Table(table, self.min_amount, self.lang)
            json_table = whole_menu.json_child['client']
            map_table = whole_menu.json_child['server']
            # map_table = whole_menu.map_child
            if json_table['total'] >= self.min_amount:
                count = count + 1
                menu_dict = {
                    'name': table.menu_name[self.lang],
                    'total': json_table['total'],
                }
                menu_dict.update(json_table['C'])
                json_menu.update({'P' + str(count): menu_dict})

                map_dict = {
                    'name': table.menu_name[self.lang],
                    'path': table.path,
                }
                map_dict.update(map_table['C'])
                menu_map.update({'P' + str(count): map_dict})

        return {'client': json_menu, 'server': menu_map}

    # use this method to write an example of the json menu to disk
    # def json_menu(self):
    #     json_menu = json.dumps(self.menu()['client'])
    #     menu_map = json.dumps(self.menu()['server'])
    #
    #     if DEBUG:  # write the json menu for the web-site to file in DEBUG mode
    #         save_path = '/home/marcus/git/vforwater-portal/vfwheron/test.json'
    #         file = open(save_path, "w")
    #         file.write(json_menu)
    #         file.close()
    #
    #         save_path = '/home/marcus/git/vforwater-portal/vfwheron/test_map.json'
    #         file = open(save_path, "w")
    #         file.write(menu_map)
    #         file.close()
    #
    #     return json_menu


# TODO: Check how often 'get_filter_type' and the others are called; Shall they be properties?
class Table:
    def __init__(self, table, min_amount, lang='EN'):
        """
        :type table: object
        """
        self.min_amount = min_amount
        self.lang = lang
        self.table_name = table
        self.child_columns = table.column_dict.keys()
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
            if self.table_name.path == '':
                query_path = columns
            else:
                query_path = self.table_name.path + '__' + columns
            self.query_paths[columns] = query_path

    @property
    def build_json_child(self):
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
            # TODO: Check if https://docs.djangoproject.com/en/2.0/ref/models/querysets/#prefetch-related can help
                        result = self.build_recursive_json(grand_child)
                        recursive = True
                else:
                    result = self.build_default_json(grand_child)

                if recursive:
                    counter = result['total']
                    json_all_childs = result['json']
                    map_all_childs = result['server']
                else:
                    grandchilds.update(
                        dict(name=self.table_name.column_dict[grand_child][self.lang], total=result['total']))
                    map_grandchilds.update({'name': self.table_name.column_dict[grand_child][self.lang],
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

        return {'client': result, 'server': map_result}

    def build_default_json(self, grand_child):
        all_grandchilds = {}
        map_grandchilds = {}
        counter = 0
        for values in self.child[grand_child]:
            if values is not None:
                total = eval("TblMeta.objects.filter(" + self.query_paths[grand_child] + "='" + values + "').count()")
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
                    all_grandchilds.update({'I' + str(counter) : grandchild_dict})
                    map_grandchilds.update({'I' + str(counter) : map_grandchild_dict})
        # if there are no values for the submenu, return nothing
        return {'json': all_grandchilds, 'total': counter, 'server': map_grandchilds}

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

        map_grandchild_dict = {
            'type': 'slider',
            'selectable_min': str(min_max['min_value']),
            'selectable_max': str(min_max['max_value']),
        }
        if total >= self.min_amount:
            counter = counter + 1
        return {'json': grandchild_dict, 'total': counter, 'server': map_grandchild_dict}

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

        map_grandchild_dict = {
            'type': 'date',
            'selectable_min': str(min_max['min_value']),
            'selectable_max': str(min_max['max_value']),
        }
        if total >= self.min_amount:
            counter = counter + 1
        return {'json': grandchild_dict, 'total': counter, 'server': map_grandchild_dict}

    def build_recursive_json(self, grand_child):
        # Recursive is one single table, so the build process is highly customized to that single table
        parent_queryset = eval(self.table_name.mother+'.objects.all()')
        project_values = parent_queryset.values("project_name", "id")

        all_childs = {}
        map_childs = {}
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
                    # TODO: IMPORTANT! Check which result is right. Maybe all three cases in one Filter?
                    # grandchild_total = TblMeta.objects.filter(nmmetadomain__domain__project_id=project_id, nmmetadomain__domain__pid_id=child_id, nmmetadomain__domain__domain_name=grandchild_name).count()
                    grandchild_total = TblMeta.objects.filter(nmmetadomain__domain__project_id=project_id).filter(nmmetadomain__domain__pid_id=child_id).filter(nmmetadomain__domain__domain_name=grandchild_name).count()
                    if grandchild_total >= self.min_amount:
                        grandchild_json = {
                            'name': grandchild_name,
                            'total': grandchild_total,
                            # 'chosen': False,
                        }
                        grandchild_counter = grandchild_counter + 1
                        inner_grandchild.update({'I'+str(grandchild_counter): grandchild_json})

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
        return {'json': all_childs, 'total': child_counter, 'server': map_childs}

    def print_properties(self):
        print('* table_name: ', self.table_name)
        print('* filter_type: ', self.filter_type)
        print('* child_columns: ', self.child_columns)
        print('* query_paths: ', self.query_paths)
        print('* child: ', self.child)
