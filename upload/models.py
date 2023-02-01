from django.contrib.gis.db import models


class UploadedFile(models.Model):
    title = models.CharField(max_length=255, blank=True)
    file = models.FileField(upload_to='uploads/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        managed = True

# class DelineateBasins(models.Model):
#     name = models.CharField(max_length=50)
#     basin = models.BigIntegerField(blank=True)
#     comid = models.BigIntegerField(blank=True)
#     unitarea = models.FloatField(blank=True)
#     mpoly = models.MultiPolygonField()
#
#     # river:
#     lenghtkm = models.FloatField(blank=True)
#     lenghtdir = models.FloatField(blank=True)
#     sinuosity = models.FloatField(blank=True)
#     slope = models.FloatField(blank=True)
#     uparea = models.FloatField(blank=True)
#     order = models.BigIntegerField(blank=True)
#     strmDrop_t = models.FloatField(blank=True)
#     slope_taud = models.FloatField(blank=True)
#     nextDownID = models.BigIntegerField(blank=True)
#     maxup = models.BigIntegerField(blank=True)
#     up1 = models.BigIntegerField(blank=True)
#     up2 = models.BigIntegerField(blank=True)
#     up3 = models.BigIntegerField(blank=True)
#     up4 = models.BigIntegerField(blank=True)
#
#     def __str__(self):
#         return self.name
#
#     class Meta:
#         managed = True
#         db_table = 'delineate'

# class DelineateLevel2Basins(models.Model):
#     name = models.CharField(max_length=50)
#     basin = models.BigIntegerField(blank=True)
#     # comid = models.BigIntegerField(blank=True)
#     # unitarea = models.FloatField(blank=True)
#     mpoly = models.MultiPolygonField()

    # river:
    # lenghtkm = models.FloatField(blank=True)
    # lenghtdir = models.FloatField(blank=True)
    # sinuosity = models.FloatField(blank=True)
    # slope = models.FloatField(blank=True)
    # uparea = models.FloatField(blank=True)
    # order = models.BigIntegerField(blank=True)
    # strmDrop_t = models.FloatField(blank=True)
    # slope_taud = models.FloatField(blank=True)
    # nextDownID = models.BigIntegerField(blank=True)
    # maxup = models.BigIntegerField(blank=True)
    # up1 = models.BigIntegerField(blank=True)
    # up2 = models.BigIntegerField(blank=True)
    # up3 = models.BigIntegerField(blank=True)
    # up4 = models.BigIntegerField(blank=True)

    # def __str__(self):
    #     return self.name
    #
    # class Meta:
    #     managed = True
    #     db_table = 'delineateleveltwobasins'

class merit_hydro_vect_level2(models.Model):
    # name = models.CharField(max_length=50, blank=True)
    basin = models.BigIntegerField()
    geom = models.PolygonField(srid=4326)

    def __str__(self):
        return self.name

    class Meta:
        managed = True
        db_table = 'merit_hydro_vect_level2'



# merit_hydro_vect_level2_mapping = {
#     'basin': 'BASIN',
#     'geom': 'POLYGON',
# }


class riv_pfaf_MERIT_Hydro_v07_Basins_v01(models.Model):
    # name = models.CharField(max_length=50, blank=True)
    comid = models.BigIntegerField()
    lengthkm = models.FloatField()
    lengthdir = models.FloatField()
    sinuosity = models.FloatField()
    slope = models.FloatField()
    uparea = models.FloatField()
    order = models.BigIntegerField()
    strmdrop_t = models.FloatField()
    slope_taud = models.FloatField()
    nextdownid = models.BigIntegerField()
    maxup = models.BigIntegerField()
    up1 = models.BigIntegerField()
    up2 = models.BigIntegerField()
    up3 = models.BigIntegerField()
    up4 = models.BigIntegerField()
    geom = models.MultiLineStringField(srid=4326)

    def __str__(self):
        return self.comid

    class Meta:
        managed = True
        db_table = 'riv_pfaf_MERIT_Hydro_v07_Basins_v01'


# riv_pfaf_27_merit_hydro_v07_basins_v01_mapping = {
#     'comid': 'COMID',
#     'lengthkm': 'lengthkm',
#     'lengthdir': 'lengthdir',
#     'sinuosity': 'sinuosity',
#     'slope': 'slope',
#     'uparea': 'uparea',
#     'order': 'order',
#     'strmdrop_t': 'strmDrop_t',
#     'slope_taud': 'slope_taud',
#     'nextdownid': 'NextDownID',
#     'maxup': 'maxup',
#     'up1': 'up1',
#     'up2': 'up2',
#     'up3': 'up3',
#     'up4': 'up4',
#     'geom': 'LINESTRING',
# }

class cat_pfaf_MERIT_Hydro_v07_Basins_v01(models.Model):
    # name = models.CharField(max_length=50, blank=True)
    comid = models.BigIntegerField()
    unitarea = models.FloatField()
    geom = models.PolygonField(srid=4326)

    def __str__(self):
        return self.comid

    class Meta:
        managed = True
        db_table = 'cat_pfaf_MERIT_Hydro_v07_Basins_v01'


# cat_pfaf_27_merit_hydro_v07_basins_v01_mapping = {
#     'comid': 'COMID',
#     'unitarea': 'unitarea',
#     'geom': 'POLYGON',
# }


# Delineate workflow:
# - get coordinates
# - coordinates to point (lng, lat, crs)
# - load: megabasin = 'data/shp/basins_level2/merit_hydro_vect_level2.shp'

    # Overlay the gage points on the Level 2 Basins polygons to find out which
    # PFAF_2 basin each point falls inside of.
    # This is a spatial join in Geopandas
    # I try this in PostGIS

# - gages_basins_join = gpd.sjoin_nearest(points_gdf, megabasins, max_distance=SEARCH_DIST)


# VARS:
# If the requested watershed outlet is not inside a catchment, how far away
# from the point should we look for the nearest catchment (in degrees)
# SEARCH_DIST = 0.01

# - if several catchments in the result, get the closest

# - check if HIGH or LOW_RES
#     if HIGH_RES:
#         catchments_dir = HIGHRES_CATCHMENTS_DIR
#         catchments_lowres_gdf = None
#     else:
#         catchments_dir = LOWRES_CATCHMENTS_DIR

# HIGHRES_CATCHMENTS_DIR = "data/shp/merit_catchments"
# LOWRES_CATCHMENTS_DIR = "data/shp/catchments_simplified"

#  B = List of all up catchments
#  subbasins_gdf = catchments_gdf.loc[B]
