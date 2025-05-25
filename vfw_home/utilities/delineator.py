import logging
import time

from django.contrib.gis.geos import Point
from django.db import connection
from vfw_home.models import merit_hydro_vect_level2, cat_pfaf_MERIT_Hydro_v07_Basins_v01, \
    riv_pfaf_MERIT_Hydro_v07_Basins_v01

logger = logging.getLogger(__name__)

"""
The data used by the delineation tool is from MERIT Hydro. In the following you find the
License Agreement

The MERIT Hydro is licensed under a Creative Commons "CC-BY-NC 4.0" or Open Data Commons "Open Database License (ODbL 1.0)".
(i.e. dual license, you can choose an appropriate license for you)

To view a copy of these license, please visit:
CC-BY-NC 4.0 license: Non-Commercial Use with less restriction.
ODbL 1.0 license: Commertial Use is OK, but the derived data based on MERIT Hydro should be made publicly available under the same ODbL license.
For example, if you create a flood hazard map using MERIT Hydro and you'd like to provide a COMMERCIAL service based on that, you have to make the hazard map PUBLICLY AVAILABLE under OdBL license.

Note that the above license terms are applied to the "derived data" based on MERIT Hydro, while they are not applied to "produced work / artwork" created with MERIT Hydro (such as figures in a journal paper). The users may have a copyright of the artwork and may assign any license, if when the produced work is not considered as "derived data".

By downloading and using the data the user agrees to the terms and conditions of the license. Notwithstanding this free license, we ask users to refrain from redistributing the data in whole in its original format on other websites without the explicit written permission from the authors.

MERIT Hydro is available for download at http://hydro.iis.u-tokyo.ac.jp/~yamadai/MERIT_Hydro/.
The copyright of MERIT Hydro is held by the developers, 2019, all rights reserved.
"""


def useSQLQuery(wkbquerystring):
    """
    Just a try-except block around a raw sql query
    :param wkbquerystring:
    :return:
    """
    try:
        with connection.cursor() as cursor:
            cursor.execute(wkbquerystring)
            row = cursor.fetchall()
    except Exception as e:
        print('e: ', e)
        row = [('error', e)]

    return row


def get_start_ID(coords, coordinates, id_range=None):

    # find detail catchment
    if id_range:
        level1_catchment = cat_pfaf_MERIT_Hydro_v07_Basins_v01.objects.filter(comid__range=id_range)

        try:
            catchment = level1_catchment.filter(geom__contains=coordinates)
        except Exception as e:
            print('e in catchment.filter: ', e)
            logger.error(f'unable to filter level1 catchment with coordinates {coordinates}')
            return {'error': e,
                    'vfw_message': f'unable to filter level1 catchment with coordinates {coordinates}'}

    if not catchment.exists():
        wkbquerystring = "SELECT ST_AsText(geom, 9) AS catchment " \
                         "FROM merit_hydro_vect_level2 WHERE ST_Contains(geom, " \
                         f"ST_Point({float(coords['lng'][0])}, {float(coords['lat'][0])}, 4326));"
        row = useSQLQuery(wkbquerystring)
        logger.error(f'No high resolution catchment at coordinates {coordinates}')
        return {'error': 'No high resolution catchment at click location.',
                'wkt': row[0][0]}

    return catchment.values()[0]['comid']


def get_coarse_catchment_id_range(coordinates):
    search_dist = 0.01

    # find coarse high level catchment for given coordinates
    level2_basin = merit_hydro_vect_level2.objects.filter(geom__contains=coordinates)

    if not level2_basin.exists():
        # Check if there is a catchment nearby
        try:
            level2_basin = merit_hydro_vect_level2.objects.filter(geom__dwithin=(coordinates, search_dist))
        except Exception as e:
            print('e: ', e)

        # if there is still no result, the return a warning
        if not level2_basin:
            print('nothing nearby, show error')
            logger.info('Something went wrong for delineation! Maybe secretGeoServer.txt is missing')
            return {'error': 'No catchment at click location.'}

    # level2_basin.objects.annotate(distance=Distance('point', coordinates)).order_by('distance')
    basin_id = level2_basin.values()[0]['basin']
    # range of ids to restrict search for data:
    return (basin_id * 1000000, (basin_id + 1) * 1000000 - 1)


