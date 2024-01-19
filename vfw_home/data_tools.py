# from typing import Literal
import json
from collections import Counter, defaultdict

import numpy as np
import pandas as pd
from django.core.exceptions import EmptyResultSet, FieldError
from django.db import connections
from django.db.models import Q
from django.utils import timezone

from heron.settings import MAX_SIZE_PREVIEW_PLOT
from vfw_home.models import Entries, Timeseries, Timeseries_1D, NmEntrygroups


def get_split_groups(IDs):
    """
    Retrieves the split datasets based on the given list of IDs.

    :param IDs: (list) A list of IDs representing the split datasets.
    :return: list: A list of dictionaries where the keys are group IDs and the values are lists of IDs belonging to each group.
    """
    split_datasets = (Entries.objects.filter(pk__in=IDs, nmentrygroups__group__type__name='Split dataset')
                      .values('id', 'nmentrygroups__group_id')
                      .order_by('nmentrygroups__group_id'))
    print('split_datasets 1: ', split_datasets)

    # put ids of a all parts of a split dataset in one list (with their group id as key)
    grouped_dict = defaultdict(list)
    for i in split_datasets:
        grouped_dict[i['nmentrygroups__group_id']].append(i['id'])

    return grouped_dict


def get_accessible_data(request: object, requested_ids: list) -> (list, list):
    """
    Use request object to check if user has read access to a list of data (entries_id). Output is a list with
    accessible data and a second list with inaccessible data.

    :param request:
    :param requested_ids:
    :return: accessible_ids, error_ids
    """
    try:
        if isinstance(requested_ids, int):
            requested_ids = [requested_ids]
        elif isinstance(requested_ids, str):
            try:
                requested_ids = [int(requested_ids)]
            except ValueError as e:
                requested_ids = [int(r_id) for r_id in requested_ids[1:-1].split(',')]
        elif isinstance(requested_ids, list) and isinstance(requested_ids[0], str):
            requested_ids = [int(r_id) for r_id in requested_ids[0].split(',')]

        # first get datasets that are open for everyone and without embargo or expired embargo
        accessible_data = list(Entries.objects.values_list('id', flat=True)
                               .filter(pk__in=requested_ids)
                               .filter(Q(embargo=False) |
                                       Q(embargo=True, embargo_end__lt=timezone.now())))

        # check if the user wanted more and is authenticated. If yes check if user has access and get the rest
        if len(requested_ids) > len(accessible_data) and request.user.is_authenticated:
            accessible_embargo_datasets = list(set(requested_ids) & set(request.session['datasets']))  # intersect sets
            accessible_data.extend(accessible_embargo_datasets)
        # check if there is still data not accessible and create error for these
        error_list = list(set(requested_ids) - set(accessible_data))
        return {'open': accessible_data, 'blocked': error_list}
    except Exception as e:
        print('Error in data_tools.get_accessible_data: ', e)

