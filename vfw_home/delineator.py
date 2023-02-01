import time

import numpy as np
import pandas as pd
from django.contrib.gis.gdal import DataSource

from django.contrib.gis.geos import Point
from django.db import connection
from vfw_home.models import merit_hydro_vect_level2, cat_pfaf_MERIT_Hydro_v07_Basins_v01, \
    riv_pfaf_MERIT_Hydro_v07_Basins_v01
from django.contrib.gis.measure import D

def delineate(coords, HIGH_RES=True, LOW_RES_THRESHOLD=50000, precise=False):
    """
    code is based on delineator-1.0 of https://github.com/mheberger/delineator
    Citation DOI: 10.5281/zenodo.7314287


    :param coords:
    :param HIGH_RES: boolean True for "high-resolution" mode or False for "low-resolution."
    :param LOW_RES_THRESHOLD: integer Threshold for watershed size in km². Above the script revert to low-resolution mode
    :param precise: boolean True for recalculation of catchment from clickpoint. False starts with the smallest catchment that includes the click point
    :return:
    """
    # code is based on delineator-1.0 of https://github.com/mheberger/delineator
    # Citation DOI: 10.5281/zenodo.7314287
    t0 = time.time()
    # Threshold for watershed size in km² above which the script will revert to
    # low-resolution mode (check uparea of river table)
    LOW_RES_THRESHOLD = 10000
    # If the requested watershed outlet is not inside a catchment, how far away
    # from the point should we look for the nearest catchment (in degrees)
    search_dist = 0.01
    def addnode(B, node):
        """"
        Recursive function to assemble the list of upstream unit catchments
        :param B: list
        :param node: integer
        """
        # first, append the node to the basin
        B.append(node)

        # next, check whether the fields up1, up2, up3, and up4 contain a node ID
        queryset_values = rivers_of_catchment.filter(comid=node).values_list('up1', 'up2', 'up3', 'up4')[0]
        for up in queryset_values:
            if up != 0:
                addnode(B, up)
            else:
                break

    def useSQLQuery(wkbquerystring):
        try:
            with connection.cursor() as cursor:
                cursor.execute(wkbquerystring)
                row = cursor.fetchall()
        except Exception as e:
            print('e: ', e)

        return row

    gages_df = pd.DataFrame(data=coords)
    if HIGH_RES:
        gages_df['lat_snap'] = np.nan
        gages_df['lng_snap'] = np.nan
        gages_df['snap_dist'] = 0

    print('1')
    crs = 'EPSG:4326'
    coordinates = Point(float(coords['lng'][0]), float(coords['lat'][0]), crs)
    coordinates = Point(10.042166, 48.311781, 'EPSG:4326')


    # find high level catchment
    level2_basin = merit_hydro_vect_level2.objects.filter(geom__contains=coordinates)
    print('coords: ', coords)
    print('coordinates: ', coordinates)

    if not level2_basin.exists():
        print('3')
        # Check if there is a catchment nearby
        # TODO: in case more than one catchment is in the result, sort, sort and use the closer one
        try:
            level2_basin = merit_hydro_vect_level2.objects.filter(geom__dwithin=(coordinates, search_dist))
            print('4 level2_basin: ', level2_basin)
        except Exception as e:
            print('e: ', e)


        # if there is still no result, the return a warning
        if not level2_basin:
            print('nothing nearby, show error')
            return {'error': 'No catchment at click location.'}
    print('5')

    # level2_basin.objects.annotate(distance=Distance('point', coordinates)).order_by('distance')
    level2_basin_id = level2_basin.values()[0]['id']
    basin_id = level2_basin.values()[0]['basin']
    print('basin id: ', basin_id)
    id_range = (basin_id*1000000, (basin_id+1)*1000000-1)

    # find detail catchment
    level1_catchment = cat_pfaf_MERIT_Hydro_v07_Basins_v01.objects.filter(comid__range=id_range)
    print('6')
    try:
        print('6a')
        catchment = level1_catchment.filter(geom__contains=coordinates)
        print('catchmetn: ', catchment)
        print('6b')
    except Exception as e:
        print('e: ', e)
    print('catchmetn: ', catchment.exists())
    print('6b')
    if not catchment.exists():
        print('does not exist')
        wkbquerystring = "SELECT ST_AsText(geom, 9) AS catchment " \
                         "FROM merit_hydro_vect_level2 WHERE ST_Contains(geom, " \
                         f"ST_Point({float(coords['lng'][0])}, {float(coords['lat'][0])}, 4326));"
        print('wkbquerystring: ', wkbquerystring)
        row = useSQLQuery(wkbquerystring)
        return {'error': 'No high resolution catchment at click location.',
                'wkt': row[0][0]}

    print('7')
    terminal_comid = catchment.values()[0]['comid']
    print('8')

    try:
        rivers_of_catchment = riv_pfaf_MERIT_Hydro_v07_Basins_v01.objects.filter(comid__range=id_range)
        river_comid = rivers_of_catchment.filter(comid=terminal_comid)
    except Exception as e:
        print('e in river: ', e)
        return {'error': 'There is a problem with your river layer.'}

    small_uparea = river_comid.values()[0]['uparea']  # might be used to check which resolution is used nexed

    # Let B be the list of unit catchments_gdf that are in the basin
    B = []
    t1 = time.time()
    # addnode(B, terminal_comid)

    t2 = time.time()

    recursive_query_string = 'WITH RECURSIVE riv_tree (comid, nextdownid, level) AS (' \
                             'SELECT comid, nextdownid, 1 AS level ' \
                             'FROM riv_pfaf_merit_hydro_v07_basins_v01 ' \
                             f'WHERE comid = {terminal_comid} ' \
                             'UNION ALL ' \
                             'SELECT r.comid, r.nextdownid, rt.level + 1 ' \
                             'FROM riv_tree rt ' \
                             'JOIN riv_pfaf_merit_hydro_v07_basins_v01 r ON rt.comid IN (r.nextdownid)' \
                             ')' \
                             'SELECT comid ' \
                             'FROM riv_tree;'

    comID_array = useSQLQuery(recursive_query_string)
    t2b = time.time()

    selectstring = ""
    singleselectstring = "SELECT ST_AsText(geom, 8) AS catchment " \
                         f"FROM cat_pfaf_merit_hydro_v07_basins_v01 WHERE comid={terminal_comid}"
    # union catchments
    for i in comID_array:
        # create query
        selectstring += "(SELECT geom FROM cat_pfaf_merit_hydro_v07_basins_v01 WHERE comid={}),".format(i[0])

    print('len comID_array: ', len(comID_array))
    if len(comID_array) > 1:
        # querystring = "SELECT ST_Union(ARRAY[{}]) as catchment".format(selectstring[:-1])
        wkbquerystring = "SELECT ST_AsText(ST_Simplify(ST_Union(ARRAY[{}]), 0.01), 6) as catchment".format(selectstring[:-1])
        # wkbquerystring = "SELECT ST_AsText(ST_Union(ARRAY[{}]), 9) as catchment".format(selectstring[:-1])
    else:
        # querystring = "{};".format(selectstring[1:-2])
        wkbquerystring = "{};".format(singleselectstring)

    # print('query: ', wkbquerystring)
    # big_catchment = cat_pfaf_MERIT_Hydro_v07_Basins_v01.objects.raw(wkbquerystring)
    t3 = time.time()
    row = useSQLQuery(wkbquerystring)
    t4 = time.time()

    if precise:
        # create raster of watershed upstream of clickpoint
        # To much details for a 'select on map' tool
        pass
    print('C: ', comID_array)
    print('recursive time: ', t2-t1)
    print('recursive sql time: ', t2b-t2)
    print('concat time: ', t4-t3)
    print('total time: ', t4-t0)


    # TODO: if layer creation in GeoServer, then think about moving store/workspace to settings.py
    # store = 'playnew'  # 'new_vforwater_gis'
    # workspace = 'playnew'
    # layer_name = f'catchment{terminal_comid}'  # only used for a geoserver layer
    # if not get_layer(layer_name, store, workspace):
    #     create_layer("", layer_name, store, workspace, B, layertype="filtercatchment")

    return {'wkt': row[0][0]}