def delineate(coords=None, terminal_comid=None, HIGH_RES=True, LOW_RES_THRESHOLD=50000, precise=False):
    """
    code is based on delineator-1.0 of https://github.com/mheberger/delineator
    Citation DOI: 10.5281/zenodo.7314287

    :param coords:
    :param terminal_comid: The ID of the clicked catchment where all the higher rivers flow in.
    :param HIGH_RES: boolean True for "high-resolution" mode or False for "low-resolution."
    :param LOW_RES_THRESHOLD: integer Threshold for watershed size in km². Above the script revert to low-resolution mode
    :param precise: boolean True for recalculation of catchment from clickpoint. False starts with the smallest catchment that includes the click point
    :return:
    """
    # code is based on delineator-1.0 of https://github.com/mheberger/delineator
    # Citation DOI: 10.5281/zenodo.7314287

    # Threshold for watershed size in km² above which the script will revert to low-resolution mode
    # (check uparea of river table)
    LOW_RES_THRESHOLD = 10000
    accuracy = 5  # 4 decimals ~= 10m; 6 decimals ~= 1m

    # If the requested watershed outlet is not inside a catchment, how far away
    # from the point should we look for the nearest catchment (in degrees)
    if coords is not None:
        crs = 'EPSG:4326'
        coordinates = Point(float(coords['lng'][0]), float(coords['lat'][0]), crs)
        id_range = get_coarse_catchment_id_range(coordinates)
        terminal_comid = get_start_ID(coords, coordinates, id_range)

    # starting from the catchment at the clickpoint, search for the connected rivers upstream
    comID_array = get_ID_array(terminal_comid)
    newcomID_tuple = tuple(*zip(*comID_array))

    if precise:
        if len(newcomID_tuple) > 1:
            # union catchments
            wkbquerystring = 'SELECT ST_AsText(' \
                             f'ST_Union(ARRAY(SELECT geom FROM cat_pfaf_merit_hydro_v07_basins_v01 WHERE comid in ' \
                             f'{newcomID_tuple})), ' \
                             f'{accuracy}) as catchment'
        else:
            wkbquerystring = f'SELECT ST_AsText(geom, {accuracy}) AS catchment ' \
                             f'FROM cat_pfaf_merit_hydro_v07_basins_v01 WHERE comid={terminal_comid};'
    else:
        # Some simplification of catchment might be necessary no to follow corners of every pixel.
        # Also the delineation is used in the url to allow sharing and bookmarking. Max length of URLs is 4096 chars, so
        # a the numbers of vertices has to estimated and the complexity has to be lowered.
        simplification = 0.01  # 0.01
        if len(comID_array) > 500:
            simplification = 0.05  # 0.01
        elif len(comID_array) > 3000:
            simplification = 0.1  # 0.01

        # create raw query. Small difference if the query is only for one catchment, or if several have to be unified
        if len(newcomID_tuple) > 1:
            # union catchments
            wkbquerystring = 'SELECT ST_AsText(' \
                             'ST_Simplify(' \
                             f'ST_Union(ARRAY(SELECT geom FROM cat_pfaf_merit_hydro_v07_basins_v01 WHERE comid in ' \
                             f'{newcomID_tuple})), ' \
                             f'{simplification}), ' \
                             f'{accuracy}) as catchment'
        else:
            wkbquerystring = f'SELECT ST_AsText(ST_Simplify(geom, {simplification}), {accuracy}) AS catchment ' \
                             f'FROM cat_pfaf_merit_hydro_v07_basins_v01 WHERE comid={terminal_comid};'

    row = useSQLQuery(wkbquerystring)

    return {'wkt': row[0][0]}


def get_ID_array(terminal_comid):
    """
    Retrieves an array of IDs following the rivers from the database using a recursive SQL query.

    :param: terminal_comid (int): The ID of the terminal comid to start the recursive query from.
    :return: list[int]: An array of comid values retrieved from the database.
    """
    return useSQLQuery('WITH RECURSIVE riv_tree (comid, nextdownid, level) AS ('
                       'SELECT comid, nextdownid, 1 AS level '
                       'FROM riv_pfaf_merit_hydro_v07_basins_v01 '
                       f'WHERE comid = {terminal_comid} '
                       'UNION ALL '
                       'SELECT r.comid, r.nextdownid, rt.level + 1 '
                       'FROM riv_tree rt '
                       'JOIN riv_pfaf_merit_hydro_v07_basins_v01 r ON rt.comid IN (r.nextdownid)'
                       ')'
                       'SELECT comid '
                       'FROM riv_tree;')


def get_unified_catchment(id_tuple, outputtype='ewkb'):
    query_string = (f'SELECT ST_AsEWKB(ST_Union(ARRAY('
                    f'SELECT geom FROM cat_pfaf_merit_hydro_v07_basins_v01 WHERE comid in {id_tuple}'
                    f'))) as catchment')

    row = useSQLQuery(query_string)
    return row