def collect_selection(request, requested_id, startdate='', enddate=''):
    """
    function distinguishes only between default user (non-embargo data) and rest (+user embargo data)
    :param requested_id:
    :param startdate: string
    :param enddate: string
    :return:
    """
    dataset_dict = {}
    error_dict = {}
    group_dict = {'is_group': False, 'type': 'mixed', 'name': 'group', 'dbIDs': [], 'orgIDs': [], 'uuIDs': [],
                  'group_IDs': [], 'is_split': [], 'split_members': []}
    name_group = {'group_titles': set(), 'var_names': [], 'type_names': [], 'geom_type': [], 'coords': [],
                  'mixed_vars': True}

    # if min_time != 0:
    #     work_query = work_query + 'AND tbl_data.tstamp > ' + str(min_time)
    # if max_time != 0:
    #     work_query = work_query + 'AND tbl_data.tstamp < ' + str(max_time)
    # from_var = 'public.tbl_data'
    # where_var = 'tbl_data.meta_id = ' + str(requested_id)

    accessible_data = get_accessible_data(request, requested_id)
    error_ids = accessible_data['blocked']
    accessible_ids = accessible_data['open']

    # TDOO: The results are all returned twice. Maybe because of split datasets?
    # Fix this somehow!
    result_dataset = NmEntrygroups.objects. \
        values('entry__id', 'entry__uuid', 'entry__variable__name', 'entry__variable__symbol',
               'entry__variable__unit__symbol', 'entry__datasource__datatype__name', 'group__title',
               'group_id', 'entry__location', 'entry__geom', 'group__type__name').filter(pk__in=accessible_ids)  # .distinct()

    # collect split members
    # print('++++ split_datasets: ', split_datasets)
    # split_datasets = get_split_groups(accessible_ids)
    split_datasets_db = (Entries.objects.filter(pk__in=accessible_ids, nmentrygroups__group__type__name='Split dataset')
                      .values('id', 'nmentrygroups__group_id')
                      .order_by('nmentrygroups__group_id'))
    split_datasets = {str(data['id']): data['nmentrygroups__group_id'] for data in split_datasets_db}

    # result = {str(item['nmentrygroups__group_id']): [item['id'] for item in split_datasets if
    #                                                  item['nmentrygroups__group_id'] == item[
    #                                                      'nmentrygroups__group_id']]}
    # print('split_dataset: ', split_datasets)

    if len(error_ids) > 0:
        error_dict = {'message': 'no access', 'id': error_ids}

    for dataset in result_dataset:
        dataset_id = 'db' + str(dataset['entry__id'])
        # tried to use an object to build dataset_dict more easily, but using object is too cumbersome
        if dataset_id in dataset_dict:
            dataset_dict[dataset_id]['DBgroup'].add(dataset['group__title'])
            dataset_dict[dataset_id]['DBgroupID'].add(dataset['group_id'])
            dataset_dict[dataset_id]['groupTypeName'].add(
                dataset['groupTypeName'] if 'groupTypeName' in dataset else "")
            dataset_dict[dataset_id]['split_members'].append(
                dataset_id if dataset['group__type__name'].find('Split dataset') else '',)
            # dataset_dict[dataset_id]['split_members'].append(
            #     split_datasets[dataset['group_id']] if dataset['group__type__name'].find('Split dataset') else None)
        else:
            try:
                # if dataset['group__type__name'].find('Split dataset'):
                    # print('is a split dataset')
                    # print("is_split: dataset['group_id']: ", True)
                    # print("split_group: dataset['group_id']: ", dataset['group_id'])
                    # print("split_members: dataset['group_id']: ", dataset_id)
                # else:
                    # print('is not a split dataset: ', False, 0, [])

                dataset_dict.update({dataset_id: {'name': dataset['entry__variable__name'],
                                              'abbr': dataset['entry__variable__symbol'],
                                              'unit': dataset['entry__variable__unit__symbol'],
                                              'is_split': True
                                              if dataset['group__type__name'].find('Split dataset') else None,
                                              'split_group': dataset['group_id']
                                              if dataset['group__type__name'].find('Split dataset') else 0,
                                              'split_members': [dataset_id]
                                              if dataset['group__type__name'].find('Split dataset') else [],
                                              'type': dataset['entry__datasource__datatype__name'],
                                              'source': 'db',
                                              'dbID': dataset['entry__id'],
                                              'uuID': dataset['entry__uuid'],
                                              'orgID': dataset_id,
                                              'start': startdate,
                                              'end': enddate,
                                              'inputs': [],
                                              'outputs': dataset['entry__datasource__datatype__name'],
                                              'DBgroup': {dataset['group__title']},
                                              'DBgroupID': {dataset['group_id']},  # looks like this is groupID and member ID. Is this helpful?
                                              'groupTypeName': {dataset['group__type__name']},
                                              # 'geom': dataset['entry__geom'].json,
                                              'location': dataset['entry__location'].json
                                              }
                                 })
            except Exception as e:
                print('error: ', e)
            # print(' - - -  -')
        # TODO: This should be done in the same loop together with dataset_dict.update(), but because of the wrong
        #  behaviour of '.distinct()' This is done in a seperate loop
        # group_dict['dbIDs'].append(dataset['entry__id'])
        # group_dict['orgIDs'].append('db' + str(dataset['entry__id']))
        # group_dict['uuIDs'].append(dataset['entry__uuid'])
        # # summarize possible attributes to name a group
        # name_group['group_titles'].append(dataset['group__title'])  # #1
        # name_group['var_names'].append(dataset['entry__variable__name'])  # #2
        # name_group['type_names'].append(dataset['entry__datasource__datatype__name'])  # #3
        # # name_group['geom'].append(dataset['entry__geom'])  # #4
        # name_group['geom_type'].append(dataset['entry__location'].geom_type)  # #4
        # name_group['coords'].append(dataset['entry__location'].coords)  # #5

    # TODO: This should be done in the same loop together with dataset_dict.update(), but because of the wrong
    #  behaviour of '.distinct()' This is done in a seperate loop
    for k, v in dataset_dict.items():
        group_dict['dbIDs'].append(v['dbID'])
        group_dict['orgIDs'].append(k)
        group_dict['uuIDs'].append(v['uuID'])
        # summarize possible attributes to name a group
        name_group['group_titles'].update(v['DBgroup'])  # #1
        name_group['var_names'].append(v['name'])  # #2
        name_group['type_names'].append(v['type'])  # #3
        # name_group['geom'].append(dataset['entry__geom'])  # #4
        name_group['geom_type'].append(json.loads(v['location'])['type'])  # #4
        name_group['coords'].append(json.loads(v['location'])['coordinates'])  # #5

    # Set the name of the group
    if len(accessible_ids) > 1:
        group_dict['is_group'] = True

        if Counter(name_group['var_names']).most_common(1)[0][1] == len(accessible_ids):
            name_group['mixed_vars'] = False
            # if all the fields 'group_titles', 'var_names' or 'type_names' are identical, then use it for groupname
        for attr in name_group.keys():
            # TODO: Poor function/design of object so we have to skip for certain values. Improve the function/object
            if isinstance(name_group[attr], set):
                name_group[attr] = list(name_group[attr])

            if attr == 'coords' or attr == 'mixed_vars':
                continue

            if Counter(name_group[attr]).most_common(1)[0][1] == len(accessible_ids) \
                and name_group[attr][0] is not None:
                group_dict['name'] += name_group[attr][0] + ' '
                # if all datasets have the same datatype use this type as group type
                if attr == 'type_names':
                    group_dict['type'] = name_group[attr][0]

        # Now add the group name to the group members
        for dataset, values in dataset_dict.items():
            dataset_dict[dataset]['groupTypeName'] = list(dataset_dict[dataset]['groupTypeName'])
            dataset_dict[dataset]['DBgroup'] = list(dataset_dict[dataset]['DBgroup'])
            dataset_dict[dataset]['DBgroupID'] = list(dataset_dict[dataset]['DBgroupID'])
            dataset_dict[dataset]['group'] = group_dict['name']
            dataset_dict[dataset]['type'] = group_dict['type']
            # dataset_dict[dataset]['members'] = group_dict['type']

    else:
        # make sure there is no set in the dataset left (set/JSON conflict)
        for dataset_name, dataset in dataset_dict.items():
            for attr, values in dataset_dict[dataset_name].items():
                if isinstance(values, set):
                    dataset_dict[dataset_name][attr] = list(values)


    # TODO: Need timestamp in name to see if different selection
    return {'data': dataset_dict, 'error': error_dict, 'group': {group_dict['name']: group_dict}}


