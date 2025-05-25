# =================================================================
#
# Authors: Marcus Strobl <marcus.strobl@kit.edu>
# Contributors: Safa Bouguezzi <safa.bouguezzi@kit.edu>
#
# Copyright (c) 2024 Marcus Strobl
#
# Permission is hereby granted, free of charge, to any person
# obtaining a copy of this software and associated documentation
# files (the "Software"), to deal in the Software without
# restriction, including without limitation the rights to use,
# copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the
# Software is furnished to do so, subject to the following
# conditions:
#
# The above copyright notice and this permission notice shall be
# included in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES
# OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
# NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT
# HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY,
# WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
# FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR
# OTHER DEALINGS IN THE SOFTWARE.
#
# =================================================================

# from typing import Literal
import json
from collections import Counter, defaultdict
import logging
import numpy as np
import pandas as pd
from django.core.cache import cache
from django.core.exceptions import EmptyResultSet, FieldError
from django.db import connections
from django.db.models import Q
from django.utils import timezone
from django.http import HttpRequest

from heron.settings import MAX_SIZE_PREVIEW_PLOT
from vfw_home.models import Entries, Timeseries, Timeseries_1D, NmEntrygroups, Locations

logger = logging.getLogger(__name__)

def get_split_groups(IDs):
    """
    Retrieves the split datasets based on the given list of IDs.

    :param IDs: (list) A list of IDs representing the split datasets.
    :return: list: A list of dictionaries where the keys are group IDs and the values are lists of IDs belonging to each group.
    """
    split_datasets = (Entries.objects.filter(pk__in=IDs, nmentrygroups__group__type__name='Split dataset')
                      .values('id', 'nmentrygroups__group_id')
                      .order_by('nmentrygroups__group_id'))

    # put ids of a all parts of a split dataset in one list (with their group id as key)
    grouped_dict = defaultdict(list)
    for i in split_datasets:
        grouped_dict[i['nmentrygroups__group_id']].append(i['id'])

    return grouped_dict

