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

import itertools
import json
import logging
import re
from pathlib import Path

import numpy as np
import pandas as pd
from django.core.cache import cache
from django.core.exceptions import FieldError
from django.core.paginator import PageNotAnInteger, EmptyPage
from django.utils import translation, timezone
from django.conf import settings

from heron.settings import DATA_DIR
from vfw_home.models import Entries

logger = logging.getLogger(__name__)

NUMPY_TYPES = ['array', '2darray', 'ndarray']
SERIES_TYPES = ['iarray', 'varray', 'timeseries', 'vtimeseries']
DF_TYPES = ['idataframe', 'vdataframe', 'time-dataframe', 'vtime-dataframe']
SPECIALS = ['raster']

regex_patterns = {
    'lat': re.compile(r'^(\+|-)?(?:90(?:(?:\.0{1,6})?)|(?:[0-9]|[1-8][0-9])(?:(?:\.[0-9]{1,6})?))$'),
    'lon': re.compile(
            r'^(\+|-)?(?:180(?:(?:\.0{1,6})?)|(?:[0-9]|[1-9][0-9]|1[0-7][0-9])(?:(?:\.[0-9]{1,6})?))$')
}

def is_coord(testString, latlon):
    if not regex_patterns[latlon].match(testString):
        raise ValueError()
    else:
        return True


def clean_database_name(name):
        """ Remove all non-alphanumeric characters """
        return re.sub(r'\W+', '', name)


def has_pending_embargo(embargo, embargo_end):
    """
    Send the information if there is an embargo and end date to check if embargo is still valid.
    Careful: Uses a naive local timezone.
    :param embargo: boolean
    :type embargo: boolean
    :param embargo_end: date
    :type embargo_end: datetime
    :return: boolean
    """
    pending = True
    if embargo is False or (embargo is True and timezone.make_naive(timezone.now()) > embargo_end):
        pending = False

    return pending


def human_readable_bool(bool_val):
    """
    Translate the boolean value to yes or no in the language of the user
    :param bool_val: bool
    :return: string
    """
    yesno = translation.gettext('No')
    if bool_val:
        yesno = translation.gettext('Yes')

    return yesno


def verbose_expiry_info(embargo, embargo_end):
    """
    Send the information if there is an embargo and end date to check if embargo is still valid.
    Careful: Uses a naive local timezone.
    :param embargo: boolean
    :type embargo: boolean
    :param embargo_end: date
    :type embargo_end: datetime
    :return: boolean
    :param embargo:
    :param embargo_end:
    :return: string
    """
    has_embargo = translation.gettext('Pending')
    if embargo is True and timezone.make_naive(timezone.now()) > embargo_end:
        has_embargo = translation.gettext('Expired')

    return has_embargo


def entry_has_data(entry: int) -> bool:
    """
    Check if Entries object has a datasource and consequently actual data.
    :param entry: entry id as integer
    :return: boolean
    """
    data = Entries.objects.values('datasource').filter(id=entry)
    if data[0]['datasource'] is not None:
        return True
    else:
        return False


def expressive_layer_name(user: object) -> str:
    """
    Build an expressive name for the layer o the geoserver
    :param user:
    :return: String of user id + username + "_layer"
    """
    namestring = str(user.id) + "_"
    if user.first_name and user.last_name:
        namestring += (user.first_name + "_" + user.last_name)
    else:
        namestring += user.username.translate({ord(c): "_" for c in "!@#$%^&*()[]{};:,./<>?|`=+\\"})

    return namestring + "_layer"


def get_cache(cache_obj: dict) -> tuple:
    """
    Check if redis is used to cache images, and if image 'name' is cached.
    Return state of redis, if image in cache and image if it is in cache.

    :param name:
    :return: returns two values. First cache object, second Bokeh image as dict of 'script' and 'div'
    """
    img = None
    try:
        img = cache_obj['redis'].get(cache_obj['name'])
    except Exception as err:
        cache_obj['use_redis'] = False
        logger.debug("Cannot connect to redis: {}".format(err))

    if cache_obj['use_redis']:
        if img is None:
            cache_obj['in_cache'] = False
        else:
            img = str(img, 'utf-8')
            cache_obj['in_cache'] = True
    return cache_obj, img


def get_dataset(s_id: int) -> object:
    """

    :param s_id: ID in metacatalob
    :return:
    """
    try:
        entry_type = Entries.objects.filter(pk=s_id).values_list('datasource__path', flat=True)[0]

        # build string of values for django query
        type_values = {'generic_1d_data': ['index', 'value', 'precision'],
                       'generic_2d_data': ['index', 'value1', 'value2', 'precision1', 'precision2'],
                       'generic_geometry_data': ['index', 'geom', 'srid'],
                       'geom_timeseries': ['tstamp', 'geom', 'srid'],
                        'timeseries': ['tstamp', 'data', 'precision'],
                       'timeseries_1d': ['tstamp', 'value', 'precision'],
                       'timeseries_2d': ['tstamp', 'value1', 'value2', 'precision1', 'precision2']}
        db_values = type_values[entry_type]

        query_values = []
        for value in db_values:
            query_values.append('{}__{}'.format(entry_type, value))

        query_filter = {entry_type: s_id}
        return Entries.objects.filter(**query_filter).values_list(*query_values)
    except Exception as e:
        # print('Unable to get_dataset in utitlites.py: ', e)
        logger.debug(f"Unable to get_dataset: {e}")