def __get_timescale(df, ID=None):
    """
    Get a dataframe with a timestamp ('tstmp'), iterate over the first 11 values (or less for shorter datasets)
    and return the smallest time difference.

    :param df: pandas dataframe
    :return: pandas timedelta
    """

    def __timescale_from_data(df):
        stepsize = []
        steps = 1
        checklength = 11

        if df.shape[0] <= checklength + 1:
            checklength = df.shape[0] - 1

        if 'tstamp' in df:
            relcol = df['tstamp']
        elif df.index.name == 'tstamp':
            relcol = df.index

        while steps < checklength:
            stepsize.append(relcol[steps + 1] - relcol[steps])
            steps += 1
        return min(stepsize)

    if ID:
        timescale = Entries.objects.filter(id=ID).values_list('datasource__temporal_scale__resolution')[0][0]
        if timescale:
            return pd.to_timedelta(timescale)
        else:
            return __timescale_from_data(df)
    else:
        return __timescale_from_data(df)


# TODO: In Python > 3.7 use Literal
# def is_data_short(ID: int, source: Literal['db', 'wps']):
def is_data_short(ID: int, source: str, date: list):
    """
    Get ID of a dataset, check the length of the dataset and return boolean if dataset is short (<= 50 000 values) or
    too long to plot completly.

    :param ID: integer
    :param source: string
    :param date: list
    :return: boolean
    """
    if source == 'db':
        datapath = Entries.objects.filter(id=ID).values_list('datasource__path', flat=True)[0]

    if datapath is None:
        return {'error': 'Dataset has no datasource__path.'}
    query_path = {'{0}'.format(datapath): ID}

    if date and date[0]:
        query_path[datapath + '__tstamp__gte'] = date[0]
        query_path[datapath + '__tstamp__lte'] = date[1]

    # TODO: Think about using the following queryset instead of creating it several times per plot
    datalength = Entries.objects.filter(**query_path).count()

    if datalength == 0:  # if not qs.exists():
        print('Problems with query_path: ', query_path)
        raise EmptyResultSet('Got no data in data_tools.is_data_short for id={}'.format(ID))

    if datalength <= MAX_SIZE_PREVIEW_PLOT:
        full = True
    else:
        full = False
    return full


