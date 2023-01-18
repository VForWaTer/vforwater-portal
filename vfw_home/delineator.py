import gpd as gpd
import numpy as np
import pandas as pd
from django.contrib.gis.gdal import DataSource
# import geopandas as gpd

# from shapely.geometry import Point
from django.contrib.gis.geos import Point


def delineate(coords, HIGH_RES):
    # code is based on delineator-1.0 of https://github.com/mheberger/delineator
    # Citation DOI: 10.5281/zenodo.7314287

    print('coords: ', coords)

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

    print('gages_df: ')
    print(gages_df)

    # Create a GeoPandas dataframe from our table of points
    # coordinates = [Point(xy) for xy in zip(gages_df['lng'], gages_df['lat'])]
    # coordinates = Point(float(coords['lng'][0]), float(coords['lat'][0]))
    crs = 'EPSG:4326'
    coordinates = Point(float(coords['lng'][0]), float(coords['lat'][0]), crs)
    # coordinates = Point(-17.73, 65.21, crs)
    # coordinates = Point(8.33, 48.65, 'EPSG:4326')
    print('coordinates: ', coordinates)
    # points_gdf = gpd.GeoDataFrame(gages_df, crs=crs, geometry=coordinates)
    # This line is adding a geometry column to gages_df, which I neither expected nor wanted.
    # gages_df.drop(['geometry'], axis=1, inplace=True)

    print("Finding out which Level 2 megabasin(s) your points are in")

    merit_basins_shp = 'vfw_home/delineate_data/merit_hydro_vect_level2.shp'
    print('path: ', merit_basins_shp)
    ds = DataSource(merit_basins_shp)
    print('ds: ', ds)
    layer = ds[0]
    print('layer: ', layer.fields)
    print('layer.fields: ', layer.fields)
    # megabasins = gpd.read_file(merit_basins_shp)
    # fill_database()
    from upload.models import merit_hydro_vect_level2, cat_pfaf_MERIT_Hydro_v07_Basins_v01, \
        riv_pfaf_MERIT_Hydro_v07_Basins_v01
    from django.contrib.gis.measure import D
    from django.contrib.gis.db.models.functions import Distance

    # find high level catchment
    level2_basin = merit_hydro_vect_level2.objects.filter(geom__contains=coordinates)
    if not level2_basin:
        print('No river catchment at click point. Now searching nearby...')
        # Check if there is a catchment nearby
        # TODO: in case more than one catchment is in the result, sort, sort and use the closer one
        level2_basin = merit_hydro_vect_level2.objects.filter(geom__dwithin=(coordinates, D(km=9)))

        # if there is still no result, the return a warning
        if not level2_basin:
            print('nothing nearby, show error')
            pass
    print('noch da')
    # level2_basin.objects.annotate(distance=Distance('point', coordinates)).order_by('distance')
    print('qs: ', level2_basin.values())
    print('qs: ', level2_basin.values()[0])
    level2_basin_id = level2_basin.values()[0]['id']
    basin_id = level2_basin.values()[0]['basin']
    id_range = (basin_id*1000000, (basin_id+1)*1000000-1)
    print('id range: ', id_range)

    print('level2_basin_id: ', level2_basin_id)
    print('basin_id: ', basin_id)

    # find detail catchment
    level1_catchment = cat_pfaf_MERIT_Hydro_v07_Basins_v01.objects.filter(comid__range=id_range)
    # print('level 1 catchment: ', level1_catchment.values())
    print('bla')
    try:
        catchment = level1_catchment.filter(geom__contains=coordinates)
    except Exception as e:
        print('e: ', e)

    print('catchment: ', catchment.values())
    print('catchment: ', catchment.values()[0])
    terminal_comid = catchment.values()[0]['comid']
    print('comid: ', terminal_comid)
    print('unitarea: ', catchment.values()[0]['unitarea'])

    try:
        print('search river')
        rivers_of_catchment = riv_pfaf_MERIT_Hydro_v07_Basins_v01.objects.filter(comid__range=id_range)
        river_comid = rivers_of_catchment.filter(comid=terminal_comid)
        print('got river')
        print('rivers_of_catchment: ', river_comid.values())
    except Exception as e:
        print('e in river: ', e)

    print('river_comid: ', river_comid.values())
    small_uparea = river_comid.values()[0]['uparea']  # might be used to check which resolution is used nexed
    print('small_uparea: ', small_uparea)

    # Let B be the list of unit catchments_gdf that are in the basin
    B = []
    addnode(B, terminal_comid)
    print('B: ', B)
    # create raster of watershed upstream of clickpoint


    pass


# delete when data is in DB!!!
from pathlib import Path
from django.contrib.gis.utils import LayerMapping
# from vfw_home.models import DelineateBasins
import vfw_home
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