def get_accessible_data(request: HttpRequest, requested_ids: list) -> (list, list):
    """
    Use request object to check if user has read access to a list of data (entries_id). Output is a list with
    accessible data and a second list with inaccessible data.
    This function is called when the user wants to pass data to the datastore, to create the data object for the client

    :param request:
    :param requested_ids:
    :return: accessible_ids, error_ids
    """
    try:
        if isinstance(requested_ids, int):
            requested_ids = [requested_ids]
        elif isinstance(requested_ids, str):
            try:
                requested_ids = [int(r_id) for r_id in requested_ids[2:].split(',')]

                # requested_ids = [int(requested_ids)]
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
    dataset_dict = {}  # collect here the info for all selected data sets to pass it to the client
    error_dict = {}
    group_dict = {'is_group': False, 'type': 'mixed', 'name': 'group', 'dbIDs': [], 'orgIDs': [], 'uuIDs': [],
                  'group_IDs': [], 'is_split': [], 'split_members': []}
    name_group = {'group_titles': set(), 'var_names': [], 'type_names': [], 'geom_type': [], 'coords': [],
                  'mixed_vars': True}

    accessible_data = get_accessible_data(request, requested_id)
    error_ids = accessible_data['blocked']
    accessible_ids = accessible_data['open']
    grouped_ids = list(NmEntrygroups.objects.values_list('entry__id', flat=True).filter(pk__in=accessible_ids))
    groupless_ids = list(set(grouped_ids).symmetric_difference(set(accessible_ids)))

    result_dataset_groups = (NmEntrygroups.objects
                             .values('entry__id', 'entry__uuid', 'entry__variable__name', 'entry__variable__symbol',
                                     'entry__variable__unit__symbol', 'entry__datasource__datatype__name',
                                     'group__title', 'group_id', 'group__type__name',
                                     'entry__datasource__spatial_scale__extent').filter(pk__in=grouped_ids))  # .distinct()

    # not all datasets have a group ID, and datasets without group ID are not in NmEntrygroups, so they have to be
    # taken from Entries.
    result_dataset = (Entries.objects
                      .values('id', 'uuid', 'variable__name', 'variable__symbol', 'variable__unit__symbol',
                              'datasource__datatype__name', 'datasource__spatial_scale__extent')
                      .filter(pk__in=groupless_ids))

    # Since the geom column is removed from entries, we have to get the geometry in a separate query
    result_geometries = (Locations.objects.values('id', 'point_location_st_asewkt', 'geom')
                         .filter(pk__in=accessible_ids))
    result_geometries_dict = {}
    for item in result_geometries:
        result_geometries_dict[f'db{item["id"]}'] = {'point_location_st_asewkt': item['point_location_st_asewkt'],
                                                     'geom': item['geom']}

    # collect split members
    split_datasets_db = (Entries.objects
                         .filter(pk__in=grouped_ids, nmentrygroups__group__type__name='Split dataset')
                         .values('id', 'nmentrygroups__group_id').order_by('nmentrygroups__group_id'))
    split_datasets = {str(data['id']): data['nmentrygroups__group_id'] for data in split_datasets_db}

    if len(error_ids) > 0:
        error_dict = {'message': 'no access', 'id': error_ids}

    """ Create Objects for ungrouped datasets """
    for dataset in result_dataset:
        dataset_id = 'db' + str(dataset['id'])
        try:
            # locations are differently stored in the database, so first get the right value for location
            data_location = {}
            data_location['type'] = result_geometries_dict[dataset_id]['geom'].geom_type
            data_location['coords'] = result_geometries_dict[dataset_id]['geom'].coords

            dataset_dict.update({dataset_id: {'name': dataset['variable__name'],
                                              'abbr': dataset['variable__symbol'],
                                              'unit': dataset['variable__unit__symbol'],
                                              'is_split': None,
                                              'split_group':  0,
                                              'split_members':  [],
                                              'type': dataset['datasource__datatype__name'],
                                              'source': 'db',
                                              'dbID': dataset['id'],
                                              'uuID': dataset['uuid'],
                                              'orgID': dataset_id,
                                              'start': startdate,
                                              'end': enddate,
                                              'inputs': [],
                                              'outputs': dataset['datasource__datatype__name'],
                                              'DBgroup': {},
                                              'DBgroupID': {},
                                              # looks like this is groupID and member ID. Is this helpful?
                                              'groupTypeName': {},
                                              'location': data_location
                                              }
                                 })
        except Exception as e:
            print('Unable to create your object: ', e)

    """ Create Objects for grouped datasets """
    for dataset in result_dataset_groups:
        dataset_id = 'db' + str(dataset['entry__id'])
        # tried to use an object to build dataset_dict more easily, but using object is too cumbersome
        if dataset_id in dataset_dict:
            dataset_dict[dataset_id]['DBgroup'].add(dataset['group__title'])
            dataset_dict[dataset_id]['DBgroupID'].add(dataset['group_id'])
            dataset_dict[dataset_id]['groupTypeName'].add(
                dataset['groupTypeName'] if 'groupTypeName' in dataset else "")
            dataset_dict[dataset_id]['split_members'].append(
                dataset_id if dataset['group__type__name'].find('Split dataset') else '',)
        else:
            try:
                data_location = {}
                data_location['type'] = result_geometries_dict[dataset_id]['geom'].geom_type
                data_location['coords'] = result_geometries_dict[dataset_id]['geom'].coords

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
                                                  'location': data_location
                                                  }
                                     })
            except Exception as e:
                print('Unable to create your object: ', e)

    for k, v in dataset_dict.items():
        group_dict['dbIDs'].append(v['dbID'])
        group_dict['orgIDs'].append(k)
        group_dict['uuIDs'].append(v['uuID'])
        # summarize possible attributes to name a group
        name_group['group_titles'].update(v['DBgroup'])  # #1
        name_group['var_names'].append(v['name'])  # #2
        name_group['type_names'].append(v['type'])  # #3
        name_group['geom_type'].append(v['location']['type'])  # #4
        name_group['coords'].append(v['location']['coords'])  # #5

    """ Set the name of the group """
    if len(grouped_ids) > 1:
        group_dict['is_group'] = True

        if Counter(name_group['var_names']).most_common(1)[0][1] == len(grouped_ids):
            name_group['mixed_vars'] = False
            # if all the fields 'group_titles', 'var_names' or 'type_names' are identical, then use it for groupname
        for attr in name_group.keys():
            if isinstance(name_group[attr], set):
                name_group[attr] = list(name_group[attr])

            if attr == 'coords' or attr == 'mixed_vars':
                continue

            if Counter(name_group[attr]).most_common(1)[0][1] == len(grouped_ids) \
                and name_group[attr][0] is not None:
                group_dict['name'] += name_group[attr][0] + ' '
                # if all datasets have the same datatype use this type as group type
                if attr == 'type_names':
                    group_dict['type'] = name_group[attr][0]

        """ Now add the group name to the group members """
        for dataset, values in dataset_dict.items():
            dataset_dict[dataset]['groupTypeName'] = list(dataset_dict[dataset]['groupTypeName'])
            dataset_dict[dataset]['DBgroup'] = list(dataset_dict[dataset]['DBgroup'])
            dataset_dict[dataset]['DBgroupID'] = list(dataset_dict[dataset]['DBgroupID'])
            dataset_dict[dataset]['group'] = group_dict['name']

    else:
        # make sure there is no set in the dataset left (set/JSON conflict)
        for dataset_name, dataset in dataset_dict.items():
            for attr, values in dataset_dict[dataset_name].items():
                if isinstance(values, set):
                    dataset_dict[dataset_name][attr] = list(values)

    return {'data': dataset_dict, 'error': error_dict, 'group': {group_dict['name']: group_dict}}


def DB_load_directiondata(ID: int, ti: str, date: list, full_res: bool):
    """
    Load data for rose plot in ten degree bins from database.

    :param ID:
    :param ti:
    :param date:
    :param full_res:
    :return:
    """
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


class DataTypes:
    """
    This is not used yet, but should be the accesspoint to define allowed datatypes and give a single access to read
    data from different types and sources.
    Format of the data on disk is defined by its datatype and automatically selected.

    :param filepath: The path to the data file.
    :type filepath: str
    :param datatype: The datatype of the data.
    :type datatype: str
    :return: The loaded data.
    """
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


def has_data(web_ID):
    """
    Check if the given web ID has data associated with it.

    :param web_ID: (int) The ID of the web entry.
    :return: bool: True if data is found for the web ID, False otherwise.
    """
    return web_ID not in cache.get('ids_without_data')

    data_path = Entries.objects.filter(id=web_ID).values_list('datasource__path', flat=True)[0]
    if data_path is None:
        return False
    query_path = {'{0}'.format(data_path): web_ID}

    try:
        data = Entries.objects.filter(**query_path).first()
    except FieldError as e:
        print('\033[33mhome.data_tools.has_data: Field das not exist:\033[0m ', e)
        logger.debug('Field Error in has_data: ', e)
    return data is not None