def __unify_dataframe(data):
    """
    Check format of dataframe. When one value in data column it's the same as timeseries-1d, so just convert array to
    number and rename 'data' column to 'value'.

    :param dict (df, bool(reduced)):
    :return: dict (df, bool(reduced), str(data_format))
    """
    data['data_format'] = '1D'
    if 'data' in data['df'].columns and not 'value' in data['df'].columns:
        data['df'].rename(columns={'data': 'value'}, inplace=True, errors="raise")
    elif 'data' in data['df'].columns and 'value' in data['df'].columns:
        print('Error while renaming dataset. Cannot rename to already existing column.')

    # if len(data['df']['data'][0]) == 1:
    #     pass
    # df['value'] = df['data'].str.get(0)
    # df.drop(columns=['data'], inplace=True)
    if len(data['df']['value'][0]) == 3:
        new_df = pd.DataFrame.from_dict(dict(zip(data['df']['value'].index, data['df']['value'].values))).transpose()
        data['df']['y1'] = new_df[0]
        data['df']['y2'] = new_df[1]
        data['df']['y3'] = new_df[2]
        data['data_format'] = '3D'
    elif len(data['df']['value'][0]) != 1 or len(data['df']['value'][0]) != 3:
        print('Dataset is length is other then expected. Cannot plot timeseries data length ',
              len(data['df']['value'][0]))

    return data


def DB_load_data(ID: int, date: list, full_res: bool):
    """
    Load data from database and return a dict with data, pandas df and axis. When full resolution == False limit length
    of result according to settings.MAX_SIZE_PREVIEW_PLOT

    :param ID: integer
    :param date: list
    :param full_res: boolean
    :return: dict - {df, axis, scale, has_preci, dataformat}
    """
    lookup_arguments = {'entry_id': ID}
    if date and date[0]:
        lookup_arguments['tstamp__gte'] = date[0]
        lookup_arguments['tstamp__lte'] = date[1]

    # datatable = Entries.objects.filter(id=ID).values_list('datasource__datatype__name', flat=True)[0]
    datatable = Entries.objects.filter(id=ID).values_list('datasource__path', flat=True)[0]

    if datatable == 'timeseries_1d':
        # request data with django ORM
        qs = Timeseries_1D.objects.filter(**lookup_arguments).values('tstamp', 'value', 'precision')

        data = __reduce_dataset(qs, full_res)
        timescale = __get_timescale(data['df'], ID)
        precision = __has_precision(data['df'])
        return {'df': data['df'], 'scale': timescale, 'has_preci': precision, 'data_format': datatable}

    elif datatable == 'timeseries':

        try:
            qs = Timeseries.objects.filter(**lookup_arguments).values('tstamp', 'value', 'precision')
        except FieldError as e:
            # TODO: check which database entries use 'data' and which 'value', adapt plot functions accordingly
            qs = Timeseries.objects.filter(**lookup_arguments).values('tstamp', 'data', 'precision')
            #
            print('\033[31mWarning! Unusual field in "timeseries" for ID:\033[0m', ID,
                  '\033[31mUsed "data" instead of "value". Python message: \033[0m', e)

        data = __reduce_dataset(qs, full_res)

        data = __unify_dataframe(data)

        timescale = __get_timescale(data['df'], ID)

        precision = __has_precision(data['df'])

        return {'df': data['df'], 'scale': timescale, 'has_preci': precision, 'data_format': data['data_format']}

    else:
        print('*** CANNOT LOAD YOUR \'{0}\' DATA. PLEASE IMPLEMENT OTHER DATATYPES, TOO! ***'.format(datatable))