def get_paginatorpage(page, paginator):
    """
    Make sure the current page of a paginator exists

    :param page:
    :param paginator:
    :return:
    """
    try:
        entriespage = paginator.page(page)
    except PageNotAnInteger:
        entriespage = paginator.page(1)
    except EmptyPage:
        entriespage = paginator.page(paginator.num_pages)

    return entriespage


def read_data(uuid: str, datatype: str) -> object:
    """
    Read wps result from disk. When for datatype is only an empty string given the result is only the meta data.

    :param uuid:
    :param datatype:
    :return:
    """

    filepath = DATA_DIR
    if uuid[0:2] == './':
        uuid = uuid[2:]

    def load_meta(uuid: str, filepath):
        with open(Path(filepath) / (uuid + '.json'), 'r') as f:
            return json.load(f)

    def load_data(uuid: str, datatype: str, filepath):

        if datatype in NUMPY_TYPES:
            data = np.load(Path(filepath) / (uuid + '.npz'))

        elif datatype in SERIES_TYPES:
            data = pd.read_pickle(Path(filepath) / (uuid + '.pkl'))

        elif datatype in DF_TYPES:
            kwargs = dict()
            if 'time' in datatype:
                kwargs['parse_dates'] = [0]
            data = pd.read_csv(Path(filepath) / (uuid + '.csv'), index_col=[0], **kwargs)

            # if array-like, use only the first column
            if datatype in SERIES_TYPES:
                data = data.iloc[:, 1].copy()

        elif datatype == 'raster':
            raise NotImplementedError('Raster files are not yet supported.')

        else:
            raise AttributeError("The datatype '%s' is not supported" % datatype)

        return data

    if datatype:
        return load_data(uuid, datatype, filepath), load_meta(uuid, filepath)
    else:
        return load_meta(uuid, filepath)


def check_data_consistency(check_interval=60*60*24):
    """
    Get all Entries and check if every entry has a datasource associated, and if yes if there is also data
    for the respective ID at the datasource.
    'check_interval' sets how long the result is cached. This means, the database is checked on every restart of the
    project.
    :param check_interval: time in seconds until a new check of the database; default is once a day
    :return:
    """
    datapaths_in_use = Entries.objects.values_list('datasource__path', flat=True).distinct()
    datapaths = ['timeseries', 'timeseries_1d', 'timeseries_2d', 'geom_timeseries',
                 'generic_geometry_data',
                 'generic_2d_data', 'generic_1d_data']
    folders = list(itertools.filterfalse(lambda item: not item, set(datapaths_in_use)-set(datapaths)))

    all_Entries = Entries.objects.values_list('id', 'datasource__path')
    id_without_datasoure = []
    id_without_data = []
    id_wrong_table = []
    id_on_disk = []
    all_num = len(all_Entries)
    count = 0
    try:
        for i in all_Entries:
            test = False
            count += 1
            if not i[1]:
                id_without_datasoure.append(i[0])
            elif i[1] in folders:
                id_on_disk.append(i[0])
            else:
                query_path = {'{0}'.format(i[1]): i[0]}
                try:
                    test = Entries.objects.filter(**query_path).exists()
                except FieldError as e:
                    # print(f"\033[91mError: Got a new source for data storage (path: entry_ID {query_path})"
                    #       f" in vfw_home/utilities/check_data_consistency: {e}.\033[0m")
                    logger.debug(f"Got a new source for data storage (path: entry_ID {query_path}): {e}")

                if int(count/200) == count/200:
                    print(f'Check data consistency, did {i[0], test} - {str(int(int(count)/int(all_num)*100))}%')
                if not test:
                    id_without_data.append(i[0])
                    """ check if dataset is associated with wrong table """
                    for dp in datapaths:
                        new_query_path = {'{0}'.format(dp): i[0]}
                        inner_test = Entries.objects.filter(**new_query_path).exists()
                        if inner_test:
                            id_wrong_table.append((i[0], dp))
    except Exception as e:
        print('e: ', e)

    if len(id_without_datasoure) > 0:
        print(f'\033[93mWARNING: following IDs have no data source: {id_without_datasoure}\033[0m')
    if len(id_without_data) > 0:
        print(f'\033[93mWARNING: following IDs have no data: {id_without_data}\033[0m')
    if len(id_wrong_table) > 0:
        print(f'\033[91mERROR: following IDs are associated with the wrong table: {id_wrong_table}\033[0m')
    if len(id_on_disk) > 0:
        print(f'\033[93mWARNING: following IDs have data on disk that has to be handled: {id_on_disk}\033[0m')

    cache.set('ids_without_data', id_without_data + id_without_datasoure, check_interval)
    cache.set('ids_data_on_path', id_on_disk, check_interval)
    return id_without_data + id_without_datasoure


def clean_database_name(name = settings.DATABASES['default']['NAME']):
    
# Remove all non-alphanumeric characters
    return re.sub(r'\W+', '', name)
