import numpy as np
import pandas as pd
from django.contrib.gis.gdal import DataSource

from django.contrib.gis.geos import Point
from django.db import connection
from upload.models import merit_hydro_vect_level2, cat_pfaf_MERIT_Hydro_v07_Basins_v01, \
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

    # Threshold for watershed size in km² above which the script will revert to
    # low-resolution mode
    LOW_RES_THRESHOLD = 50000
    def addnode(B, node):
        """"
        Recursive function to assemble the list of upstream unit catchments
        :param B: list
        :param node: integer
        """
        # first, append the node to the basin
        B.append(node)

        # next, check whether the fields up1, up2, up3, and up4 contain a node ID
        for i in ['up1', 'up2', 'up3', 'up4']:
            up = rivers_of_catchment.filter(comid=node).values()[0][i]
            if up != 0:
                addnode(B, up)

    gages_df = pd.DataFrame(data=coords)
    if HIGH_RES:
        gages_df['lat_snap'] = np.nan
        gages_df['lng_snap'] = np.nan
        gages_df['snap_dist'] = 0

    crs = 'EPSG:4326'
    coordinates = Point(float(coords['lng'][0]), float(coords['lat'][0]), crs)
    # coordinates = Point(-17.73, 65.21, crs)
    # coordinates = Point(8.33, 48.65, 'EPSG:4326')

    merit_basins_shp = 'vfw_home/delineate_data/merit_hydro_vect_level2.shp'
    ds = DataSource(merit_basins_shp)

    # find high level catchment
    level2_basin = merit_hydro_vect_level2.objects.filter(geom__contains=coordinates)
    if not level2_basin:
        # Check if there is a catchment nearby
        # TODO: in case more than one catchment is in the result, sort, sort and use the closer one
        level2_basin = merit_hydro_vect_level2.objects.filter(geom__dwithin=(coordinates, D(km=9)))

        # if there is still no result, the return a warning
        if not level2_basin:
            print('nothing nearby, show error')
            pass

    # level2_basin.objects.annotate(distance=Distance('point', coordinates)).order_by('distance')
    level2_basin_id = level2_basin.values()[0]['id']
    basin_id = level2_basin.values()[0]['basin']
    id_range = (basin_id*1000000, (basin_id+1)*1000000-1)

    # find detail catchment
    level1_catchment = cat_pfaf_MERIT_Hydro_v07_Basins_v01.objects.filter(comid__range=id_range)
    try:
        catchment = level1_catchment.filter(geom__contains=coordinates)
    except Exception as e:
        print('No catchment at clickpoint: ', e)

    terminal_comid = catchment.values()[0]['comid']

    try:
        rivers_of_catchment = riv_pfaf_MERIT_Hydro_v07_Basins_v01.objects.filter(comid__range=id_range)
        river_comid = rivers_of_catchment.filter(comid=terminal_comid)
    except Exception as e:
        print('e in river: ', e)

    small_uparea = river_comid.values()[0]['uparea']  # might be used to check which resolution is used nexed

    # Let B be the list of unit catchments_gdf that are in the basin
    B = []
    addnode(B, terminal_comid)

    selectstring = ""
    singleselectstring = "SELECT ST_AsText(geom, 9) AS catchment " \
                         f"FROM cat_pfaf_merit_hydro_v07_basins_v01 WHERE comid={B[0]}"
    # union catchments
    for i in B:
        # create query
        selectstring += "(SELECT geom FROM cat_pfaf_merit_hydro_v07_basins_v01 WHERE comid={}),".format(i)

    if len(B) > 1:
        # querystring = "SELECT ST_Union(ARRAY[{}]) as catchment".format(selectstring[:-1])
        wkbquerystring = "SELECT ST_AsText(ST_Union(ARRAY[{}]), 9) as catchment".format(selectstring[:-1])
    else:
        # querystring = "{};".format(selectstring[1:-2])
        wkbquerystring = "{};".format(singleselectstring)

    big_catchment = cat_pfaf_MERIT_Hydro_v07_Basins_v01.objects.raw(wkbquerystring)
    try:
        with connection.cursor() as cursor:
            cursor.execute(wkbquerystring)
            row = cursor.fetchall()
    except Exception as e:
        print('e: ', e)

    if precise:
        # create raster of watershed upstream of clickpoint
        # To much details for a 'select on map' tool
        pass

    # TODO: if layer creation in GeoServer, then think about moving store/workspace to settings.py
    # store = 'playnew'  # 'new_vforwater_gis'
    # workspace = 'playnew'
    # layer_name = f'catchment{terminal_comid}'  # only used for a geoserver layer
    # if not get_layer(layer_name, store, workspace):
    #     create_layer("", layer_name, store, workspace, B, layertype="filtercatchment")

    return row[0][0]



# delete when data is in DB!!!
from pathlib import Path
from django.contrib.gis.utils import LayerMapping
# from vfw_home.models import DelineateBasins
import vfw_home
import geopandas as gpd
def fill_database():
    print('other def')
    name = 'merit_hydro_vect_level2.shp'
    path = Path(vfw_home.__file__).resolve().parent/'delineate_data'/name
    print('path: ', path)
    ds = DataSource(path)
    print('--- ds: ', ds)
    layer = ds[0]
    print('fields: ', layer.fields)
    geo_type = str(layer.geom_type).upper()
    print('layer.geom_type: ', geo_type)
    mapping = {
        # 'name': name,
        'basin': 'BASIN',
        'mpoly': geo_type
    }
    print('mapping: ', mapping)
    # print('path: ', str(path).split('.')[0])
    # try:
    #     # lm = LayerMapping(DelineateBasins, str(path), mapping)
    #     # print('lm1: ', lm)
    #     # class CustomLayerMapping(LayerMapping):
    #     #     print('2')
    #     #     def __init__(self, *args, **kwargs):
    #     #         print('3')
    #     #         self.custom = kwargs.pop('custom', {})
    #     #         super(CustomLayerMapping, self).__init__(*args, **kwargs)
    #     #
    #     #     def feature_kwargs(self, feature):
    #     #         print('4')
    #     #         kwargs = super(CustomLayerMapping, self).feature_kwargs(feature)
    #     #         kwargs.update(self.custom)
    #     #         return kwargs
    #     #
    #     # print('1')
    #     # lm = CustomLayerMapping(
    #     #     model=DelineateBasins,
    #     #     data=str(path),
    #     #     mapping={
    #     #         'basin': 'BASIN',
    #     #         'mpoly': geo_type
    #     #     },
    #     #     custom={
    #     #         'name': name,
    #     #
    #     #     }
    #     # )
    #     # print('lm: ', lm)
    #
    # except Exception as e:
    #     print('e: ', e)