def __has_precision(df):
    """
    Check if dataset has any precision values.

    :param df: pandas dataframe
    :return: bool
    """
    precision = False
    if 'precision' in df.columns:
        if not df['precision'].isnull().values.any():
            precision = True
    return precision


def __reduce_dataset(qs: object, full_res: bool):
    """
    Reduce length of dataset to length given in 'settings.MAX_SIZE_PREVIEW_PLOT' to speed up loading time of preview.

    :param qs: data as django queryset or pandas dataframe
    :param full_res: bool
    :return: dict (pandas dataframe, bool(reduced))
    """
    reduced = False
    if isinstance(qs, pd.DataFrame):
        if full_res:
            df = qs
        else:
            df = (qs.tail(MAX_SIZE_PREVIEW_PLOT)).copy()
            reduced = True
    else:
        if full_res:
            df = pd.DataFrame(list(qs))
        else:
            qs_length = qs.count()
            df = pd.DataFrame(list(qs[qs_length - MAX_SIZE_PREVIEW_PLOT:qs_length]))
            reduced = True
    return {'df': df, 'reduced': reduced}


def __get_axis_limits(plot_data):
    """
    Take a dictionary with a dataframe, check if data has precision and set the limits of the axis accordingly.

    :param plot_data: dict - {'df'}
    :return: dict {'df', 'axis'}
    """
    df = plot_data['df']

    if 'precision' in df.columns and not df['precision'].isnull().values.any():
        axis = {'ymin': (df['value'] - df['precision']).min(),
                'ymax': (df['value'] + df['precision']).max()}
    elif 'precavg' in df.columns:
        # y is for the main plot -> min and  max of the day of the day,
        # y2 for the secondary plot with min and max in each group for each day
        axis = {'ymin': df['min'].min, 'ymax': df['max'].max,
                'y2min': df['precmin'].min, 'y2max': df['precmax'].max}
        # axis = {'y1min': min(result[2]), 'y1max': max(result[3]), 'y2min': min(result[4]), 'y2max': max(result[4])}
    else:
        if '3D' in plot_data['data_format']:
            axis = {'y1min': df['y1'].min(), 'y1max': df['y1'].max(),
                    'y2min': df['y2'].min(), 'y2max': df['y2'].max(),
                    'y3min': df['y3'].min(), 'y3max': df['y3'].max()}
        elif 'value' in df.columns:
            axis = {'ymin': df['value'].min(), 'ymax': df['value'].max()}
        elif 'data' in df.columns:
            axis = {'ymin': df['data'].min(), 'ymax': df['data'].max()}

    plot_data['axis'] = axis
    return plot_data


def DB_load_data_avg(ID: int, scale='day'):
    """

    :param ID: Entry ID
    :param scale:
    :return:
    """
    datatable = Entries.objects.filter(id=ID).values_list('datasource__datatype__name', flat=True)[0]
    if datatable == 'timeseries':
        # TODO: Use django ORM instead of pure sql
        # connect to database and fetch day(x), daily average, daily min, daily max, # of daily values
        cursor = connections['default'].cursor()
        # noinspection SqlResolve
        cursor.execute("SELECT date_trunc('{2}', tstamp) as date, "
                       "avg(value), min(value), max(value), count(*), "
                       "avg(precision) as prec_avg, min(precision) as prec_min, max(precision) as prec_max "
                       "FROM {0} "
                       "WHERE entry_id = {1} "
                       "GROUP BY date_trunc('{2}', tstamp)"
                       "ORDER BY date ASC;".format(datatable, ID, scale))
        dbresult = cursor.fetchall()
        cursor.close()
        result = list(zip(*dbresult))

        df = pd.DataFrame(data={'tstamp': result[0], 'avg': result[1], 'min': result[2], 'max': result[3],
                                'count': result[4], 'precavg': result[5], 'precmin': result[6], 'precmax': result[7]})
        # try to get timescale from database. If not available get it from dataset
        timescale = Entries.objects.filter(id=ID).values_list('datasource__temporal_scale__resolution')[0][0]
        if timescale:
            timescale = pd.to_timedelta(timescale)
        else:
            timescale = __get_timescale(df)

        precision = False if df['precavg'].isnull().values.any() else True

        return {'data': df, 'scale': timescale, 'has_preci': precision}
    else:
        print('*** PLEASE IMPLEMENT OTHER DATATYPES, TOO! ***')


def DB_load_directiondata(ID: int, ti: str, date: list, full_res: bool):
    """
    Load data for rose plot in ten degree bins from database.

    :param ID:
    :param ti:
    :param date:
    :param full_res:
    :return:
    """
    # TODO: Use django ORM instead of pure sql
    # TODO: if iwg is interested in it: Check number of time intervals.
    #  If this number is lower then 100 a smaller interval is used.
    datestring = ' '
    if date:
        datestring = "AND tstamp >= '{0}'::timestamp AND tstamp < '{1}'::timestamp ".format(date[0], date[1])

    datatable = Entries.objects.filter(id=ID).values_list('datasource__datatype__name', flat=True)[0]
    cursor = connections['default'].cursor()

    # adjust number of time frames according to the selected time frame
    date_opt = ['year', 'month', 'week', 'day']
    cursor.execute("SELECT date_trunc('{0}', tstamp)::date as date "
                   "FROM {2} "
                   "WHERE entry_id = {1} {3}"
                   "GROUP BY date_trunc('{0}', tstamp);".format(ti, ID, datatable, datestring))
    data_length = len(cursor.fetchall())
    if data_length < 100 and date_opt.index(ti) < len(date_opt):
        ti = date_opt[date_opt.index(ti) + 1]
    elif data_length > 1500 and date_opt.index(ti) > 0:
        ti = date_opt[date_opt.index(ti) - 1]

    # create 36 groups with group 1 from 355-5 degree and group 36 from 345-355 degree
    # TODO: check if this assumption above for the direction in now (that it is implemented with pandas) is still valid
    sum_string = ""
    for i in range(1, 36):
        sum_string += "count(*) FILTER (WHERE trunc(((data[1])+5)/10)::double precision = %i ) as b%i," % (i, i)

    cursor.execute("SELECT date_trunc('{0}', tstamp)::date as date, count(*), "
                   "count(*) FILTER (WHERE trunc(((data[1])+5)/10)::double precision = 0 "
                   "or trunc(((data[1])+5)/10)::double precision = 36) as b0, {1} "
                   "FROM {3} "
                   "WHERE entry_id = {2} {4}"
                   "GROUP BY date_trunc('{0}', tstamp);".format(ti, sum_string[:-1], ID, datatable, datestring))

    dbresult = cursor.fetchall()
    cursor.close()

    index = ['tstamp', 'sum'] + list(map(str, range(0, 36)))

    return pd.DataFrame(dbresult, columns=index), ti


def find_data_gaps(db_data: object):
    """
    Fill gaps in datasets and prepare for plot

    :param db_data: dict - dictionary with pandas dataframe 'df', 'has_preci' and 'scale'
    :return:
    """
    # use first five time steps to estimate resolution/step size of data
    scale = db_data['scale']
    df = db_data['df']
    missing_data = {}

    # check if data has a scaling
    if not scale:
        scale = __get_scaling(df)

    # check if data is continuous. If not write position of missing values in noDataPos
    noDataPos = __get_gap_position(df, scale, 'tstamp')
    # check if dataset has values for precision
    nan_in_data = False
    # To get a discontinuous line add 'nan' when a time step is missing.
    if len(noDataPos) > 0:
        nan_in_data = True
        defect_x = []
        defect_y = []
        # if 'precision' in df.columns and df['precision'].sum() > 0:  # if preview with average, min, max  values
        if 'avg' in df.columns:  # if dataset with average, min, max  values
            for pos in noDataPos[::-1]:
                # TODO: change this code to pandas df.
                print('TODO: change this code to pandas df.')
                db_data['data'][0] = db_data['data'][0][: pos + 1] + \
                                     (db_data['data'][0][pos] + scale,
                                      db_data['data'][0][pos + 1] - scale,) + \
                                     db_data['data'][0][pos + 1:]
                db_data['data'][1] = db_data['data'][1][: pos + 1] + (float('nan'), float('nan'),) + \
                                     db_data['data'][1][pos + 1:]
                bandbef = (db_data['data'][2][pos] + db_data['data'][3][pos]) / 2
                bandaft = (db_data['data'][2][pos + 1] + db_data['data'][3][pos + 1]) / 2
                db_data['data'][2] = db_data['data'][2][: pos + 1] + (bandbef, bandaft,) + db_data['data'][2][
                                                                                           pos + 1:]
                db_data['data'][3] = db_data['data'][3][: pos + 1] + (bandbef, bandaft,) + db_data['data'][3][
                                                                                           pos + 1:]
                db_data['data'][4] = db_data['data'][4][: pos + 1] + (0, 0,) + db_data['data'][4][pos + 1:]
                # white_line = white_line[: pos + 1] + (bandbef, bandaft,) + white_line[pos + 1:]
                defect_x.extend([db_data['data'][0][pos] - scale, db_data['data'][0][pos],
                                 db_data['data'][0][pos + 3], db_data['data'][0][pos] + scale])
                defect_y.extend([float('nan'), db_data['data'][1][pos],
                                 db_data['data'][1][pos + 3], float('nan'), ])
            source = pd.DataFrame({'date': db_data['data'][0], 'y': db_data['data'][1],
                                   'ymin': db_data['data'][2], 'ymax': db_data['data'][3],
                                   'count': db_data['data'][4]})
            missing_data = pd.DataFrame({'tstamp': defect_x, 'value': defect_y})
        else:  # if full dataset, without average, min, max values
            # copy random rows which happen to be the first two
            empty_rows = df.loc[1:2].copy()
            # set all columns except tstamp to nan
            empty_rows.loc[:, empty_rows.columns != 'tstamp'] = float('nan')
            for pos in noDataPos[::-1]:
                # set correct tstamp to new rows
                empty_rows['tstamp'] = df['tstamp'][pos] + scale, df['tstamp'][pos + 1] - scale
                # insert new rows with float index positions
                df.loc[pos + 0.3] = empty_rows.loc[1]
                # df.loc[pos+0.3] = df['tstamp'][pos] + scale, float('nan'), float('nan')
                df.loc[pos + 0.6] = empty_rows.loc[2]
                # df.loc[pos+0.6] = df['tstamp'][pos + 1] - scale, float('nan'), float('nan')
                defect_x.extend([df['tstamp'][pos] - scale, df['tstamp'][pos],
                                 df['tstamp'][pos + 1], df['tstamp'][pos + 1] + scale])
                if db_data['data_format'] == '3D':
                    defect_y.extend([float('nan'), float('nan'), float('nan'), float('nan'), ])
                elif 'value' in df.columns:
                    defect_y.extend([float('nan'), df['value'][pos], df['value'][pos + 1], float('nan'), ])
                elif 'data' in df.columns:
                    defect_y.extend([float('nan'), df['data'][pos], df['data'][pos + 1], float('nan'), ])
            # reset the index to integer
            df = df.sort_index().reset_index(drop=True)
            missing_data = pd.DataFrame({'tstamp': defect_x, 'value': defect_y})

    return {'df': df, 'scale': scale, 'nan_in_data': nan_in_data, 'data_format': db_data['data_format'],
            'missing_data': missing_data, 'has_preci': db_data['has_preci']}


def __get_scaling(df):
    """
    Make a list of the distance between the first ten datasets and return te smallest difference as scale.

    :param df: pandas dataframe
    :return:
    """
    scalelist = []

    testlength = df.shape[0] if df.shape[0] <= 10 else 10

    for row in range(1, testlength):
        scalelist.append(df['tstamp'][row] - df['tstamp'][row - 1])
    return min(scalelist)


def __get_gap_position(df, scale, index):
    """
    Iterate over a dataset and find all positions where the distance between two rows is greater than the given scale.

    :param df:
    :param scale:
    :param index: string - name of the column of the dataframe that is to be checked for gaps
    :return: list - row(s) before the gap(s)
    """
    val_beforeGap = []
    # use datetime as index and request the list of datetimes your looking for
    starttime = df[index][0]
    endtime = df.iloc[-1][index]
    # create a perfect DataFrame without gaps
    perfect_frame = pd.DataFrame(pd.date_range(start=starttime, end=endtime, freq=scale), columns=['tstamp'])
    # fill the empty frame without gaps with the data from original frame
    combined_dataframes = pd.merge(perfect_frame, df, how="outer", on="tstamp")
    # get rows without values
    try:
        empty_list = combined_dataframes.loc[combined_dataframes['value'].isna()].index.values
    except Exception as e:
        print('in get gab position: ', e)
        empty_list = combined_dataframes.loc[combined_dataframes['data'].isna()].index.values

    # use two shifted lists for comparison to find the first value of a gap
    shifted_list = np.append(0, empty_list)
    empty_list = np.append(empty_list, 0)
    diff_list = np.subtract(empty_list, shifted_list)

    # get indices of the perfect dataframe (without gaps)
    perfectframe_gaps = empty_list[diff_list > 1] - 1
    # get list of dates just before the gap
    gaps_date_list = combined_dataframes.loc[perfectframe_gaps.tolist()][index].tolist()

    # make a list of the indices (from the original dataframe) of the position before the gaps
    for i in gaps_date_list:
        val_beforeGapRow = df.loc[df[index] == i]
        val_beforeGap.append(val_beforeGapRow.index[0])

    return val_beforeGap


def precision_to_minmax(df):
    """
    Get a pandas dataframe with columns 'value', 'precision' or with 'avg', 'precmax', 'precavg' and calculate the min
    and max values for it, and add it to the dataframe.

    :param df: pandas dataframe 'value', 'precision' or with 'avg', 'precmax', 'precavg'
    :return: pandas dataframe + upper, lower, (upper_avg, lower_avg)
    """
    if 'value' in df.columns:
        df['upper'] = df['value'] + df['precision']
        df['lower'] = df['value'] - df['precision']
    elif 'avg' in df.columns:
        df['upper'] = df['avg'] + df['precmax']
        df['lower'] = df['acg'] - df['precmax']
        df['upper_avg'] = df['avg'] + df['precavg']
        df['lower_avg'] = df['acg'] - df['precavg']
    else:
        print('WARNING: there is a unknown dataset to convert precision in precision to minmax.')

    return df


class DataTypes:
    NUMPY_TYPES = ['array', '2darray', 'ndarray']
    SERIES_TYPES = ['iarray', 'varray', 'timeseries', 'vtimeseries']
    DF_TYPES = ['idataframe', 'vdataframe', 'time-dataframe', 'vtime-dataframe']
    SPECIALS = ['raster']

    def read_data(self, filepath: str, datatype: str):
        """
        Read data from disk. Format of the data on disk is defined by its datatype and automaticly selected..

        :param filepath:
        :param datatype:
        :return:
        """
        if datatype in self.NUMPY_TYPES:
            data = np.load(filepath + '.npz')
        elif datatype in self.SERIES_TYPES:
            data = pd.read_pickle(filepath + '.pkl')
        elif datatype in self.DF_TYPES:
            kwargs = dict()
            if 'time' in datatype:
                kwargs['parse_dates'] = [0]
            data = pd.read_csv(self.filepath + '.csv', index_col=[0], **kwargs)

            # if array-like, use only the first column
            # if datatype in self.SERIES_TYPES:
            #     data = data.iloc[:, 1].copy()

        elif datatype == 'raster':
            raise NotImplementedError('Raster files are not yet supported.')

        else:
            raise AttributeError("The datatype '%s' is not supported" % datatype)

        return data


class Button:

    def __init__(self, dbID, inputs, name, type, outputs, wps, source, status, dropBtn, group):
        self.group = group
        self.dropBtn = dropBtn
        self.status = status
        self.wps = wps
        self.outputs = outputs
        self.type = type
        self.name = name
        self.dbID = dbID
        self.inputs = inputs
        if self.wps:
            self.source = "wps"


def has_data(web_ID):
    """
    Check if the given web ID has data associated with it.

    :param web_ID: (int) The ID of the web entry.
    :return: bool: True if data is found for the web ID, False otherwise.
    """
    data_path = Entries.objects.filter(id=web_ID).values_list('datasource__path', flat=True)[0]
    if data_path is None:
        return False
    query_path = {'{0}'.format(data_path): web_ID}

    # TODO: Think about reusing the following queryset instead of creating it several times per plot
    data = Entries.objects.filter(**query_path).first()
    return data is not None
